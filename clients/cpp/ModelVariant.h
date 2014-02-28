// -*-c++-*-

#ifndef MODELVARIANT_H
#define MODELVARIANT_H

#include <iostream>
#include "structures.h"


///Represents Variant of Droid.
class ModelVariant {
  public:
  void* ptr;
  ModelVariant(_ModelVariant* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The name of this variant of Droid.
  char* name();
  ///The ModelVariant specific id representing this variant of Droid.
  int variant();
  ///The scrap cost to spawn this Droid variant into the game.
  int cost();
  ///The maximum number of times the Droid can attack.
  int maxAttacks();
  ///The maximum amount of this health this Droid can have
  int maxHealth();
  ///The maximum number of moves this Droid can move.
  int maxMovement();
  ///The range of this Droid's attack.
  int range();
  ///The power of this Droid variant's attack.
  int attack();
  ///How much armor the Droid has which reduces damage taken.
  int maxArmor();
  ///The amount of scrap the Droid drops.
  int scrapWorth();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, ModelVariant ob);
};

#endif

