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
void AI::init(){}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  
  return true;
}

void AI::spawn()
{
  int unitType=rand()%7;
  int spawnX = rand()%
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
        //spawn the claw
        players[playerID()].orbitalDrop(spawnX, spawnY, unitType);
      }
    }
  }
}

//This function is run once, after your last turn.
void AI::end(){
  cout<<"WINNING!!"<<endl;
}




