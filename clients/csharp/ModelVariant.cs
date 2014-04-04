using System;
using System.Runtime.InteropServices;

/// <summary>
/// Represents Variant of Droid.
/// </summary>
public class ModelVariant
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;

  public ModelVariant()
  {
  }

  public ModelVariant(IntPtr p)
  {
    ptr = p;
    ID = Client.modelVariantGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.modelVariants.Length; i++)
    {
      if(BaseAI.modelVariants[i].ID == ID)
      {
        ptr = BaseAI.modelVariants[i].ptr;
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
      int value = Client.modelVariantGetId(ptr);
      return value;
    }
  }

  /// <summary>
  /// The name of this variant of Droid.
  /// </summary>
  public string Name
  {
    get
    {
      validify();
      IntPtr value = Client.modelVariantGetName(ptr);
      return Marshal.PtrToStringAuto(value);
    }
  }

  /// <summary>
  /// The ModelVariant specific id representing this variant of Droid.
  /// </summary>
  public int Variant
  {
    get
    {
      validify();
      int value = Client.modelVariantGetVariant(ptr);
      return value;
    }
  }

  /// <summary>
  /// The scrap cost to spawn this Droid variant into the game.
  /// </summary>
  public int Cost
  {
    get
    {
      validify();
      int value = Client.modelVariantGetCost(ptr);
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
      int value = Client.modelVariantGetMaxAttacks(ptr);
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
      int value = Client.modelVariantGetMaxHealth(ptr);
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
      int value = Client.modelVariantGetMaxMovement(ptr);
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
      int value = Client.modelVariantGetRange(ptr);
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
      int value = Client.modelVariantGetAttack(ptr);
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
      int value = Client.modelVariantGetMaxArmor(ptr);
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
      int value = Client.modelVariantGetScrapWorth(ptr);
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
      int value = Client.modelVariantGetTurnsToBeHacked(ptr);
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
      int value = Client.modelVariantGetHacketsMax(ptr);
      return value;
    }
  }

  #endregion

  #region Properties
  #endregion
}
