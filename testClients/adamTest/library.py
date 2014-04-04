# -*-python-*-

import os

from ctypes import *

try:
  if os.name == 'posix':
    library = CDLL("./libclient.so")
  elif os.name == 'nt':
    library = CDLL("./client.dll")
  else:
    raise Exception("Unrecognized OS: "+os.name)
except OSError:
  raise Exception("It looks like you didn't build libclient. Run 'make' and try again.")

# commands

library.createConnection.restype = c_void_p
library.createConnection.argtypes = []

library.serverConnect.restype = c_int
library.serverConnect.argtypes = [c_void_p, c_char_p, c_char_p]

library.serverLogin.restype = c_int
library.serverLogin.argtypes = [c_void_p, c_char_p, c_char_p]

library.createGame.restype = c_int
library.createGame.argtypes = [c_void_p]

library.joinGame.restype = c_int
library.joinGame.argtypes = [c_void_p, c_int, c_char_p]

library.endTurn.restype = None
library.endTurn.argtypes = [c_void_p]

library.getStatus.restype = None
library.getStatus.argtypes = [c_void_p]

library.networkLoop.restype = c_int
library.networkLoop.argtypes = [c_void_p]

#Functions
library.playerTalk.restype = c_int
library.playerTalk.argtypes = [c_void_p, c_char_p]

library.playerOrbitalDrop.restype = c_int
library.playerOrbitalDrop.argtypes = [c_void_p, c_int, c_int, c_int]

library.droidMove.restype = c_int
library.droidMove.argtypes = [c_void_p, c_int, c_int]

library.droidOperate.restype = c_int
library.droidOperate.argtypes = [c_void_p, c_int, c_int]

# accessors

#Globals
library.getMapWidth.restype = c_int
library.getMapWidth.argtypes = [c_void_p]

library.getMapHeight.restype = c_int
library.getMapHeight.argtypes = [c_void_p]

library.getTurnNumber.restype = c_int
library.getTurnNumber.argtypes = [c_void_p]

library.getMaxDroids.restype = c_int
library.getMaxDroids.argtypes = [c_void_p]

library.getPlayerID.restype = c_int
library.getPlayerID.argtypes = [c_void_p]

library.getGameNumber.restype = c_int
library.getGameNumber.argtypes = [c_void_p]

library.getScrapRate.restype = c_int
library.getScrapRate.argtypes = [c_void_p]

library.getMaxScrap.restype = c_int
library.getMaxScrap.argtypes = [c_void_p]

library.getDropTime.restype = c_int
library.getDropTime.argtypes = [c_void_p]

library.getPlayer.restype = c_void_p
library.getPlayer.argtypes = [c_void_p, c_int]

library.getPlayerCount.restype = c_int
library.getPlayerCount.argtypes = [c_void_p]

library.getMappable.restype = c_void_p
library.getMappable.argtypes = [c_void_p, c_int]

library.getMappableCount.restype = c_int
library.getMappableCount.argtypes = [c_void_p]

library.getDroid.restype = c_void_p
library.getDroid.argtypes = [c_void_p, c_int]

library.getDroidCount.restype = c_int
library.getDroidCount.argtypes = [c_void_p]

library.getTile.restype = c_void_p
library.getTile.argtypes = [c_void_p, c_int]

library.getTileCount.restype = c_int
library.getTileCount.argtypes = [c_void_p]

library.getModelVariant.restype = c_void_p
library.getModelVariant.argtypes = [c_void_p, c_int]

library.getModelVariantCount.restype = c_int
library.getModelVariantCount.argtypes = [c_void_p]

# getters

#Data
library.playerGetId.restype = c_int
library.playerGetId.argtypes = [c_void_p]

library.playerGetPlayerName.restype = c_char_p
library.playerGetPlayerName.argtypes = [c_void_p]

library.playerGetTime.restype = c_float
library.playerGetTime.argtypes = [c_void_p]

library.playerGetScrapAmount.restype = c_int
library.playerGetScrapAmount.argtypes = [c_void_p]

library.mappableGetId.restype = c_int
library.mappableGetId.argtypes = [c_void_p]

library.mappableGetX.restype = c_int
library.mappableGetX.argtypes = [c_void_p]

library.mappableGetY.restype = c_int
library.mappableGetY.argtypes = [c_void_p]

library.droidGetId.restype = c_int
library.droidGetId.argtypes = [c_void_p]

library.droidGetX.restype = c_int
library.droidGetX.argtypes = [c_void_p]

library.droidGetY.restype = c_int
library.droidGetY.argtypes = [c_void_p]

library.droidGetOwner.restype = c_int
library.droidGetOwner.argtypes = [c_void_p]

library.droidGetVariant.restype = c_int
library.droidGetVariant.argtypes = [c_void_p]

library.droidGetAttacksLeft.restype = c_int
library.droidGetAttacksLeft.argtypes = [c_void_p]

library.droidGetMaxAttacks.restype = c_int
library.droidGetMaxAttacks.argtypes = [c_void_p]

library.droidGetHealthLeft.restype = c_int
library.droidGetHealthLeft.argtypes = [c_void_p]

library.droidGetMaxHealth.restype = c_int
library.droidGetMaxHealth.argtypes = [c_void_p]

library.droidGetMovementLeft.restype = c_int
library.droidGetMovementLeft.argtypes = [c_void_p]

library.droidGetMaxMovement.restype = c_int
library.droidGetMaxMovement.argtypes = [c_void_p]

library.droidGetRange.restype = c_int
library.droidGetRange.argtypes = [c_void_p]

library.droidGetAttack.restype = c_int
library.droidGetAttack.argtypes = [c_void_p]

library.droidGetArmor.restype = c_int
library.droidGetArmor.argtypes = [c_void_p]

library.droidGetMaxArmor.restype = c_int
library.droidGetMaxArmor.argtypes = [c_void_p]

library.droidGetScrapWorth.restype = c_int
library.droidGetScrapWorth.argtypes = [c_void_p]

library.droidGetTurnsToBeHacked.restype = c_int
library.droidGetTurnsToBeHacked.argtypes = [c_void_p]

library.droidGetHackedTurnsLeft.restype = c_int
library.droidGetHackedTurnsLeft.argtypes = [c_void_p]

library.droidGetHackets.restype = c_int
library.droidGetHackets.argtypes = [c_void_p]

library.droidGetHacketsMax.restype = c_int
library.droidGetHacketsMax.argtypes = [c_void_p]

library.tileGetId.restype = c_int
library.tileGetId.argtypes = [c_void_p]

library.tileGetX.restype = c_int
library.tileGetX.argtypes = [c_void_p]

library.tileGetY.restype = c_int
library.tileGetY.argtypes = [c_void_p]

library.tileGetOwner.restype = c_int
library.tileGetOwner.argtypes = [c_void_p]

library.tileGetTurnsUntilAssembled.restype = c_int
library.tileGetTurnsUntilAssembled.argtypes = [c_void_p]

library.tileGetVariantToAssemble.restype = c_int
library.tileGetVariantToAssemble.argtypes = [c_void_p]

library.modelVariantGetId.restype = c_int
library.modelVariantGetId.argtypes = [c_void_p]

library.modelVariantGetName.restype = c_char_p
library.modelVariantGetName.argtypes = [c_void_p]

library.modelVariantGetVariant.restype = c_int
library.modelVariantGetVariant.argtypes = [c_void_p]

library.modelVariantGetCost.restype = c_int
library.modelVariantGetCost.argtypes = [c_void_p]

library.modelVariantGetMaxAttacks.restype = c_int
library.modelVariantGetMaxAttacks.argtypes = [c_void_p]

library.modelVariantGetMaxHealth.restype = c_int
library.modelVariantGetMaxHealth.argtypes = [c_void_p]

library.modelVariantGetMaxMovement.restype = c_int
library.modelVariantGetMaxMovement.argtypes = [c_void_p]

library.modelVariantGetRange.restype = c_int
library.modelVariantGetRange.argtypes = [c_void_p]

library.modelVariantGetAttack.restype = c_int
library.modelVariantGetAttack.argtypes = [c_void_p]

library.modelVariantGetMaxArmor.restype = c_int
library.modelVariantGetMaxArmor.argtypes = [c_void_p]

library.modelVariantGetScrapWorth.restype = c_int
library.modelVariantGetScrapWorth.argtypes = [c_void_p]

library.modelVariantGetTurnsToBeHacked.restype = c_int
library.modelVariantGetTurnsToBeHacked.argtypes = [c_void_p]

library.modelVariantGetHacketsMax.restype = c_int
library.modelVariantGetHacketsMax.argtypes = [c_void_p]


#Properties
