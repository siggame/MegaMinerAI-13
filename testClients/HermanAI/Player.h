// -*-c++-*-

#ifndef PLAYER_H
#define PLAYER_H

#include <iostream>
#include "structures.h"


class Player {
  public:
  void* ptr;
  Player(_Player* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///Player's Name
  char* playerName();
  ///Time remaining, updated at start of turn
  float time();
  ///The amount of scrap you have in your Hangar.
  int scrapAmount();

  // Actions
  ///Allows a player to display messages on the screen
  bool talk(char* message);
  ///Allows a player to spawn a Droid.
  bool orbitalDrop(int x, int y, int variant);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Player ob);
};

#endif

