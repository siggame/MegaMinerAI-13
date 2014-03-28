// -*-c++-*-

#include "Droid.h"
#include "game.h"


Droid::Droid(_Droid* pointer)
{
    ptr = (void*) pointer;
}

int Droid::id()
{
  return ((_Droid*)ptr)->id;
}

int Droid::x()
{
  return ((_Droid*)ptr)->x;
}

int Droid::y()
{
  return ((_Droid*)ptr)->y;
}

int Droid::owner()
{
  return ((_Droid*)ptr)->owner;
}

int Droid::variant()
{
  return ((_Droid*)ptr)->variant;
}

int Droid::attacksLeft()
{
  return ((_Droid*)ptr)->attacksLeft;
}

int Droid::maxAttacks()
{
  return ((_Droid*)ptr)->maxAttacks;
}

int Droid::healthLeft()
{
  return ((_Droid*)ptr)->healthLeft;
}

int Droid::maxHealth()
{
  return ((_Droid*)ptr)->maxHealth;
}

int Droid::movementLeft()
{
  return ((_Droid*)ptr)->movementLeft;
}

int Droid::maxMovement()
{
  return ((_Droid*)ptr)->maxMovement;
}

int Droid::range()
{
  return ((_Droid*)ptr)->range;
}

int Droid::attack()
{
  return ((_Droid*)ptr)->attack;
}

int Droid::armor()
{
  return ((_Droid*)ptr)->armor;
}

int Droid::maxArmor()
{
  return ((_Droid*)ptr)->maxArmor;
}

int Droid::scrapWorth()
{
  return ((_Droid*)ptr)->scrapWorth;
}

int Droid::turnsToBeHacked()
{
  return ((_Droid*)ptr)->turnsToBeHacked;
}

int Droid::hackedTurnsLeft()
{
  return ((_Droid*)ptr)->hackedTurnsLeft;
}

int Droid::hackets()
{
  return ((_Droid*)ptr)->hackets;
}

int Droid::hacketsMax()
{
  return ((_Droid*)ptr)->hacketsMax;
}


bool Droid::move(int x, int y)
{
  return droidMove( (_Droid*)ptr, x, y);
}

bool Droid::operate(int x, int y)
{
  return droidOperate( (_Droid*)ptr, x, y);
}



std::ostream& operator<<(std::ostream& stream,Droid ob)
{
  stream << "id: " << ((_Droid*)ob.ptr)->id  <<'\n';
  stream << "x: " << ((_Droid*)ob.ptr)->x  <<'\n';
  stream << "y: " << ((_Droid*)ob.ptr)->y  <<'\n';
  stream << "owner: " << ((_Droid*)ob.ptr)->owner  <<'\n';
  stream << "variant: " << ((_Droid*)ob.ptr)->variant  <<'\n';
  stream << "attacksLeft: " << ((_Droid*)ob.ptr)->attacksLeft  <<'\n';
  stream << "maxAttacks: " << ((_Droid*)ob.ptr)->maxAttacks  <<'\n';
  stream << "healthLeft: " << ((_Droid*)ob.ptr)->healthLeft  <<'\n';
  stream << "maxHealth: " << ((_Droid*)ob.ptr)->maxHealth  <<'\n';
  stream << "movementLeft: " << ((_Droid*)ob.ptr)->movementLeft  <<'\n';
  stream << "maxMovement: " << ((_Droid*)ob.ptr)->maxMovement  <<'\n';
  stream << "range: " << ((_Droid*)ob.ptr)->range  <<'\n';
  stream << "attack: " << ((_Droid*)ob.ptr)->attack  <<'\n';
  stream << "armor: " << ((_Droid*)ob.ptr)->armor  <<'\n';
  stream << "maxArmor: " << ((_Droid*)ob.ptr)->maxArmor  <<'\n';
  stream << "scrapWorth: " << ((_Droid*)ob.ptr)->scrapWorth  <<'\n';
  stream << "turnsToBeHacked: " << ((_Droid*)ob.ptr)->turnsToBeHacked  <<'\n';
  stream << "hackedTurnsLeft: " << ((_Droid*)ob.ptr)->hackedTurnsLeft  <<'\n';
  stream << "hackets: " << ((_Droid*)ob.ptr)->hackets  <<'\n';
  stream << "hacketsMax: " << ((_Droid*)ob.ptr)->hacketsMax  <<'\n';
  return stream;
}
