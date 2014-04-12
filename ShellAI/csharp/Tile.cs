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
  /// Owner of spawning droid. 0 - Player 1, 1 - Player 2, 2 - No spawning droid.
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
  /// The number of turns until a Droid is assembled.
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
  /// The variant of Droid to assemble.
  /// </summary>
  public int VariantToAssemble
  {
    get
    {
      validify();
      int value = Client.tileGetVariantToAssemble(ptr);
      return value;
    }
  }

  #endregion

  #region Properties
  #endregion
}
