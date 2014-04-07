//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that

#include "BaseAI.h"
#include "game.h"

int BaseAI::mapWidth()
{
  return getMapWidth(c);
}
int BaseAI::mapHeight()
{
  return getMapHeight(c);
}
int BaseAI::turnNumber()
{
  return getTurnNumber(c);
}
int BaseAI::maxDroids()
{
  return getMaxDroids(c);
}
int BaseAI::playerID()
{
  return getPlayerID(c);
}
int BaseAI::gameNumber()
{
  return getGameNumber(c);
}
int BaseAI::scrapRate()
{
  return getScrapRate(c);
}
int BaseAI::maxScrap()
{
  return getMaxScrap(c);
}
int BaseAI::dropTime()
{
  return getDropTime(c);
}

bool BaseAI::startTurn()
{
  static bool initialized = false;
  int count = 0;
  count = getPlayerCount(c);
  players.clear();
  players.resize(count);
  for(int i = 0; i < count; i++)
  {
    players[i] = Player(getPlayer(c, i));
  }

  count = getMappableCount(c);
  mappables.clear();
  mappables.resize(count);
  for(int i = 0; i < count; i++)
  {
    mappables[i] = Mappable(getMappable(c, i));
  }

  count = getDroidCount(c);
  droids.clear();
  droids.resize(count);
  for(int i = 0; i < count; i++)
  {
    droids[i] = Droid(getDroid(c, i));
  }

  count = getTileCount(c);
  tiles.clear();
  tiles.resize(count);
  for(int i = 0; i < count; i++)
  {
    tiles[i] = Tile(getTile(c, i));
  }

  count = getModelVariantCount(c);
  modelVariants.clear();
  modelVariants.resize(count);
  for(int i = 0; i < count; i++)
  {
    modelVariants[i] = ModelVariant(getModelVariant(c, i));
  }

  if(!initialized)
  {
    initialized = true;
    init();
  }
  return run();
}

BaseAI::BaseAI(Connection* conn) : c(conn) {}
BaseAI::~BaseAI() {}
