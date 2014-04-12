import com.sun.jna.Pointer;

///Represents Variant of Droid.
class ModelVariant
{
  Pointer ptr;
  int ID;
  int iteration;
  public ModelVariant(Pointer p)
  {
    ptr = p;
    ID = Client.INSTANCE.modelVariantGetId(ptr);
    iteration = BaseAI.iteration;
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.modelVariants.length; i++)
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

    //commands


    //getters

  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.modelVariantGetId(ptr);
  }
  ///The name of this variant of Droid.
  public String getName()
  {
    validify();
    return Client.INSTANCE.modelVariantGetName(ptr);
  }
  ///The ModelVariant specific id representing this variant of Droid.
  public int getVariant()
  {
    validify();
    return Client.INSTANCE.modelVariantGetVariant(ptr);
  }
  ///The scrap cost to spawn this Droid variant into the game.
  public int getCost()
  {
    validify();
    return Client.INSTANCE.modelVariantGetCost(ptr);
  }
  ///The maximum number of times the Droid can attack.
  public int getMaxAttacks()
  {
    validify();
    return Client.INSTANCE.modelVariantGetMaxAttacks(ptr);
  }
  ///The maximum amount of this health this Droid can have
  public int getMaxHealth()
  {
    validify();
    return Client.INSTANCE.modelVariantGetMaxHealth(ptr);
  }
  ///The maximum number of moves this Droid can move.
  public int getMaxMovement()
  {
    validify();
    return Client.INSTANCE.modelVariantGetMaxMovement(ptr);
  }
  ///The range of this Droid's attack.
  public int getRange()
  {
    validify();
    return Client.INSTANCE.modelVariantGetRange(ptr);
  }
  ///The power of this Droid variant's attack.
  public int getAttack()
  {
    validify();
    return Client.INSTANCE.modelVariantGetAttack(ptr);
  }
  ///How much armor the Droid has which reduces damage taken.
  public int getMaxArmor()
  {
    validify();
    return Client.INSTANCE.modelVariantGetMaxArmor(ptr);
  }
  ///The amount of scrap the Droid drops.
  public int getScrapWorth()
  {
    validify();
    return Client.INSTANCE.modelVariantGetScrapWorth(ptr);
  }
  ///The number of turns this unit will be hacked, if it is hacked. If 0, the droid cannot be hacked.
  public int getTurnsToBeHacked()
  {
    validify();
    return Client.INSTANCE.modelVariantGetTurnsToBeHacked(ptr);
  }
  ///The maximum number of hackets that can be sustained before hacked. If 0, the Droid cannot be hacked.
  public int getHacketsMax()
  {
    validify();
    return Client.INSTANCE.modelVariantGetHacketsMax(ptr);
  }

}
