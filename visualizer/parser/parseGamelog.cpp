#include "parser.h"
#include "sexp/sexp.h"
#include "sexp/parser.h"
#include "sexp/sfcompat.h"

#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <iostream>

using namespace std;

namespace parser
{

char *ToLower( char *str )
{
  for( int i = 0; i < strlen( str ); i++ )
  {
    str[ i ] = tolower( str[ i ] );
  }
  return str;
}


static bool parsePlayer(Player& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.playerName = new char[strlen(sub->val)+1];
  strncpy(object.playerName, sub->val, strlen(sub->val));
  object.playerName[strlen(sub->val)] = 0;
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.time = atof(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.scrapAmount = atoi(sub->val);
  sub = sub->next;

  return true;

}
static bool parseMappable(Mappable& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseMappable.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseMappable.\n Parsing: " << *expression << endl;
    return false;
  }

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseMappable.\n Parsing: " << *expression << endl;
    return false;
  }

  object.y = atoi(sub->val);
  sub = sub->next;

  return true;

}
static bool parseDroid(Droid& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.owner = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.variant = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.attacksLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxAttacks = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.healthLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxHealth = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.movementLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxMovement = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.range = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.attack = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.armor = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxArmor = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.scrapWorth = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.hackedTurnsLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseDroid.\n Parsing: " << *expression << endl;
    return false;
  }

  object.hackets = atoi(sub->val);
  sub = sub->next;

  return true;

}
static bool parseTile(Tile& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.owner = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.turnsUntilAssembled = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.scrapAmount = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseTile.\n Parsing: " << *expression << endl;
    return false;
  }

  object.health = atoi(sub->val);
  sub = sub->next;

  return true;

}
static bool parseModelVariant(ModelVariant& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.name = new char[strlen(sub->val)+1];
  strncpy(object.name, sub->val, strlen(sub->val));
  object.name[strlen(sub->val)] = 0;
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.variant = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.cost = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxAttacks = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxHealth = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxMovement = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.range = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.attack = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxArmor = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseModelVariant.\n Parsing: " << *expression << endl;
    return false;
  }

  object.scrapWorth = atoi(sub->val);
  sub = sub->next;

  return true;

}

static bool parseMove(move& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = MOVE;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.fromX = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.fromY = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.toX = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.toY = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseAttack(attack& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = ATTACK;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parseattack.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parseattack.\n Parsing: " << *expression << endl;
    return false;
  }
  object.targetID = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseSpawn(spawn& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = SPAWN;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsespawn.\n Parsing: " << *expression << endl;
    return false;
  }
  object.sourceID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsespawn.\n Parsing: " << *expression << endl;
    return false;
  }
  object.unitID = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseHack(hack& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = HACK;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsehack.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsehack.\n Parsing: " << *expression << endl;
    return false;
  }
  object.targetID = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseOrbitalDrop(orbitalDrop& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = ORBITALDROP;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parseorbitalDrop.\n Parsing: " << *expression << endl;
    return false;
  }
  object.sourceID = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseRepair(repair& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = REPAIR;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parserepair.\n Parsing: " << *expression << endl;
    return false;
  }
  object.actingID = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parserepair.\n Parsing: " << *expression << endl;
    return false;
  }
  object.targetID = atoi(sub->val);
  sub = sub->next;
  return true;

}

static bool parseSexp(Game& game, sexp_t* expression)
{
  sexp_t* sub, *subsub;
  if( !expression ) return false;
  expression = expression->list;
  if( !expression ) return false;
  if(expression->val != NULL && strcmp(expression->val, "status") == 0)
  {
    GameState gs;
    while(expression->next != NULL)
    {
      expression = expression->next;
      sub = expression->list;
      if ( !sub ) return false;
      if(string(sub->val) == "game")
      {
          sub = sub->next;
          if ( !sub ) return false;
          gs.mapWidth = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.mapHeight = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.turnNumber = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.maxDroids = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.maxWalls = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.playerID = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.gameNumber = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.scrapRate = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.maxScrap = atoi(sub->val);
          sub = sub->next;
      }
      else if(string(sub->val) == "Player")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Player object;
          flag = parsePlayer(object, sub);
          gs.players[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Mappable")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Mappable object;
          flag = parseMappable(object, sub);
          gs.mappables[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Droid")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Droid object;
          flag = parseDroid(object, sub);
          gs.droids[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Tile")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Tile object;
          flag = parseTile(object, sub);
          gs.tiles[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "ModelVariant")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          ModelVariant object;
          flag = parseModelVariant(object, sub);
          gs.modelVariants[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
    }
    game.states.push_back(gs);
  }
  else if(string(expression->val) == "animations")
  {
    std::map< int, std::vector< SmartPointer< Animation > > > animations;
    while(expression->next)
    {
      expression = expression->next;
      sub = expression->list;
      if ( !sub ) return false;
      if(string(ToLower( sub->val ) ) == "move")
      {
        SmartPointer<move> animation = new move;
        if ( !parseMove(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "attack")
      {
        SmartPointer<attack> animation = new attack;
        if ( !parseAttack(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "spawn")
      {
        SmartPointer<spawn> animation = new spawn;
        if ( !parseSpawn(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "hack")
      {
        SmartPointer<hack> animation = new hack;
        if ( !parseHack(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "orbital-drop")
      {
        SmartPointer<orbitalDrop> animation = new orbitalDrop;
        if ( !parseOrbitalDrop(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "repair")
      {
        SmartPointer<repair> animation = new repair;
        if ( !parseRepair(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
    }
    game.states[game.states.size()-1].animations = animations;
  }
  else if(string(expression->val) == "ident")
  {
    expression = expression->next;
    if ( !expression ) return false;
    sub = expression->list;
    while(sub)
    {
      subsub = sub->list;
      if ( !subsub ) return false;
      int number = atoi(subsub->val);
      if(number >= 0)
      {
        subsub = subsub->next;
        if ( !subsub ) return false;
        subsub = subsub->next;
        if ( !subsub ) return false;
        game.players[number] = subsub->val;
      }
      sub = sub->next;
    }
  }
  else if(string(expression->val) == "game-winner")
  {
    expression = expression->next;
    if ( !expression ) return false;
    expression = expression->next;
    if ( !expression ) return false;
    expression = expression->next;
    if ( !expression ) return false;
    game.winner = atoi(expression->val);
		expression = expression->next;
		if( !expression ) return false;
		game.winReason = expression->val;
  }

  return true;
}


bool parseFile(Game& game, const char* filename)
{
  //bool value;
  FILE* in = fopen(filename, "r");
  //int size;
  if(!in)
    return false;

  parseFile(in);

  sexp_t* st = NULL;

  while((st = parse()))
  {
    if( !parseSexp(game, st) )
    {
      while(parse()); //empty the file, keep Lex happy.
      fclose(in);
      return false;
    }
    destroy_sexp(st);
  }

  fclose(in);

  return true;
}


bool parseGameFromString(Game& game, const char* string)
{

  parseString( string );

  sexp_t* st = NULL;

  while((st = parse()))
  {
    if( !parseSexp(game, st) )
    {
      while(parse()); //empty the file, keep Lex happy.
      return false;
    }
    destroy_sexp(st);
  }

  return true;
}

} // parser
