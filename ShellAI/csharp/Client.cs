using System;
using System.Runtime.InteropServices;

public class Client {
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern IntPtr createConnection();
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int serverConnect(IntPtr connection, string host, string port);

  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int serverLogin(IntPtr connection, string username, string password);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int createGame(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int joinGame(IntPtr connection, int id, string playerType);

  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern void endTurn(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern void getStatus(IntPtr connection);

  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int networkLoop(IntPtr connection);

#region Commands
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int playerTalk(IntPtr self, string message);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int playerOrbitalDrop(IntPtr self, int x, int y, int variant);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidMove(IntPtr self, int x, int y);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidOperate(IntPtr self, int x, int y);
#endregion

#region Accessors
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getMapWidth(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getMapHeight(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getTurnNumber(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getMaxDroids(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getPlayerID(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getGameNumber(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getScrapRate(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getMaxScrap(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getDropTime(IntPtr connection);

  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern IntPtr getPlayer(IntPtr connection, int num);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getPlayerCount(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern IntPtr getMappable(IntPtr connection, int num);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getMappableCount(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern IntPtr getDroid(IntPtr connection, int num);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getDroidCount(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern IntPtr getTile(IntPtr connection, int num);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getTileCount(IntPtr connection);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern IntPtr getModelVariant(IntPtr connection, int num);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int getModelVariantCount(IntPtr connection);
#endregion

#region Getters
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int playerGetId(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern IntPtr playerGetPlayerName(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern float playerGetTime(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int playerGetScrapAmount(IntPtr ptr);

  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int mappableGetId(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int mappableGetX(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int mappableGetY(IntPtr ptr);

  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetId(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetX(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetY(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetOwner(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetVariant(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetAttacksLeft(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetMaxAttacks(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetHealthLeft(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetMaxHealth(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetMovementLeft(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetMaxMovement(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetRange(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetAttack(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetArmor(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetMaxArmor(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetScrapWorth(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetTurnsToBeHacked(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetHackedTurnsLeft(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetHackets(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int droidGetHacketsMax(IntPtr ptr);

  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int tileGetId(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int tileGetX(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int tileGetY(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int tileGetOwner(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int tileGetTurnsUntilAssembled(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int tileGetVariantToAssemble(IntPtr ptr);

  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetId(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern IntPtr modelVariantGetName(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetVariant(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetCost(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetMaxAttacks(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetMaxHealth(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetMaxMovement(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetRange(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetAttack(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetMaxArmor(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetScrapWorth(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetTurnsToBeHacked(IntPtr ptr);
  [DllImport("client", CallingConvention=CallingConvention.Cdecl)]
  public static extern int modelVariantGetHacketsMax(IntPtr ptr);

#endregion

#region Properties
#endregion
}
