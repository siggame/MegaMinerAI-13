#ifndef GETTERS_H 
#define GETTERS_H
#include "structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

DLLEXPORT int playerGetId(_Player* ptr);
DLLEXPORT char* playerGetPlayerName(_Player* ptr);
DLLEXPORT float playerGetTime(_Player* ptr);
DLLEXPORT int playerGetScrapAmount(_Player* ptr);


DLLEXPORT int mappableGetId(_Mappable* ptr);
DLLEXPORT int mappableGetX(_Mappable* ptr);
DLLEXPORT int mappableGetY(_Mappable* ptr);


DLLEXPORT int droidGetId(_Droid* ptr);
DLLEXPORT int droidGetX(_Droid* ptr);
DLLEXPORT int droidGetY(_Droid* ptr);
DLLEXPORT int droidGetOwner(_Droid* ptr);
DLLEXPORT int droidGetVariant(_Droid* ptr);
DLLEXPORT int droidGetAttacksLeft(_Droid* ptr);
DLLEXPORT int droidGetMaxAttacks(_Droid* ptr);
DLLEXPORT int droidGetHealthLeft(_Droid* ptr);
DLLEXPORT int droidGetMaxHealth(_Droid* ptr);
DLLEXPORT int droidGetMovementLeft(_Droid* ptr);
DLLEXPORT int droidGetMaxMovement(_Droid* ptr);
DLLEXPORT int droidGetRange(_Droid* ptr);
DLLEXPORT int droidGetAttack(_Droid* ptr);
DLLEXPORT int droidGetArmor(_Droid* ptr);
DLLEXPORT int droidGetMaxArmor(_Droid* ptr);
DLLEXPORT int droidGetScrapWorth(_Droid* ptr);
DLLEXPORT int droidGetTurnsToBeHacked(_Droid* ptr);
DLLEXPORT int droidGetHackedTurnsLeft(_Droid* ptr);
DLLEXPORT int droidGetHackets(_Droid* ptr);
DLLEXPORT int droidGetHacketsMax(_Droid* ptr);


DLLEXPORT int tileGetId(_Tile* ptr);
DLLEXPORT int tileGetX(_Tile* ptr);
DLLEXPORT int tileGetY(_Tile* ptr);
DLLEXPORT int tileGetOwner(_Tile* ptr);
DLLEXPORT int tileGetTurnsUntilAssembled(_Tile* ptr);
DLLEXPORT int tileGetVariantToAssemble(_Tile* ptr);


DLLEXPORT int modelVariantGetId(_ModelVariant* ptr);
DLLEXPORT char* modelVariantGetName(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetVariant(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetCost(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetMaxAttacks(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetMaxHealth(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetMaxMovement(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetRange(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetAttack(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetMaxArmor(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetScrapWorth(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetTurnsToBeHacked(_ModelVariant* ptr);
DLLEXPORT int modelVariantGetHacketsMax(_ModelVariant* ptr);



#ifdef __cplusplus
}
#endif

#endif
