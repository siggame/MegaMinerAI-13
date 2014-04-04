//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

struct Connection;
struct _Player;
struct _Mappable;
struct _Droid;
struct _Tile;
struct _ModelVariant;


struct _Player
{
  Connection* _c;
  int id;
  char* playerName;
  float time;
  int scrapAmount;
};
struct _Mappable
{
  Connection* _c;
  int id;
  int x;
  int y;
};
struct _Droid
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int variant;
  int attacksLeft;
  int maxAttacks;
  int healthLeft;
  int maxHealth;
  int movementLeft;
  int maxMovement;
  int range;
  int attack;
  int armor;
  int maxArmor;
  int scrapWorth;
  int turnsToBeHacked;
  int hackedTurnsLeft;
  int hackets;
  int hacketsMax;
};
struct _Tile
{
  Connection* _c;
  int id;
  int x;
  int y;
  int owner;
  int turnsUntilAssembled;
  int variantToAssemble;
};
struct _ModelVariant
{
  Connection* _c;
  int id;
  char* name;
  int variant;
  int cost;
  int maxAttacks;
  int maxHealth;
  int maxMovement;
  int range;
  int attack;
  int maxArmor;
  int scrapWorth;
  int turnsToBeHacked;
  int hacketsMax;
};

#endif
