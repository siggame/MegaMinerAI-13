import com.sun.jna.Pointer;

///Represents a single tile on the map.
class Tile extends Mappable
{
  public Tile(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.tiles.length; i++)
    {
      if(BaseAI.tiles[i].ID == ID)
      {
        ptr = BaseAI.tiles[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

    //commands

  ///Attempt to assemble a Droid at this location.
  boolean assemble(int type)
  {
    validify();
    return (Client.INSTANCE.tileAssemble(ptr, type) == 0) ? false : true;
  }

    //getters

  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.tileGetId(ptr);
  }
  ///X position of the object
  public int getX()
  {
    validify();
    return Client.INSTANCE.tileGetX(ptr);
  }
  ///Y position of the object
  public int getY()
  {
    validify();
    return Client.INSTANCE.tileGetY(ptr);
  }
  ///The owner of the tile. If 0: Player 1; If 1: Player 2; 
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.tileGetOwner(ptr);
  }
  ///The number of turns until a structure is assembled.
  public int getTurnsUntilAssembled()
  {
    validify();
    return Client.INSTANCE.tileGetTurnsUntilAssembled(ptr);
  }
  ///The type of structure to assemble. If 0: Wall. If 1: Turret
  public int getTypeToAssemble()
  {
    validify();
    return Client.INSTANCE.tileGetTypeToAssemble(ptr);
  }
  ///The health of the Hangar or Wall on this tile.
  public int getHealth()
  {
    validify();
    return Client.INSTANCE.tileGetHealth(ptr);
  }

}
