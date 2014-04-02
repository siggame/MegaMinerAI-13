#include "getters.h"

DLLEXPORT int playerGetId(_Player* ptr)
{
  return ptr->id;
}
DLLEXPORT char* playerGetPlayerName(_Player* ptr)
{
  return ptr->playerName;
}
DLLEXPORT float playerGetTime(_Player* ptr)
{
  return ptr->time;
}
DLLEXPORT int playerGetScrapAmount(_Player* ptr)
{
  return ptr->scrapAmount;
}
DLLEXPORT int mappableGetId(_Mappable* ptr)
{
  return ptr->id;
}
DLLEXPORT int mappableGetX(_Mappable* ptr)
{
  return ptr->x;
}
DLLEXPORT int mappableGetY(_Mappable* ptr)
{
  return ptr->y;
}
DLLEXPORT int droidGetId(_Droid* ptr)
{
  return ptr->id;
}
DLLEXPORT int droidGetX(_Droid* ptr)
{
  return ptr->x;
}
DLLEXPORT int droidGetY(_Droid* ptr)
{
  return ptr->y;
}
DLLEXPORT int droidGetOwner(_Droid* ptr)
{
  return ptr->owner;
}
DLLEXPORT int droidGetVariant(_Droid* ptr)
{
  return ptr->variant;
}
DLLEXPORT int droidGetAttacksLeft(_Droid* ptr)
{
  return ptr->attacksLeft;
}
DLLEXPORT int droidGetMaxAttacks(_Droid* ptr)
{
  return ptr->maxAttacks;
}
DLLEXPORT int droidGetHealthLeft(_Droid* ptr)
{
  return ptr->healthLeft;
}
DLLEXPORT int droidGetMaxHealth(_Droid* ptr)
{
  return ptr->maxHealth;
}
DLLEXPORT int droidGetMovementLeft(_Droid* ptr)
{
  return ptr->movementLeft;
}
DLLEXPORT int droidGetMaxMovement(_Droid* ptr)
{
  return ptr->maxMovement;
}
DLLEXPORT int droidGetRange(_Droid* ptr)
{
  return ptr->range;
}
DLLEXPORT int droidGetAttack(_Droid* ptr)
{
  return ptr->attack;
}
DLLEXPORT int droidGetArmor(_Droid* ptr)
{
  return ptr->armor;
}
DLLEXPORT int droidGetMaxArmor(_Droid* ptr)
{
  return ptr->maxArmor;
}
DLLEXPORT int droidGetScrapWorth(_Droid* ptr)
{
  return ptr->scrapWorth;
}
DLLEXPORT int droidGetTurnsToBeHacked(_Droid* ptr)
{
  return ptr->turnsToBeHacked;
}
DLLEXPORT int droidGetHackedTurnsLeft(_Droid* ptr)
{
  return ptr->hackedTurnsLeft;
}
DLLEXPORT int droidGetHackets(_Droid* ptr)
{
  return ptr->hackets;
}
DLLEXPORT int droidGetHacketsMax(_Droid* ptr)
{
  return ptr->hacketsMax;
}
DLLEXPORT int tileGetId(_Tile* ptr)
{
  return ptr->id;
}
DLLEXPORT int tileGetX(_Tile* ptr)
{
  return ptr->x;
}
DLLEXPORT int tileGetY(_Tile* ptr)
{
  return ptr->y;
}
DLLEXPORT int tileGetOwner(_Tile* ptr)
{
  return ptr->owner;
}
DLLEXPORT int tileGetTurnsUntilAssembled(_Tile* ptr)
{
  return ptr->turnsUntilAssembled;
}
DLLEXPORT int tileGetVariantToAssemble(_Tile* ptr)
{
  return ptr->variantToAssemble;
}
DLLEXPORT int modelVariantGetId(_ModelVariant* ptr)
{
  return ptr->id;
}
DLLEXPORT char* modelVariantGetName(_ModelVariant* ptr)
{
  return ptr->name;
}
DLLEXPORT int modelVariantGetVariant(_ModelVariant* ptr)
{
  return ptr->variant;
}
DLLEXPORT int modelVariantGetCost(_ModelVariant* ptr)
{
  return ptr->cost;
}
DLLEXPORT int modelVariantGetMaxAttacks(_ModelVariant* ptr)
{
  return ptr->maxAttacks;
}
DLLEXPORT int modelVariantGetMaxHealth(_ModelVariant* ptr)
{
  return ptr->maxHealth;
}
DLLEXPORT int modelVariantGetMaxMovement(_ModelVariant* ptr)
{
  return ptr->maxMovement;
}
DLLEXPORT int modelVariantGetRange(_ModelVariant* ptr)
{
  return ptr->range;
}
DLLEXPORT int modelVariantGetAttack(_ModelVariant* ptr)
{
  return ptr->attack;
}
DLLEXPORT int modelVariantGetMaxArmor(_ModelVariant* ptr)
{
  return ptr->maxArmor;
}
DLLEXPORT int modelVariantGetScrapWorth(_ModelVariant* ptr)
{
  return ptr->scrapWorth;
}
DLLEXPORT int modelVariantGetTurnsToBeHacked(_ModelVariant* ptr)
{
  return ptr->turnsToBeHacked;
}
DLLEXPORT int modelVariantGetHacketsMax(_ModelVariant* ptr)
{
  return ptr->hacketsMax;
}

