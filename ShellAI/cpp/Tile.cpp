// -*-c++-*-

#include "Tile.h"
#include "game.h"


Tile::Tile(_Tile* pointer)
{
    ptr = (void*) pointer;
}

int Tile::id()
{
  return ((_Tile*)ptr)->id;
}

int Tile::x()
{
  return ((_Tile*)ptr)->x;
}

int Tile::y()
{
  return ((_Tile*)ptr)->y;
}

int Tile::owner()
{
  return ((_Tile*)ptr)->owner;
}

int Tile::turnsUntilAssembled()
{
  return ((_Tile*)ptr)->turnsUntilAssembled;
}

int Tile::variantToAssemble()
{
  return ((_Tile*)ptr)->variantToAssemble;
}




std::ostream& operator<<(std::ostream& stream,Tile ob)
{
  stream << "id: " << ((_Tile*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Tile*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Tile*)ob.ptr)->y  <<'\n';
  stream << "owner: " << ((_Tile*)ob.ptr)->owner  <<'\n';
  stream << "turnsUntilAssembled: " << ((_Tile*)ob.ptr)->turnsUntilAssembled  <<'\n';
  stream << "variantToAssemble: " << ((_Tile*)ob.ptr)->variantToAssemble  <<'\n';
  return stream;
}
