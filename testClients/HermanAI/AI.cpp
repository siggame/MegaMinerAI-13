#include "AI.h"
#include "util.h"
#include <iostream>
#include "string"
using namespace std;
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
void AI::init(){

}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  spawnDemDroids();
  getDemDroids();
  doStuffs();
  return true;
}

void AI::spawnDemDroids()
{
  spawnX=rand()%mapWidth();
  spawnY=rand()%mapHeight();
  int unitType=TERMINATOR;
  if(players[playerID()].scrapAmount() >= modelVariants[unitType].cost())
  {
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
        //spawn the turret
        players[playerID()].orbitalDrop(spawnX, spawnY, unitType);
      }
    }
  }
}

void AI::doStuffs()
{
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
        
        Droid* target = NULL;
        if(droids[i].variant() == REPAIRER)
        {
          target = getFriendInRange(droids[i].x(), droids[i].y(), droids[i].range());
        }
        else
        {
          target = getEnemyInRange(droids[i].x(), droids[i].y(), droids[i].range());
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
} 


//This function is run once, after your last turn.
void AI::end(){
  cout<<"WINNING!!"<<endl;
}

Tile* AI::getTile(const int x, const int y)
{
    if(0 <= x && x < mapWidth() && 0 <= y && y < mapHeight())
        return &tiles[x * mapHeight() + y];
    else
        return NULL;
}

void AI::getDemDroids()
{
  enemyDroids.clear();
  friendDroids.clear();
  enemyHangars.clear();
  for(int i=0; i< droids.size(); i++)
  {
    if(droids[i].owner() != playerID())
    {
      enemyDroids.push_back(& droids[i]);
      if(droids[i].variant() == HANGAR)
      {
        enemyHangars.push_back(& droids[i]);
      }
    }
    else if(droids[i].owner() == playerID())
    {
      friendDroids.push_back(& droids[i]);
    }
  }
}

Droid* AI::getEnemyInRange(int xloc, int yloc, int range)
{
  for(int i=0; i< enemyDroids.size(); i++)
  {
    if(abs(xloc - enemyDroids[i]->x()) + abs(yloc - enemyDroids[i]->y()) <= range &&
       !(xloc == enemyDroids[i]->x() && yloc == enemyDroids[i]->y()))
      return enemyDroids[i];
  }
  return NULL;
}
Droid* AI::getFriendInRange(int xloc, int yloc, int range)
{
  for(int i=0; i< friendDroids.size(); i++)
  {
    if(abs(xloc - friendDroids[i]->x()) + abs(yloc - friendDroids[i]->y()) <= range &&
       !(xloc == friendDroids[i]->x() && yloc == friendDroids[i]->y()))
      return enemyDroids[i];
  }
  return NULL;
}
