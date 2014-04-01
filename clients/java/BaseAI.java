import com.sun.jna.Pointer;

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of builer-plate code out of the way
///The provided AI class does just that.
public abstract class BaseAI
{
  static Player[] players;
  static Mappable[] mappables;
  static Droid[] droids;
  static Tile[] tiles;
  static ModelVariant[] modelVariants;
  Pointer connection;
  static int iteration;
  boolean initialized;

  public BaseAI(Pointer c)
  {
    connection = c;
  }
    
  ///
  ///Make this your username, which should be provided.
  public abstract String username();
  ///
  ///Make this your password, which should be provided.
  public abstract String password();
  ///
  ///This is run on turn 1 before run
  public abstract void init();
  ///
  ///This is run every turn . Return true to end the turn, return false
  ///to request a status update from the server and then immediately rerun this function with the
  ///latest game status.
  public abstract boolean run();

  ///
  ///This is run on after your last turn.
  public abstract void end();


  public boolean startTurn()
  {
    iteration++;
    int count = 0;
    count = Client.INSTANCE.getPlayerCount(connection);
    players = new Player[count];
    for(int i = 0; i < count; i++)
    {
      players[i] = new Player(Client.INSTANCE.getPlayer(connection, i));
    }
    count = Client.INSTANCE.getMappableCount(connection);
    mappables = new Mappable[count];
    for(int i = 0; i < count; i++)
    {
      mappables[i] = new Mappable(Client.INSTANCE.getMappable(connection, i));
    }
    count = Client.INSTANCE.getDroidCount(connection);
    droids = new Droid[count];
    for(int i = 0; i < count; i++)
    {
      droids[i] = new Droid(Client.INSTANCE.getDroid(connection, i));
    }
    count = Client.INSTANCE.getTileCount(connection);
    tiles = new Tile[count];
    for(int i = 0; i < count; i++)
    {
      tiles[i] = new Tile(Client.INSTANCE.getTile(connection, i));
    }
    count = Client.INSTANCE.getModelVariantCount(connection);
    modelVariants = new ModelVariant[count];
    for(int i = 0; i < count; i++)
    {
      modelVariants[i] = new ModelVariant(Client.INSTANCE.getModelVariant(connection, i));
    }

    if(!initialized)
    {
      initialized = true;
      init();
    }
    return run();
  }


  ///The width of the total map.
  int mapWidth()
  {
    return Client.INSTANCE.getMapWidth(connection);
  }
  ///The height of the total map.
  int mapHeight()
  {
    return Client.INSTANCE.getMapHeight(connection);
  }
  ///The current turn number.
  int turnNumber()
  {
    return Client.INSTANCE.getTurnNumber(connection);
  }
  ///The maximum number of Droids allowed per player.
  int maxDroids()
  {
    return Client.INSTANCE.getMaxDroids(connection);
  }
  ///The id of the current player.
  int playerID()
  {
    return Client.INSTANCE.getPlayerID(connection);
  }
  ///What number game this is for the server.
  int gameNumber()
  {
    return Client.INSTANCE.getGameNumber(connection);
  }
  ///The rate a player receives scrap per turn.
  int scrapRate()
  {
    return Client.INSTANCE.getScrapRate(connection);
  }
  ///The maximum amount of scrap a player can have at once.
  int maxScrap()
  {
    return Client.INSTANCE.getMaxScrap(connection);
  }
  ///The amount of turns it takes to orbitally drop per tile away from the player's respective edge.
  int dropTime()
  {
    return Client.INSTANCE.getDropTime(connection);
  }
}
