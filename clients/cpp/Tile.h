// -*-c++-*-

#ifndef TILE_H
#define TILE_H

#include <iostream>
#include "structures.h"

#include "Mappable.h"

///Represents a single tile on the map.
class Tile : public Mappable {
  public:
  Tile(_Tile* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///X position of the object
  int x();
  ///Y position of the object
  int y();
  ///Owner of spawning droid. 0 - Player 1, 1 - Player 2, 2 - No spawning droid.
  int owner();
  ///The number of turns until a Droid is assembled.
  int turnsUntilAssembled();
  ///The variant of Droid to assemble.
  int variantToAssemble();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Tile ob);
};

#endif

