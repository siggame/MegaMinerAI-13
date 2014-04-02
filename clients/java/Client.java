import com.sun.jna.Library;
import com.sun.jna.Pointer;
import com.sun.jna.Native;

public interface Client extends Library {
  Client INSTANCE = (Client)Native.loadLibrary("client", Client.class);
  Pointer createConnection();
  boolean serverConnect(Pointer connection, String host, String port);

  boolean serverLogin(Pointer connection, String username, String password);
  int createGame(Pointer connection);
  int joinGame(Pointer connection, int id, String playerType);

  void endTurn(Pointer connection);
  void getStatus(Pointer connection);

  int networkLoop(Pointer connection);


    //commands
  int playerTalk(Pointer object, String message);
  int playerOrbitalDrop(Pointer object, int x, int y, int variant);
  int droidMove(Pointer object, int x, int y);
  int droidOperate(Pointer object, int x, int y);

    //accessors
  int getMapWidth(Pointer connection);
  int getMapHeight(Pointer connection);
  int getTurnNumber(Pointer connection);
  int getMaxDroids(Pointer connection);
  int getPlayerID(Pointer connection);
  int getGameNumber(Pointer connection);
  int getScrapRate(Pointer connection);
  int getMaxScrap(Pointer connection);
  int getDropTime(Pointer connection);

  Pointer getPlayer(Pointer connection, int num);
  int getPlayerCount(Pointer connection);
  Pointer getMappable(Pointer connection, int num);
  int getMappableCount(Pointer connection);
  Pointer getDroid(Pointer connection, int num);
  int getDroidCount(Pointer connection);
  Pointer getTile(Pointer connection, int num);
  int getTileCount(Pointer connection);
  Pointer getModelVariant(Pointer connection, int num);
  int getModelVariantCount(Pointer connection);


    //getters
  int playerGetId(Pointer ptr);
  String playerGetPlayerName(Pointer ptr);
  float playerGetTime(Pointer ptr);
  int playerGetScrapAmount(Pointer ptr);

  int mappableGetId(Pointer ptr);
  int mappableGetX(Pointer ptr);
  int mappableGetY(Pointer ptr);

  int droidGetId(Pointer ptr);
  int droidGetX(Pointer ptr);
  int droidGetY(Pointer ptr);
  int droidGetOwner(Pointer ptr);
  int droidGetVariant(Pointer ptr);
  int droidGetAttacksLeft(Pointer ptr);
  int droidGetMaxAttacks(Pointer ptr);
  int droidGetHealthLeft(Pointer ptr);
  int droidGetMaxHealth(Pointer ptr);
  int droidGetMovementLeft(Pointer ptr);
  int droidGetMaxMovement(Pointer ptr);
  int droidGetRange(Pointer ptr);
  int droidGetAttack(Pointer ptr);
  int droidGetArmor(Pointer ptr);
  int droidGetMaxArmor(Pointer ptr);
  int droidGetScrapWorth(Pointer ptr);
  int droidGetTurnsToBeHacked(Pointer ptr);
  int droidGetHackedTurnsLeft(Pointer ptr);
  int droidGetHackets(Pointer ptr);
  int droidGetHacketsMax(Pointer ptr);

  int tileGetId(Pointer ptr);
  int tileGetX(Pointer ptr);
  int tileGetY(Pointer ptr);
  int tileGetOwner(Pointer ptr);
  int tileGetTurnsUntilAssembled(Pointer ptr);
  int tileGetVariantToAssemble(Pointer ptr);

  int modelVariantGetId(Pointer ptr);
  String modelVariantGetName(Pointer ptr);
  int modelVariantGetVariant(Pointer ptr);
  int modelVariantGetCost(Pointer ptr);
  int modelVariantGetMaxAttacks(Pointer ptr);
  int modelVariantGetMaxHealth(Pointer ptr);
  int modelVariantGetMaxMovement(Pointer ptr);
  int modelVariantGetRange(Pointer ptr);
  int modelVariantGetAttack(Pointer ptr);
  int modelVariantGetMaxArmor(Pointer ptr);
  int modelVariantGetScrapWorth(Pointer ptr);
  int modelVariantGetTurnsToBeHacked(Pointer ptr);
  int modelVariantGetHacketsMax(Pointer ptr);


    //properties

}
