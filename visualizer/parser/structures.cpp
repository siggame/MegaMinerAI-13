// -*-c++-*-

#include "structures.h"

#include <iostream>

namespace parser
{


std::ostream& operator<<(std::ostream& stream, Player ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "playerName: " << ob.playerName  <<'\n';
  stream << "time: " << ob.time  <<'\n';
  stream << "scrapAmount: " << ob.scrapAmount  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Mappable ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Droid ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "variant: " << ob.variant  <<'\n';
  stream << "attacksLeft: " << ob.attacksLeft  <<'\n';
  stream << "maxAttacks: " << ob.maxAttacks  <<'\n';
  stream << "healthLeft: " << ob.healthLeft  <<'\n';
  stream << "maxHealth: " << ob.maxHealth  <<'\n';
  stream << "movementLeft: " << ob.movementLeft  <<'\n';
  stream << "maxMovement: " << ob.maxMovement  <<'\n';
  stream << "range: " << ob.range  <<'\n';
  stream << "attack: " << ob.attack  <<'\n';
  stream << "armor: " << ob.armor  <<'\n';
  stream << "maxArmor: " << ob.maxArmor  <<'\n';
  stream << "scrapWorth: " << ob.scrapWorth  <<'\n';
  stream << "hackedTurnsLeft: " << ob.hackedTurnsLeft  <<'\n';
  stream << "hackets: " << ob.hackets  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Tile ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "turnsUntilAssembled: " << ob.turnsUntilAssembled  <<'\n';
  stream << "scrapAmount: " << ob.scrapAmount  <<'\n';
  stream << "health: " << ob.health  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, ModelVariant ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "name: " << ob.name  <<'\n';
  stream << "variant: " << ob.variant  <<'\n';
  stream << "cost: " << ob.cost  <<'\n';
  stream << "maxAttacks: " << ob.maxAttacks  <<'\n';
  stream << "maxHealth: " << ob.maxHealth  <<'\n';
  stream << "maxMovement: " << ob.maxMovement  <<'\n';
  stream << "range: " << ob.range  <<'\n';
  stream << "attack: " << ob.attack  <<'\n';
  stream << "maxArmor: " << ob.maxArmor  <<'\n';
  stream << "scrapWorth: " << ob.scrapWorth  <<'\n';
  return stream;
}



std::ostream& operator<<(std::ostream& stream, move ob)
{
  stream << "move" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "fromX: " << ob.fromX  <<'\n';
  stream << "fromY: " << ob.fromY  <<'\n';
  stream << "toX: " << ob.toX  <<'\n';
  stream << "toY: " << ob.toY  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, attack ob)
{
  stream << "attack" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "targetID: " << ob.targetID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, spawn ob)
{
  stream << "spawn" << "\n";
  stream << "sourceID: " << ob.sourceID  <<'\n';
  stream << "unitID: " << ob.unitID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, hack ob)
{
  stream << "hack" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "targetID: " << ob.targetID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, orbitalDrop ob)
{
  stream << "orbitalDrop" << "\n";
  stream << "sourceID: " << ob.sourceID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, repair ob)
{
  stream << "repair" << "\n";
  stream << "actingID: " << ob.actingID  <<'\n';
  stream << "targetID: " << ob.targetID  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, GameState ob)
{
  stream << "mapWidth: " << ob.mapWidth  <<'\n';
  stream << "mapHeight: " << ob.mapHeight  <<'\n';
  stream << "turnNumber: " << ob.turnNumber  <<'\n';
  stream << "maxDroids: " << ob.maxDroids  <<'\n';
  stream << "maxWalls: " << ob.maxWalls  <<'\n';
  stream << "playerID: " << ob.playerID  <<'\n';
  stream << "gameNumber: " << ob.gameNumber  <<'\n';
  stream << "scrapRate: " << ob.scrapRate  <<'\n';
  stream << "maxScrap: " << ob.maxScrap  <<'\n';

  stream << "\n\nPlayers:\n";
  for(std::map<int,Player>::iterator i = ob.players.begin(); i != ob.players.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nMappables:\n";
  for(std::map<int,Mappable>::iterator i = ob.mappables.begin(); i != ob.mappables.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nDroids:\n";
  for(std::map<int,Droid>::iterator i = ob.droids.begin(); i != ob.droids.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nTiles:\n";
  for(std::map<int,Tile>::iterator i = ob.tiles.begin(); i != ob.tiles.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nModelVariants:\n";
  for(std::map<int,ModelVariant>::iterator i = ob.modelVariants.begin(); i != ob.modelVariants.end(); i++)
    stream << i->second << '\n';
  stream << "\nAnimation\n";
  for
    (
    std::map< int, std::vector< SmartPointer< Animation > > >::iterator j = ob.animations.begin(); 
    j != ob.animations.end(); 
    j++ 
    )
  {
  for(std::vector< SmartPointer< Animation > >::iterator i = j->second.begin(); i != j->second.end(); i++)
  {
//    if((*(*i)).type == MOVE)
//      stream << *((move*)*i) << "\n";
//    if((*(*i)).type == ATTACK)
//      stream << *((attack*)*i) << "\n";
//    if((*(*i)).type == SPAWN)
//      stream << *((spawn*)*i) << "\n";
//    if((*(*i)).type == HACK)
//      stream << *((hack*)*i) << "\n";
//    if((*(*i)).type == ORBITALDROP)
//      stream << *((orbitalDrop*)*i) << "\n";
//    if((*(*i)).type == REPAIR)
//      stream << *((repair*)*i) << "\n";
  }
  

  }
  return stream;
}

Game::Game()
{
  winner = -1;
}

} // parser
