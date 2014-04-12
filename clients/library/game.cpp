//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#pragma warning(disable : 4996)

#include <string>
#include <cstring>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <fstream>
#include <memory>
#include <cmath>

#include "game.h"
#include "network.h"
#include "structures.h"

#include "sexp/sfcompat.h"

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

#ifdef _WIN32
//Doh, namespace collision.
namespace Windows
{
    #include <Windows.h>
};
#else
#include <unistd.h>
#endif

#ifdef ENABLE_THREADS
#define LOCK(X) pthread_mutex_lock(X)
#define UNLOCK(X) pthread_mutex_unlock(X)
#else
#define LOCK(X)
#define UNLOCK(X)
#endif

using std::cout;
using std::cerr;
using std::endl;
using std::stringstream;
using std::string;
using std::ofstream;

DLLEXPORT Connection* createConnection()
{
  Connection* c = new Connection;
  c->socket = -1;
  #ifdef ENABLE_THREADS
  pthread_mutex_init(&c->mutex, NULL);
  #endif

  c->mapWidth = 0;
  c->mapHeight = 0;
  c->turnNumber = 0;
  c->maxDroids = 0;
  c->playerID = 0;
  c->gameNumber = 0;
  c->scrapRate = 0;
  c->maxScrap = 0;
  c->dropTime = 0;
  c->Players = NULL;
  c->PlayerCount = 0;
  c->Mappables = NULL;
  c->MappableCount = 0;
  c->Droids = NULL;
  c->DroidCount = 0;
  c->Tiles = NULL;
  c->TileCount = 0;
  c->ModelVariants = NULL;
  c->ModelVariantCount = 0;
  return c;
}

DLLEXPORT void destroyConnection(Connection* c)
{
  #ifdef ENABLE_THREADS
  pthread_mutex_destroy(&c->mutex);
  #endif
  if(c->Players)
  {
    for(int i = 0; i < c->PlayerCount; i++)
    {
      delete[] c->Players[i].playerName;
    }
    delete[] c->Players;
  }
  if(c->Mappables)
  {
    for(int i = 0; i < c->MappableCount; i++)
    {
    }
    delete[] c->Mappables;
  }
  if(c->Droids)
  {
    for(int i = 0; i < c->DroidCount; i++)
    {
    }
    delete[] c->Droids;
  }
  if(c->Tiles)
  {
    for(int i = 0; i < c->TileCount; i++)
    {
    }
    delete[] c->Tiles;
  }
  if(c->ModelVariants)
  {
    for(int i = 0; i < c->ModelVariantCount; i++)
    {
      delete[] c->ModelVariants[i].name;
    }
    delete[] c->ModelVariants;
  }
  delete c;
}

DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port)
{
  c->socket = open_server_connection(host, port);
  return c->socket + 1; //false if socket == -1
}

DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password)
{
  string expr = "(login \"";
  expr += username;
  expr += "\" \"";
  expr += password;
  expr +="\")";

  send_string(c->socket, expr.c_str());

  sexp_t* expression, *message;

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  message = expression->list;
  if(message->val == NULL || strcmp(message->val, "login-accepted") != 0)
  {
    cerr << "Unable to login to server" << endl;
    destroy_sexp(expression);
    return 0;
  }
  destroy_sexp(expression);
  return 1;
}

DLLEXPORT int createGame(Connection* c)
{
  sexp_t* expression, *number;

  send_string(c->socket, "(create-game)");

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  number = expression->list->next;
  c->gameNumber = atoi(number->val);
  destroy_sexp(expression);

  std::cout << "Creating game " << c->gameNumber << endl;

  c->playerID = 0;

  return c->gameNumber;
}

DLLEXPORT int joinGame(Connection* c, int gameNum, const char* playerType)
{
  sexp_t* expression;
  stringstream expr;

  c->gameNumber = gameNum;

  expr << "(join-game " << c->gameNumber << " "<< playerType << ")";
  send_string(c->socket, expr.str().c_str());

  char* reply = rec_string(c->socket);
  expression = extract_sexpr(reply);
  delete[] reply;

  if(strcmp(expression->list->val, "join-accepted") == 0)
  {
    destroy_sexp(expression);
    c->playerID = 1;
    send_string(c->socket, "(game-start)");
    return 1;
  }
  else if(strcmp(expression->list->val, "create-game") == 0)
  {
    std::cout << "Game did not exist, creating game " << c->gameNumber << endl;
    destroy_sexp(expression);
    c->playerID = 0;
    return 1;
  }
  else
  {
    cerr << "Cannot join game "<< c->gameNumber << ": " << expression->list->next->val << endl;
    destroy_sexp(expression);
    return 0;
  }
}

DLLEXPORT void endTurn(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(end-turn)");
  UNLOCK( &c->mutex );
}

DLLEXPORT void getStatus(Connection* c)
{
  LOCK( &c->mutex );
  send_string(c->socket, "(game-status)");
  UNLOCK( &c->mutex );
}


DLLEXPORT int playerTalk(_Player* object, char* message)
{
  stringstream expr;
  expr << "(game-talk " << object->id
      << " \"" << escape_string(message) << "\""
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);
  return 1;
}

DLLEXPORT int playerOrbitalDrop(_Player* object, int x, int y, int variant)
{
  stringstream expr;
  expr << "(game-orbital-drop " << object->id
       << " " << x
       << " " << y
       << " " << variant
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);

  Connection* c = object->_c;

  // Check bounds
  if (x < 0 || x >= getMapWidth(c) || y < 0 || y >= getMapHeight(c))
    return 0;
  // Check drop type
  if (variant < 0 || variant > 7)
    return 0;

  int cost = getModelVariant(c, variant)->cost;

  // Check cost
  if (getPlayer(c, getPlayerID(c))->scrapAmount < cost)
    return 0;

  _Tile* tile = getTile(c, x * getMapHeight(c) + y);

  // Check for previous orbital drop
  if (tile->turnsUntilAssembled > 0)
    return 0;

  // Check for hangars
  for (int i = 0; i < getDroidCount(c); ++i)
  {
    if (getDroid(c, i)->x == x && getDroid(c, i)->y == y && getDroid(c, i)->variant == 7)
      return 0;
  }

  int xoff = getPlayerID(c) ? getMapWidth(c) : -1;

  tile->turnsUntilAssembled = abs(xoff - x) * getDropTime(c);
  tile->variantToAssemble = variant;
  tile->owner = getPlayerID(c);

  getPlayer(c, getPlayerID(c))->scrapAmount -= cost;

  return 1;
}



DLLEXPORT int droidMove(_Droid* object, int x, int y)
{
  stringstream expr;
  expr << "(game-move " << object->id
       << " " << x
       << " " << y
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);

  Connection* c = object->_c;

  // Ownership check
  if (object->owner != (getPlayerID(c) ^ (object->hackedTurnsLeft > 0)))
    return 0;
  // Alive?
  if (object->healthLeft <= 0)
    return 0;
  // Movement left
  if (object->movementLeft <= 0)
    return 0;
  // Check bounds
  if (x < 0 || x >= getMapWidth(c) || y < 0 || y >= getMapHeight(c))
    return 0;

  _Tile* tile = getTile(c, x * getMapHeight(c) + y);

  // Check distance
  if (abs(x - object->x) + abs(y - object->y) != 1)
    return 0;

  // Check collision with droids
  for (int i = 0; i < getDroidCount(c); ++i)
  {
    if (getDroid(c,i)->healthLeft > 0 && getDroid(c, i)->x == x && getDroid(c, i)->y == y)
      return 0;
  }

  object->x = x;
  object->y = y;

  object->movementLeft--;

  return 1;
}

DLLEXPORT int droidOperate(_Droid* object, int x, int y)
{
  stringstream expr;
  expr << "(game-operate " << object->id
       << " " << x
       << " " << y
       << ")";
  LOCK( &object->_c->mutex);
  send_string(object->_c->socket, expr.str().c_str());
  UNLOCK( &object->_c->mutex);

  Connection* c = object->_c;


  // Check bounds
  if (x < 0 || x >= getMapWidth(c) || y < 0 || y >= getMapHeight(c))
    return 0;
  // Check ownership
  if (object->owner != (getPlayerID(c) ^ (object->hackedTurnsLeft > 0)))
    return 0;
  // Check attacks left
  if (object->attacksLeft <= 0)
    return 0;
  // Check if dead
  if (object->healthLeft <= 0)
    return 0;
  // Check distance
  if (abs(x - object->x) + abs(y - object->y) > object->range)
    return 0;

  bool attacked_droid = false;

  // Check if attacking droid
  for (int i = 0; i < getDroidCount(c); ++i)
  {
    _Droid* target = getDroid(c, i);
    if (target->x == x && target->y == y)
    {
      // Check for heal
      if (object->attack < 0)
      {
        // Check target ownership
        if (target->owner != (getPlayerID(c) ^ (target->hackedTurnsLeft > 0)))
          return 0;

        // Repair armor
        target->armor -= object->attack;
        if (target->armor > target->maxArmor)
          target->armor = target->maxArmor;

        // Reduce hackets
        target->hackets += object->attack;
        if (target->hackets < 0)
          target->hackets = 0;
      }
      else
      {
        // Check target ownership
        if (object->variant == 3 && target->owner == getPlayerID(c) && target->hackedTurnsLeft > 0)
          return 0;
        if (target->owner == (getPlayerID(c) ^ (target->hackedTurnsLeft > 0)))
          return 0;

        // Check for hacker
        if (object->variant == 3)
        {
          target->hackets += object->attack;
          if (target->hackets >= target->hacketsMax)
          {
            target->hackedTurnsLeft = target->turnsToBeHacked;
            target->hackets = 0;
          }
        }
        else
        {
          int damage;
          if (object->attack > target->armor)
          {
            target->armor = 0;
            damage = target->armor - object->attack;
          }
          if (target->armor > 0)
          {
            damage = static_cast<int>(object->attack * ((target->maxArmor - target->armor) / static_cast<double>(target->maxArmor)));
            target->armor -= object->attack;
            if (target->armor < 0)
              target->armor = 0;
          }
          else
          {
            damage = object->attack;
          }

          target->healthLeft -= damage;
        }
      }

      attacked_droid = true;
      break;
    }
  }

  object->attacksLeft--;
  return 1;
}




//Utility functions for parsing data
void parsePlayer(Connection* c, _Player* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->playerName = new char[strlen(sub->val)+1];
  strncpy(object->playerName, sub->val, strlen(sub->val));
  object->playerName[strlen(sub->val)] = 0;
  sub = sub->next;
  object->time = atof(sub->val);
  sub = sub->next;
  object->scrapAmount = atoi(sub->val);
  sub = sub->next;

}
void parseMappable(Connection* c, _Mappable* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;

}
void parseDroid(Connection* c, _Droid* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->variant = atoi(sub->val);
  sub = sub->next;
  object->attacksLeft = atoi(sub->val);
  sub = sub->next;
  object->maxAttacks = atoi(sub->val);
  sub = sub->next;
  object->healthLeft = atoi(sub->val);
  sub = sub->next;
  object->maxHealth = atoi(sub->val);
  sub = sub->next;
  object->movementLeft = atoi(sub->val);
  sub = sub->next;
  object->maxMovement = atoi(sub->val);
  sub = sub->next;
  object->range = atoi(sub->val);
  sub = sub->next;
  object->attack = atoi(sub->val);
  sub = sub->next;
  object->armor = atoi(sub->val);
  sub = sub->next;
  object->maxArmor = atoi(sub->val);
  sub = sub->next;
  object->scrapWorth = atoi(sub->val);
  sub = sub->next;
  object->turnsToBeHacked = atoi(sub->val);
  sub = sub->next;
  object->hackedTurnsLeft = atoi(sub->val);
  sub = sub->next;
  object->hackets = atoi(sub->val);
  sub = sub->next;
  object->hacketsMax = atoi(sub->val);
  sub = sub->next;

}
void parseTile(Connection* c, _Tile* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->x = atoi(sub->val);
  sub = sub->next;
  object->y = atoi(sub->val);
  sub = sub->next;
  object->owner = atoi(sub->val);
  sub = sub->next;
  object->turnsUntilAssembled = atoi(sub->val);
  sub = sub->next;
  object->variantToAssemble = atoi(sub->val);
  sub = sub->next;

}
void parseModelVariant(Connection* c, _ModelVariant* object, sexp_t* expression)
{
  sexp_t* sub;
  sub = expression->list;

  object->_c = c;

  object->id = atoi(sub->val);
  sub = sub->next;
  object->name = new char[strlen(sub->val)+1];
  strncpy(object->name, sub->val, strlen(sub->val));
  object->name[strlen(sub->val)] = 0;
  sub = sub->next;
  object->variant = atoi(sub->val);
  sub = sub->next;
  object->cost = atoi(sub->val);
  sub = sub->next;
  object->maxAttacks = atoi(sub->val);
  sub = sub->next;
  object->maxHealth = atoi(sub->val);
  sub = sub->next;
  object->maxMovement = atoi(sub->val);
  sub = sub->next;
  object->range = atoi(sub->val);
  sub = sub->next;
  object->attack = atoi(sub->val);
  sub = sub->next;
  object->maxArmor = atoi(sub->val);
  sub = sub->next;
  object->scrapWorth = atoi(sub->val);
  sub = sub->next;
  object->turnsToBeHacked = atoi(sub->val);
  sub = sub->next;
  object->hacketsMax = atoi(sub->val);
  sub = sub->next;

}

DLLEXPORT int networkLoop(Connection* c)
{
  while(true)
  {
    sexp_t* base, *expression, *sub, *subsub;

    char* message = rec_string(c->socket);
    string text = message;
    base = extract_sexpr(message);
    delete[] message;
    expression = base->list;
    if(expression->val != NULL && strcmp(expression->val, "game-winner") == 0)
    {
      expression = expression->next->next->next;
      int winnerID = atoi(expression->val);
      if(winnerID == c->playerID)
      {
        cout << "You win!" << endl << expression->next->val << endl;
      }
      else
      {
        cout << "You lose. :(" << endl << expression->next->val << endl;
      }
      stringstream expr;
      expr << "(request-log " << c->gameNumber << ")";
      send_string(c->socket, expr.str().c_str());
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "log") == 0)
    {
      ofstream out;
      stringstream filename;
      expression = expression->next;
      filename << expression->val;
      filename << ".gamelog";
      expression = expression->next;
      out.open(filename.str().c_str());
      if (out.good())
        out.write(expression->val, strlen(expression->val));
      else
        cerr << "Error : Could not create log." << endl;
      out.close();
      destroy_sexp(base);
      return 0;
    }
    else if(expression->val != NULL && strcmp(expression->val, "game-accepted")==0)
    {
      char gameID[30];

      expression = expression->next;
      strcpy(gameID, expression->val);
      cout << "Created game " << gameID << endl;
    }
    else if(expression->val != NULL && strstr(expression->val, "denied"))
    {
      cout << expression->val << endl;
      cout << expression->next->val << endl;
    }
    else if(expression->val != NULL && strcmp(expression->val, "status") == 0)
    {
      while(expression->next != NULL)
      {
        expression = expression->next;
        sub = expression->list;
        if(string(sub->val) == "game")
        {
          sub = sub->next;
          c->mapWidth = atoi(sub->val);
          sub = sub->next;

          c->mapHeight = atoi(sub->val);
          sub = sub->next;

          c->turnNumber = atoi(sub->val);
          sub = sub->next;

          c->maxDroids = atoi(sub->val);
          sub = sub->next;

          c->playerID = atoi(sub->val);
          sub = sub->next;

          c->gameNumber = atoi(sub->val);
          sub = sub->next;

          c->scrapRate = atoi(sub->val);
          sub = sub->next;

          c->maxScrap = atoi(sub->val);
          sub = sub->next;

          c->dropTime = atoi(sub->val);
          sub = sub->next;

        }
        else if(string(sub->val) == "Player")
        {
          if(c->Players)
          {
            for(int i = 0; i < c->PlayerCount; i++)
            {
              delete[] c->Players[i].playerName;
            }
            delete[] c->Players;
          }
          c->PlayerCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Players = new _Player[c->PlayerCount];
          for(int i = 0; i < c->PlayerCount; i++)
          {
            sub = sub->next;
            parsePlayer(c, c->Players+i, sub);
          }
        }
        else if(string(sub->val) == "Mappable")
        {
          if(c->Mappables)
          {
            for(int i = 0; i < c->MappableCount; i++)
            {
            }
            delete[] c->Mappables;
          }
          c->MappableCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Mappables = new _Mappable[c->MappableCount];
          for(int i = 0; i < c->MappableCount; i++)
          {
            sub = sub->next;
            parseMappable(c, c->Mappables+i, sub);
          }
        }
        else if(string(sub->val) == "Droid")
        {
          if(c->Droids)
          {
            for(int i = 0; i < c->DroidCount; i++)
            {
            }
            delete[] c->Droids;
          }
          c->DroidCount =  sexp_list_length(expression)-1; //-1 for the header
          c->Droids = new _Droid[c->DroidCount];
          for(int i = 0; i < c->DroidCount; i++)
          {
            sub = sub->next;
            parseDroid(c, c->Droids+i, sub);
          }
        }
        else if(string(sub->val) == "Tile")
        {
          if(c->Tiles)
          {
            sub = sub->next;
            for(int i = 0; i < c->TileCount; i++)
            {
              if(!sub)
              {
                break;
              }
              int id = atoi(sub->list->val);
              if(id == c->Tiles[i].id)
              {
                parseTile(c, c->Tiles+i, sub);
                sub = sub->next;
              }
            }
          }
          else
          {
            c->TileCount =  sexp_list_length(expression)-1; //-1 for the header
            c->Tiles = new _Tile[c->TileCount];
            for(int i = 0; i < c->TileCount; i++)
            {
              sub = sub->next;
              parseTile(c, c->Tiles+i, sub);
            }
          }
        }
        else if(string(sub->val) == "ModelVariant")
        {
          if(c->ModelVariants)
          {
            sub = sub->next;
            for(int i = 0; i < c->ModelVariantCount; i++)
            {
              if(!sub)
              {
                break;
              }
              int id = atoi(sub->list->val);
              if(id == c->ModelVariants[i].id)
              {
                delete[] c->ModelVariants[i].name;
                parseModelVariant(c, c->ModelVariants+i, sub);
                sub = sub->next;
              }
            }
          }
          else
          {
            c->ModelVariantCount =  sexp_list_length(expression)-1; //-1 for the header
            c->ModelVariants = new _ModelVariant[c->ModelVariantCount];
            for(int i = 0; i < c->ModelVariantCount; i++)
            {
              sub = sub->next;
              parseModelVariant(c, c->ModelVariants+i, sub);
            }
          }
        }
      }
      destroy_sexp(base);
      return 1;
    }
    else
    {
#ifdef SHOW_WARNINGS
      cerr << "Unrecognized message: " << text << endl;
#endif
    }
    destroy_sexp(base);
  }
}

DLLEXPORT _Player* getPlayer(Connection* c, int num)
{
  return c->Players + num;
}
DLLEXPORT int getPlayerCount(Connection* c)
{
  return c->PlayerCount;
}

DLLEXPORT _Mappable* getMappable(Connection* c, int num)
{
  return c->Mappables + num;
}
DLLEXPORT int getMappableCount(Connection* c)
{
  return c->MappableCount;
}

DLLEXPORT _Droid* getDroid(Connection* c, int num)
{
  return c->Droids + num;
}
DLLEXPORT int getDroidCount(Connection* c)
{
  return c->DroidCount;
}

DLLEXPORT _Tile* getTile(Connection* c, int num)
{
  return c->Tiles + num;
}
DLLEXPORT int getTileCount(Connection* c)
{
  return c->TileCount;
}

DLLEXPORT _ModelVariant* getModelVariant(Connection* c, int num)
{
  return c->ModelVariants + num;
}
DLLEXPORT int getModelVariantCount(Connection* c)
{
  return c->ModelVariantCount;
}


DLLEXPORT int getMapWidth(Connection* c)
{
  return c->mapWidth;
}
DLLEXPORT int getMapHeight(Connection* c)
{
  return c->mapHeight;
}
DLLEXPORT int getTurnNumber(Connection* c)
{
  return c->turnNumber;
}
DLLEXPORT int getMaxDroids(Connection* c)
{
  return c->maxDroids;
}
DLLEXPORT int getPlayerID(Connection* c)
{
  return c->playerID;
}
DLLEXPORT int getGameNumber(Connection* c)
{
  return c->gameNumber;
}
DLLEXPORT int getScrapRate(Connection* c)
{
  return c->scrapRate;
}
DLLEXPORT int getMaxScrap(Connection* c)
{
  return c->maxScrap;
}
DLLEXPORT int getDropTime(Connection* c)
{
  return c->dropTime;
}
