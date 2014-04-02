import com.sun.jna.Pointer;

///Represents a single Droid on the map.
class Droid extends Mappable
{
  public Droid(Pointer p)
  {
    super(p);
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.droids.length; i++)
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

    //commands

  ///Make the Droid move to the respective x and y location.
  boolean move(int x, int y)
  {
    validify();
    return (Client.INSTANCE.droidMove(ptr, x, y) == 0) ? false : true;
  }
  ///Command to operate (repair, attack, hack) on another Droid.
  boolean operate(int x, int y)
  {
    validify();
    return (Client.INSTANCE.droidOperate(ptr, x, y) == 0) ? false : true;
  }

    //getters

  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.droidGetId(ptr);
  }
  ///X position of the object
  public int getX()
  {
    validify();
    return Client.INSTANCE.droidGetX(ptr);
  }
  ///Y position of the object
  public int getY()
  {
    validify();
    return Client.INSTANCE.droidGetY(ptr);
  }
  ///The owner of this Droid.
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.droidGetOwner(ptr);
  }
  ///The variant of this Droid. This variant refers to list of ModelVariants.
  public int getVariant()
  {
    validify();
    return Client.INSTANCE.droidGetVariant(ptr);
  }
  ///The number of attacks the Droid has remaining.
  public int getAttacksLeft()
  {
    validify();
    return Client.INSTANCE.droidGetAttacksLeft(ptr);
  }
  ///The maximum number of times the Droid can attack.
  public int getMaxAttacks()
  {
    validify();
    return Client.INSTANCE.droidGetMaxAttacks(ptr);
  }
  ///The current amount health this Droid has remaining.
  public int getHealthLeft()
  {
    validify();
    return Client.INSTANCE.droidGetHealthLeft(ptr);
  }
  ///The maximum amount of this health this Droid can have
  public int getMaxHealth()
  {
    validify();
    return Client.INSTANCE.droidGetMaxHealth(ptr);
  }
  ///The number of moves this Droid has remaining.
  public int getMovementLeft()
  {
    validify();
    return Client.INSTANCE.droidGetMovementLeft(ptr);
  }
  ///The maximum number of moves this Droid can move.
  public int getMaxMovement()
  {
    validify();
    return Client.INSTANCE.droidGetMaxMovement(ptr);
  }
  ///The range of this Droid's attack.
  public int getRange()
  {
    validify();
    return Client.INSTANCE.droidGetRange(ptr);
  }
  ///The power of this Droid variant's attack.
  public int getAttack()
  {
    validify();
    return Client.INSTANCE.droidGetAttack(ptr);
  }
  ///How much armor the Droid has which reduces damage taken.
  public int getArmor()
  {
    validify();
    return Client.INSTANCE.droidGetArmor(ptr);
  }
  ///How much armor the Droid has which reduces damage taken.
  public int getMaxArmor()
  {
    validify();
    return Client.INSTANCE.droidGetMaxArmor(ptr);
  }
  ///The amount of scrap the Droid drops.
  public int getScrapWorth()
  {
    validify();
    return Client.INSTANCE.droidGetScrapWorth(ptr);
  }
  ///The number of turns this unit will be hacked, if it is hacked. If 0, the droid cannot be hacked.
  public int getTurnsToBeHacked()
  {
    validify();
    return Client.INSTANCE.droidGetTurnsToBeHacked(ptr);
  }
  ///The number of turns the Droid has remaining as hacked.
  public int getHackedTurnsLeft()
  {
    validify();
    return Client.INSTANCE.droidGetHackedTurnsLeft(ptr);
  }
  ///The amount of hacking progress that has been made.
  public int getHackets()
  {
    validify();
    return Client.INSTANCE.droidGetHackets(ptr);
  }
  ///The maximum number of hackets that can be sustained before hacked. If 0, the Droid cannot be hacked.
  public int getHacketsMax()
  {
    validify();
    return Client.INSTANCE.droidGetHacketsMax(ptr);
  }

}
