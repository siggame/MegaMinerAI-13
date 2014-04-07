//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <iostream>
#include <vector>
#include <map>
#include <string>

#include "smartpointer.h"

namespace parser
{

const int SPAWN = 0;
const int REPAIR = 1;
const int MOVE = 2;
const int HACK = 3;
const int ORBITALDROP = 4;
const int ATTACK = 5;

struct Player
{
  int id;
  char* playerName;
  float time;
  int scrapAmount;

  friend std::ostream& operator<<(std::ostream& stream, Player obj);
};

struct Mappable
{
  int id;
  int x;
  int y;

  friend std::ostream& operator<<(std::ostream& stream, Mappable obj);
};

struct Droid: public Mappable 
{
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

  friend std::ostream& operator<<(std::ostream& stream, Droid obj);
};

struct Tile: public Mappable 
{
  int owner;
  int turnsUntilAssembled;
  int variantToAssemble;

  friend std::ostream& operator<<(std::ostream& stream, Tile obj);
};

struct ModelVariant
{
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

  friend std::ostream& operator<<(std::ostream& stream, ModelVariant obj);
};


struct Animation
{
  int type;
};

struct spawn : public Animation
{
  int sourceID;
  int unitID;

  friend std::ostream& operator<<(std::ostream& stream, spawn obj);
};

struct repair : public Animation
{
  int actingID;
  int targetID;

  friend std::ostream& operator<<(std::ostream& stream, repair obj);
};

struct move : public Animation
{
  int actingID;
  int fromX;
  int fromY;
  int toX;
  int toY;

  friend std::ostream& operator<<(std::ostream& stream, move obj);
};

struct hack : public Animation
{
  int actingID;
  int targetID;

  friend std::ostream& operator<<(std::ostream& stream, hack obj);
};

struct orbitalDrop : public Animation
{
  int sourceID;

  friend std::ostream& operator<<(std::ostream& stream, orbitalDrop obj);
};

struct attack : public Animation
{
  int actingID;
  int targetID;

  friend std::ostream& operator<<(std::ostream& stream, attack obj);
};


struct AnimOwner: public Animation
{
  int owner;
};

struct GameState
{
  std::map<int,Player> players;
  std::map<int,Mappable> mappables;
  std::map<int,Droid> droids;
  std::map<int,Tile> tiles;
  std::map<int,ModelVariant> modelVariants;

  int mapWidth;
  int mapHeight;
  int turnNumber;
  int maxDroids;
  int playerID;
  int gameNumber;
  int scrapRate;
  int maxScrap;
  int dropTime;

  std::map< int, std::vector< SmartPointer< Animation > > > animations;
  friend std::ostream& operator<<(std::ostream& stream, GameState obj);
};

struct Game
{
  std::vector<GameState> states;
  std::string players[2];
  int winner;
	std::string winReason;

  Game();
};

} // parser

#endif
