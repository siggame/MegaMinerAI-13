// -*-c++-*-

#include "ModelVariant.h"
#include "game.h"


ModelVariant::ModelVariant(_ModelVariant* pointer)
{
    ptr = (void*) pointer;
}

int ModelVariant::id()
{
  return ((_ModelVariant*)ptr)->id;
}

char* ModelVariant::name()
{
  return ((_ModelVariant*)ptr)->name;
}

int ModelVariant::variant()
{
  return ((_ModelVariant*)ptr)->variant;
}

int ModelVariant::cost()
{
  return ((_ModelVariant*)ptr)->cost;
}

int ModelVariant::maxAttacks()
{
  return ((_ModelVariant*)ptr)->maxAttacks;
}

int ModelVariant::maxHealth()
{
  return ((_ModelVariant*)ptr)->maxHealth;
}

int ModelVariant::maxMovement()
{
  return ((_ModelVariant*)ptr)->maxMovement;
}

int ModelVariant::range()
{
  return ((_ModelVariant*)ptr)->range;
}

int ModelVariant::attack()
{
  return ((_ModelVariant*)ptr)->attack;
}

int ModelVariant::maxArmor()
{
  return ((_ModelVariant*)ptr)->maxArmor;
}

int ModelVariant::scrapWorth()
{
  return ((_ModelVariant*)ptr)->scrapWorth;
}

int ModelVariant::turnsToBeHacked()
{
  return ((_ModelVariant*)ptr)->turnsToBeHacked;
}

int ModelVariant::hacketsMax()
{
  return ((_ModelVariant*)ptr)->hacketsMax;
}




std::ostream& operator<<(std::ostream& stream,ModelVariant ob)
{
  stream << "id: " << ((_ModelVariant*)ob.ptr)->id  <<'\n';
  stream << "name: " << ((_ModelVariant*)ob.ptr)->name  <<'\n';
  stream << "variant: " << ((_ModelVariant*)ob.ptr)->variant  <<'\n';
  stream << "cost: " << ((_ModelVariant*)ob.ptr)->cost  <<'\n';
  stream << "maxAttacks: " << ((_ModelVariant*)ob.ptr)->maxAttacks  <<'\n';
  stream << "maxHealth: " << ((_ModelVariant*)ob.ptr)->maxHealth  <<'\n';
  stream << "maxMovement: " << ((_ModelVariant*)ob.ptr)->maxMovement  <<'\n';
  stream << "range: " << ((_ModelVariant*)ob.ptr)->range  <<'\n';
  stream << "attack: " << ((_ModelVariant*)ob.ptr)->attack  <<'\n';
  stream << "maxArmor: " << ((_ModelVariant*)ob.ptr)->maxArmor  <<'\n';
  stream << "scrapWorth: " << ((_ModelVariant*)ob.ptr)->scrapWorth  <<'\n';
  stream << "turnsToBeHacked: " << ((_ModelVariant*)ob.ptr)->turnsToBeHacked  <<'\n';
  stream << "hacketsMax: " << ((_ModelVariant*)ob.ptr)->hacketsMax  <<'\n';
  return stream;
}
