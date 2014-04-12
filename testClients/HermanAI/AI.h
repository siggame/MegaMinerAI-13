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
  virtual Tile* getTile(int x, int y);
  void spawnBitches();
};

#endif