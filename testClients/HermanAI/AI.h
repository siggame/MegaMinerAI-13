#ifndef AI_H
#define AI_H

#include "BaseAI.h"

///The class implementing gameplay logic.
class AI: public BaseAI
{
public:
  AI(Connection* c);
  virtual const char* username();
  virtual const char* password();
  virtual void init();
  virtual bool run();
  virtual void spawn();
  virtual void end();
  std::vector<Droid*> friendHangar;
  std::vector<Droid*> enemyHangar;
  Tile* getTile(const int x, const int y);
};

#endif
