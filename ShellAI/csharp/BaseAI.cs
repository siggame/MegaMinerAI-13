using System;
using System.Runtime.InteropServices;

/// <summary>
/// This class implements most the code an AI would need to interface with the lower-level game code.
/// AIs should extend this class to get a lot of builer-plate code out of the way. The provided AI class does just that.
/// </summary>
public abstract class BaseAI
{
  public static Player[] players;
  public static Mappable[] mappables;
  public static Droid[] droids;
  public static Tile[] tiles;
  public static ModelVariant[] modelVariants;

  IntPtr connection;
  public static int iteration;
  bool initialized;

  public BaseAI(IntPtr c)
  {
    connection = c;
  }

  /// <summary>
  /// Make this your username, which should be provided.
  /// </summary>
  /// <returns>Returns the username of the player.</returns>
  public abstract String username();

  /// <summary>
  /// Make this your password, which should be provided.
  /// </summary>
  /// <returns>Returns the password of the player.</returns>
  public abstract String password();

  /// <summary>
  /// This is run once on turn one before run().
  /// </summary>
  public abstract void init();

  /// <summary>
  /// This is run every turn.
  /// </summary>
  /// <returns>
  /// Return true to end turn, false to resynchronize with the 
  /// server and run again.
  /// </returns>
  public abstract bool run();

  /// <summary>
  /// This is run once after your last turn.
  /// </summary>
  public abstract void end();

  /// <summary>
  /// Synchronizes with the server, then calls run().
  /// </summary>
  /// <returns>
  /// Return true to end turn, false to resynchronize with the 
  /// server and run again.
  /// </returns>
  public bool startTurn()
  {
    int count = 0;
    iteration++;

    count = Client.getPlayerCount(connection);
    players = new Player[count];
    for(int i = 0; i < count; i++)
      players[i] = new Player(Client.getPlayer(connection, i));

    count = Client.getMappableCount(connection);
    mappables = new Mappable[count];
    for(int i = 0; i < count; i++)
      mappables[i] = new Mappable(Client.getMappable(connection, i));

    count = Client.getDroidCount(connection);
    droids = new Droid[count];
    for(int i = 0; i < count; i++)
      droids[i] = new Droid(Client.getDroid(connection, i));

    count = Client.getTileCount(connection);
    tiles = new Tile[count];
    for(int i = 0; i < count; i++)
      tiles[i] = new Tile(Client.getTile(connection, i));

    count = Client.getModelVariantCount(connection);
    modelVariants = new ModelVariant[count];
    for(int i = 0; i < count; i++)
      modelVariants[i] = new ModelVariant(Client.getModelVariant(connection, i));

    if(!initialized)
    {
      initialized = true;
      init();
    }

    return run();
  }

  /// <summary>
  /// The width of the total map.
  /// </summary>
  /// <returns>Returns the width of the total map.</returns>
  public int mapWidth()
  {
    int value = Client.getMapWidth(connection);
    return value;
  }

  /// <summary>
  /// The height of the total map.
  /// </summary>
  /// <returns>Returns the height of the total map.</returns>
  public int mapHeight()
  {
    int value = Client.getMapHeight(connection);
    return value;
  }

  /// <summary>
  /// The current turn number.
  /// </summary>
  /// <returns>Returns the current turn number.</returns>
  public int turnNumber()
  {
    int value = Client.getTurnNumber(connection);
    return value;
  }

  /// <summary>
  /// The maximum number of Droids allowed per player.
  /// </summary>
  /// <returns>Returns the maximum number of Droids allowed per player.</returns>
  public int maxDroids()
  {
    int value = Client.getMaxDroids(connection);
    return value;
  }

  /// <summary>
  /// The id of the current player.
  /// </summary>
  /// <returns>Returns the id of the current player.</returns>
  public int playerID()
  {
    int value = Client.getPlayerID(connection);
    return value;
  }

  /// <summary>
  /// What number game this is for the server.
  /// </summary>
  /// <returns>Returns what number game this is for the server.</returns>
  public int gameNumber()
  {
    int value = Client.getGameNumber(connection);
    return value;
  }

  /// <summary>
  /// The rate a player receives scrap per turn.
  /// </summary>
  /// <returns>Returns the rate a player receives scrap per turn.</returns>
  public int scrapRate()
  {
    int value = Client.getScrapRate(connection);
    return value;
  }

  /// <summary>
  /// The maximum amount of scrap a player can have at once.
  /// </summary>
  /// <returns>Returns the maximum amount of scrap a player can have at once.</returns>
  public int maxScrap()
  {
    int value = Client.getMaxScrap(connection);
    return value;
  }

  /// <summary>
  /// The amount of turns it takes to orbitally drop per tile away from the player's respective edge.
  /// </summary>
  /// <returns>Returns the amount of turns it takes to orbitally drop per tile away from the player's respective edge.</returns>
  public int dropTime()
  {
    int value = Client.getDropTime(connection);
    return value;
  }
}
