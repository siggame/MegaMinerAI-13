// -*-c++-*-

#ifndef TILE_H
#define TILE_H

#include <iostream>
#include "vc_structures.h"

#include "Mappable.h"

namespace client
{


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
  ///The owner of the tile. If 0: Player 1; If 1: Player 2; 
  int owner();
  ///The number of turns until a structure is assembled.
  int turnsUntilAssembled();
  ///The amount of scrap on this tile.
  int scrapAmount();
  ///The health of the Hangar or Wall on this tile.
  int health();

  // Actions
  ///Attempt to assemble a Droid at this location.
  int assemble(int type);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Tile ob);
};

}

#endif

