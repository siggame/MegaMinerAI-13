using System;
using System.Runtime.InteropServices;

/// <summary>
/// Represents a single tile on the map.
/// </summary>
public class Tile: Mappable
{

  public Tile()
  {
  }

  public Tile(IntPtr p)
  {
    ptr = p;
    ID = Client.tileGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.tiles.Length; i++)
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

  #region Commands
  /// <summary>
  /// Attempt to assemble a Droid at this location.
  /// </summary>
  public bool assemble(int type)
  {
    validify();
    return (Client.tileAssemble(ptr, type) == 0) ? false : true;
  }
  #endregion

  #region Getters
  /// <summary>
  /// Unique Identifier
  /// </summary>
  public new int Id
  {
    get
    {
      validify();
      int value = Client.tileGetId(ptr);
      return value;
    }
  }

  /// <summary>
  /// X position of the object
  /// </summary>
  public new int X
  {
    get
    {
      validify();
      int value = Client.tileGetX(ptr);
      return value;
    }
  }

  /// <summary>
  /// Y position of the object
  /// </summary>
  public new int Y
  {
    get
    {
      validify();
      int value = Client.tileGetY(ptr);
      return value;
    }
  }

  /// <summary>
  /// The owner of the tile. If 0: Player 1; If 1: Player 2; 
  /// </summary>
  public int Owner
  {
    get
    {
      validify();
      int value = Client.tileGetOwner(ptr);
      return value;
    }
  }

  /// <summary>
  /// The number of turns until a structure is assembled.
  /// </summary>
  public int TurnsUntilAssembled
  {
    get
    {
      validify();
      int value = Client.tileGetTurnsUntilAssembled(ptr);
      return value;
    }
  }

  /// <summary>
  /// The type of structure to assemble. If 0: Wall. If 1: Turret
  /// </summary>
  public int TypeToAssemble
  {
    get
    {
      validify();
      int value = Client.tileGetTypeToAssemble(ptr);
      return value;
    }
  }

  /// <summary>
  /// The health of the Hangar or Wall on this tile.
  /// </summary>
  public int Health
  {
    get
    {
      validify();
      int value = Client.tileGetHealth(ptr);
      return value;
    }
  }

  #endregion

  #region Properties
  #endregion
}
