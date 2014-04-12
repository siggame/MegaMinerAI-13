using System;
using System.Runtime.InteropServices;

/// <summary>
/// A mappable object!
/// </summary>
public class Mappable
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;

  public Mappable()
  {
  }

  public Mappable(IntPtr p)
  {
    ptr = p;
    ID = Client.mappableGetId(ptr);
    iteration = BaseAI.iteration;
  }

  virtual public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.mappables.Length; i++)
    {
      if(BaseAI.mappables[i].ID == ID)
      {
        ptr = BaseAI.mappables[i].ptr;
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
  public int Id
  {
    get
    {
      validify();
      int value = Client.mappableGetId(ptr);
      return value;
    }
  }

  /// <summary>
  /// X position of the object
  /// </summary>
  public int X
  {
    get
    {
      validify();
      int value = Client.mappableGetX(ptr);
      return value;
    }
  }

  /// <summary>
  /// Y position of the object
  /// </summary>
  public int Y
  {
    get
    {
      validify();
      int value = Client.mappableGetY(ptr);
      return value;
    }
  }

  #endregion

  #region Properties
  #endregion
}
