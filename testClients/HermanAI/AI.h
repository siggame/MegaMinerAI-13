#ifndef AI_H
#define AI_H

#include "BaseAI.h"
#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <cmath>
///The class implementing gameplay logic.
class AI: public BaseAI
{
  int spawnX, spawnY;
public:
  AI(Connection* c);
  virtual const char* username();
  virtual const char* password();
  virtual void init();
  virtual bool run();
  virtual void end();
  
  //vectors! vectors everywhere
  std::vector<Droid*> enemyDroids;
  std::vector<Droid*> friendDroids;
  std::vector<Droid*> enemyHangars;
  
  
  virtual Tile* getTile(int x, int y);
  void spawnDemDroids();
  void doStuffs();
  void getDemDroids();
  Droid* getEnemyInRange(int xloc, int yloc, int range);
  Droid* getFriendInRange(int xloc, int yloc, int range);
  Droid* getNearestHangar(int xloc, int yloc);
  Droid* getNearestEnemy(int xloc, int yloc);
  Droid* getNearestFriend(int xloc, int yloc);
  
  void moveTo(Droid & droid, int x, int y);
  bool validMove(const int x, const int y);

  
};

#endif