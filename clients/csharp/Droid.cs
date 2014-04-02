using System;
using System.Runtime.InteropServices;

/// <summary>
/// Represents a single Droid on the map.
/// </summary>
public class Droid: Mappable
{

  public Droid()
  {
  }

  public Droid(IntPtr p)
  {
    ptr = p;
    ID = Client.droidGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public override bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.droids.Length; i++)
    {
      if(BaseAI.droids[i].ID == ID)
      {
        ptr = BaseAI.droids[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }

  #region Commands
  /// <summary>
  /// Make the Droid move to the respective x and y location.
  /// </summary>
  public bool move(int x, int y)
  {
    validify();
    return (Client.droidMove(ptr, x, y) == 0) ? false : true;
  }
  /// <summary>
  /// Command to operate (repair, attack, hack) on another Droid.
  /// </summary>
  public bool operate(int x, int y)
  {
    validify();
    return (Client.droidOperate(ptr, x, y) == 0) ? false : true;
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
      int value = Client.droidGetId(ptr);
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
      int value = Client.droidGetX(ptr);
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
      int value = Client.droidGetY(ptr);
      return value;
    }
  }

  /// <summary>
  /// The owner of this Droid.
  /// </summary>
  public int Owner
  {
    get
    {
      validify();
      int value = Client.droidGetOwner(ptr);
      return value;
    }
  }

  /// <summary>
  /// The variant of this Droid. This variant refers to list of ModelVariants.
  /// </summary>
  public int Variant
  {
    get
    {
      validify();
      int value = Client.droidGetVariant(ptr);
      return value;
    }
  }

  /// <summary>
  /// The number of attacks the Droid has remaining.
  /// </summary>
  public int AttacksLeft
  {
    get
    {
      validify();
      int value = Client.droidGetAttacksLeft(ptr);
      return value;
    }
  }

  /// <summary>
  /// The maximum number of times the Droid can attack.
  /// </summary>
  public int MaxAttacks
  {
    get
    {
      validify();
      int value = Client.droidGetMaxAttacks(ptr);
      return value;
    }
  }

  /// <summary>
  /// The current amount health this Droid has remaining.
  /// </summary>
  public int HealthLeft
  {
    get
    {
      validify();
      int value = Client.droidGetHealthLeft(ptr);
      return value;
    }
  }

  /// <summary>
  /// The maximum amount of this health this Droid can have
  /// </summary>
  public int MaxHealth
  {
    get
    {
      validify();
      int value = Client.droidGetMaxHealth(ptr);
      return value;
    }
  }

  /// <summary>
  /// The number of moves this Droid has remaining.
  /// </summary>
  public int MovementLeft
  {
    get
    {
      validify();
      int value = Client.droidGetMovementLeft(ptr);
      return value;
    }
  }

  /// <summary>
  /// The maximum number of moves this Droid can move.
  /// </summary>
  public int MaxMovement
  {
    get
    {
      validify();
      int value = Client.droidGetMaxMovement(ptr);
      return value;
    }
  }

  /// <summary>
  /// The range of this Droid's attack.
  /// </summary>
  public int Range
  {
    get
    {
      validify();
      int value = Client.droidGetRange(ptr);
      return value;
    }
  }

  /// <summary>
  /// The power of this Droid variant's attack.
  /// </summary>
  public int Attack
  {
    get
    {
      validify();
      int value = Client.droidGetAttack(ptr);
      return value;
    }
  }

  /// <summary>
  /// How much armor the Droid has which reduces damage taken.
  /// </summary>
  public int Armor
  {
    get
    {
      validify();
      int value = Client.droidGetArmor(ptr);
      return value;
    }
  }

  /// <summary>
  /// How much armor the Droid has which reduces damage taken.
  /// </summary>
  public int MaxArmor
  {
    get
    {
      validify();
      int value = Client.droidGetMaxArmor(ptr);
      return value;
    }
  }

  /// <summary>
  /// The amount of scrap the Droid drops.
  /// </summary>
  public int ScrapWorth
  {
    get
    {
      validify();
      int value = Client.droidGetScrapWorth(ptr);
      return value;
    }
  }

  /// <summary>
  /// The number of turns this unit will be hacked, if it is hacked. If 0, the droid cannot be hacked.
  /// </summary>
  public int TurnsToBeHacked
  {
    get
    {
      validify();
      int value = Client.droidGetTurnsToBeHacked(ptr);
      return value;
    }
  }

  /// <summary>
  /// The number of turns the Droid has remaining as hacked.
  /// </summary>
  public int HackedTurnsLeft
  {
    get
    {
      validify();
      int value = Client.droidGetHackedTurnsLeft(ptr);
      return value;
    }
  }

  /// <summary>
  /// The amount of hacking progress that has been made.
  /// </summary>
  public int Hackets
  {
    get
    {
      validify();
      int value = Client.droidGetHackets(ptr);
      return value;
    }
  }

  /// <summary>
  /// The maximum number of hackets that can be sustained before hacked. If 0, the Droid cannot be hacked.
  /// </summary>
  public int HacketsMax
  {
    get
    {
      validify();
      int value = Client.droidGetHacketsMax(ptr);
      return value;
    }
  }

  #endregion

  #region Properties
  #endregion
}
