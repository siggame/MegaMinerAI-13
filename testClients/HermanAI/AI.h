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
  std::vector<Droid*> enemyClaw;
  std::vector<Droid*> friendClaw;
  std::vector<Droid*> enemyArcher;
  std::vector<Droid*> friendArcher;
  std::vector<Droid*> enemyRepairer;
  std::vector<Droid*> friendRepairer;
  std::vector<Droid*> enemyHacker;
  std::vector<Droid*> friendHacker;
  std::vector<Droid*> enemyTurret;
  std::vector<Droid*> friendTurret;
  std::vector<Droid*> enemyWall;
  std::vector<Droid*> friendWall;
  std::vector<Droid*> enemyTerminator;
  std::vector<Droid*> friendTerminator;
  
  virtual Tile* getTile(int x, int y);
  void spawnBitches();
  void doStuffs();
};

#endif