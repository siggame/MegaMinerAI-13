#include "AI.h"
#include "util.h"

enum
{
  CLAW = 0,
  ARCHER = 1,
  REPAIRER = 2,
  HACKER = 3,
  TURRET = 4,
  WALL = 5,
  TERMINATOR = 6,
  HANGAR = 7,
};

AI::AI(Connection* conn) : BaseAI(conn) {}

const char* AI::username()
{
  return "Shell AI";
}

const char* AI::password()
{
  return "password";
}

//This function is run once, before your first turn.
void AI::init()
{
  int offset = 0;
  bool found = false;
  while(!found)
  {
    //find a location without a hangar
    for(int i = 0; i < tiles.size(); i++)
    {
      //make sure that the tile is near the edge
      if(tiles[i].x() == (mapWidth() - 1) * playerID() + offset)
      {
        bool hangarPresent = false;
        //check for hangar
        for(int z = 0; z < droids.size(); z++)
        {
          if(droids[z].x() == tiles[i].x() && droids[z].y() == tiles[i].y())
          {
            hangarPresent = true;
            break;
          }
        }
        if(!hangarPresent)
        {
          spawnX = tiles[i].x();
          spawnY = tiles[i].y();
          found = true;
          break;
        }
      }
    }
    //if nothing was found then move away from the edge
    if(!found)
    {
      //if on the left
      if(playerID() == 0)
      {
        offset++;
      }
      else
      {
        //on the right
        offset--;
      }
    }
  }
}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  //try to spawn a claw near your side
  //make sure you own enough scrap
  if(players[playerID()].scrapAmount() >= modelVariants[CLAW].cost())
  {
    //make sure nothing is spawning there
    if(getTile(spawnX, spawnY)->turnsUntilAssembled() == 0)
    {
      bool spawn = true;
      //make sure there isn't a hangar there
      for(int i = 0; i < droids.size(); i++)
      {
        //if the droid's x and y is the same as the spawn point
        if(droids[i].x() == spawnX && droids[i].y() == spawnY)
        {
          //if the droid is a hangar
          if(droids[i].variant() == HANGAR)
          {
            //can't spawn on top of hangars
            spawn = false;
            break;
          }
        }
      }
      if(spawn)
      {
        //spawn the claw
        players[playerID()].orbitalDrop(spawnX, spawnY, CLAW);
      }
    }
  }
  //loop through all of the droids
  for(int i = 0; i < droids.size(); i++)
  {
    //if you have control of the droid
    if((droids[i].owner() == playerID() && droids[i].hackedTurnsLeft() <= 0) ||
       (droids[i].owner() != playerID() && droids[i].hackedTurnsLeft() > 0))
    {
      //if there are any moves to be done
      if(droids[i].movementLeft() > 0)
      {
        //try to move towards the enemy
        int changeX = 1;
        //if on the right move towards the left
        if(playerID() == 1)
        {
          changeX = -1;
        }
        bool move = true;
        //check if there is a droid on that tile
        for(int z = 0; z < droids.size(); z++)
        {
          //if the two droids are different
          if(droids[z].id() != droids[i].id())
          {
            //if there is a droid to run into
            if(droids[z].x() == droids[i].x() + changeX && droids[z].y() == droids[i].y())
            {
              //don't move
              move = false;
            }
          }
        }
        //move if okay and within map boundaries
        if(move && droids[i].x() + changeX >= 0 && droids[i].x() + changeX < mapWidth())
        {
          droids[i].move(droids[i].x() + changeX, droids[i].y());
        }
      }
      //if there are any attacks left
      if(droids[i].attacksLeft() > 0)
      {
        //find a target towards the enemy
        int changeX = 1;
        //enemy is to the left if playerID is one
        if(playerID() == 1)
        {
          changeX = -1;
        }
        Droid* target = NULL;
        for(int z = 0; z < droids.size(); z++)
        {
          //if the droid is there make it a target
          if(droids[z].x() == droids[i].x() + changeX && droids[z].y() == droids[i].y() && droids[z].healthLeft() > 0)
          {
            target = &droids[z];
          }
        }
        //if a target was found
        if(target != NULL)
        {
          //repairer logic
          if(droids[i].variant() == REPAIRER)
          {
            //only try to heal your units or hacked enemy units
            if((target->owner() == playerID() && target->hackedTurnsLeft() <= 0) ||
               (target->owner() != playerID() && target->hackedTurnsLeft() > 0))
            {
              //heal the target
              droids[i].operate(target->x(), target->y());
            }
          }
          //hacker unit logic
          else if(droids[i].variant() == HACKER)
          {
            //only operate on non-hacked enemy units
            if(target->owner() != playerID() && target->hackedTurnsLeft() > 0)
            {
              //don't hack hangars or walls
              if(target->variant() != HANGAR && target->variant() != WALL)
              {
                //hack the target
                droids[i].operate(target->x(), target->y());
              }
            }
          }
          //other unit logic
          else
          {
            //only operate on hacked friendly units or enemy units
            if((target->owner() == playerID() && target->hackedTurnsLeft() > 0) ||
               (target->owner() != playerID() && target->hackedTurnsLeft() <= 0))
            {
              //attack the target
              droids[i].operate(target->x(), target->y());
            }
          }
        }
      }
    }
  }
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}

//This functions returns a pointer to a tile, or returns NULL for an invalid tile
Tile* AI::getTile(int x, int y)
{
  if(x >= mapWidth() || x < 0 || y >= mapHeight() || y < 0)
  {
    return NULL;
  }
  return &tiles[y + x * mapHeight()];
}
