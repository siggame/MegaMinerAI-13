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
  ///Owner of spawning droid. 0 - Player 1, 1 - Player 2, 2 - No spawning droid.
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.tileGetOwner(ptr);
  }
  ///The number of turns until a Droid is assembled.
  public int getTurnsUntilAssembled()
  {
    validify();
    return Client.INSTANCE.tileGetTurnsUntilAssembled(ptr);
  }
  ///The variant of Droid to assemble.
  public int getVariantToAssemble()
  {
    validify();
    return Client.INSTANCE.tileGetVariantToAssemble(ptr);
  }

}
