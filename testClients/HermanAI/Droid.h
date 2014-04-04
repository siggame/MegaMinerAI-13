// -*-c++-*-

#ifndef DROID_H
#define DROID_H

#include <iostream>
#include "structures.h"

#include "Mappable.h"

///Represents a single Droid on the map.
class Droid : public Mappable {
  public:
  Droid(_Droid* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///X position of the object
  int x();
  ///Y position of the object
  int y();
  ///The owner of this Droid.
  int owner();
  ///The variant of this Droid. This variant refers to list of ModelVariants.
  int variant();
  ///The number of attacks the Droid has remaining.
  int attacksLeft();
  ///The maximum number of times the Droid can attack.
  int maxAttacks();
  ///The current amount health this Droid has remaining.
  int healthLeft();
  ///The maximum amount of this health this Droid can have
  int maxHealth();
  ///The number of moves this Droid has remaining.
  int movementLeft();
  ///The maximum number of moves this Droid can move.
  int maxMovement();
  ///The range of this Droid's attack.
  int range();
  ///The power of this Droid variant's attack.
  int attack();
  ///How much armor the Droid has which reduces damage taken.
  int armor();
  ///How much armor the Droid has which reduces damage taken.
  int maxArmor();
  ///The amount of scrap the Droid drops.
  int scrapWorth();
  ///The number of turns this unit will be hacked, if it is hacked. If 0, the droid cannot be hacked.
  int turnsToBeHacked();
  ///The number of turns the Droid has remaining as hacked.
  int hackedTurnsLeft();
  ///The amount of hacking progress that has been made.
  int hackets();
  ///The maximum number of hackets that can be sustained before hacked. If 0, the Droid cannot be hacked.
  int hacketsMax();

  // Actions
  ///Make the Droid move to the respective x and y location.
  bool move(int x, int y);
  ///Command to operate (repair, attack, hack) on another Droid.
  bool operate(int x, int y);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Droid ob);
};

#endif

