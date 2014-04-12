import com.sun.jna.Pointer;

///The class implementing gameplay logic.
public class AI extends BaseAI
{
  int spawnX, spawnY;
  //variant numbers
  public static final int CLAW = 0,
                          ARCHER = 1,
                          REPAIRER = 2,
                          HACKER = 3,
                          TURRET = 4,
                          WALL = 5,
                          TERMINATOR = 6,
                          HANGAR = 7;

  public String username()
  {
    return "Shell AI";
  }
  public String password()
  {
    return "password";
  }

  //This function is called each time it is your turn
  //Return true to end your turn, return false to ask the server for updated information
  public boolean run()
  {
    //try to spawn a claw near your side
    //make sure you own enough scrap
    if(players[playerID()].getScrapAmount() >= modelVariants[CLAW].getCost())
    {
      //make sure nothing is spawning there
      if(getTile(spawnX, spawnY).getTurnsUntilAssembled() == 0)
      {
        boolean spawn = true;
        //make sure there isn't a hangar there
        for(int i = 0; i < droids.length; i++)
        {
          //if the droid's x and y is the same as the spawn point
          if(droids[i].getX() == spawnX && droids[i].getY() == spawnY)
          {
            //if the droid is a hangar
            if(droids[i].getVariant() == HANGAR)
            {
              //can't spawn on top of hangars
              spawn = false;
              break;
            }
          }
        }
        if(spawn)
        {
          //spawn the claw
          players[playerID()].orbitalDrop(spawnX, spawnY, CLAW);
        }
      }
    }
    //loop through all of the droids
    for(int i = 0; i < droids.length; i++)
    {
      //if you have control of the droid
      if((droids[i].getOwner() == playerID() && droids[i].getHackedTurnsLeft() <= 0) ||
         (droids[i].getOwner() != playerID() && droids[i].getHackedTurnsLeft() > 0))
      {
        //if there are any moves to be done
        if(droids[i].getMovementLeft() > 0)
        {
          //try to move towards the enemy
          int changeX = 1;
          //if on the right move towards the left
          if(playerID() == 1)
          {
            changeX = -1;
          }
          boolean move = true;
          //check if there is a droid on that tile
          for(int z = 0; z < droids.length; z++)
          {
            //if the two droids are different
            if(droids[z].getId() != droids[i].getId())
            {
              //if there is a droid to run into
              if(droids[z].getX() == droids[i].getX() + changeX && droids[z].getY() == droids[i].getY())
              {
                //don't move
                move = false;
              }
            }
          }
          //move if okay and within map boundaries
          if(move && droids[i].getX() + changeX >= 0 && droids[i].getX() + changeX < mapWidth())
          {
            droids[i].move(droids[i].getX() + changeX, droids[i].getY());
          }
        }
        //if there are any attacks left
        if(droids[i].getAttacksLeft() > 0)
        {
          //find a target towards the enemy
          int changeX = 1;
          //enemy is to the left if playerID is one
          if(playerID() == 1)
          {
            changeX = -1;
          }
          Droid target = null;
          for(int z = 0; z < droids.length; z++)
          {
            //if the droid is there make it a target
            if(droids[z].getX() == droids[i].getX() + changeX && droids[z].getY() == droids[i].getY() && droids[z].getHealthLeft() > 0)
            {
              target = droids[z];
            }
          }
          //if a target was found
          if(target != null)
          {
            //repairer logic
            if(droids[i].getVariant() == REPAIRER)
            {
              //only try to heal your units or hacked enemy units
              if((target.getOwner() == playerID() && target.getHackedTurnsLeft() <= 0) ||
                 (target.getOwner() != playerID() && target.getHackedTurnsLeft() > 0))
              {
                //heal the target
                droids[i].operate(target.getX(), target.getY());
              }
            }
            //hacker unit logic
            else if(droids[i].getVariant() == HACKER)
            {
              //only operate on non-hacked enemy units
              if(target.getOwner() != playerID() && target.getHackedTurnsLeft() == 0)
              {
                //don't hack hangars or walls
                if(target.getVariant() != HANGAR && target.getVariant() != WALL)
                {
                  //hack the target
                  droids[i].operate(target.getX(), target.getY());
                }
              }
            }
            //other unit logic
            else
            {
              //only operate on hacked friendly units or enemy units
              if((target.getOwner() == playerID() && target.getHackedTurnsLeft() > 0) ||
                 (target.getOwner() != playerID() && target.getHackedTurnsLeft() <= 0))
              {
                //attack the target
                droids[i].operate(target.getX(), target.getY());
              }
            }
          }
        }
      }
    }
    return true;
  }


  //This function is called once, before your first turn
  public void init()
  {
    int offset = 0;
    boolean found = false;
    while(!found)
    {
      //find a location without a hangar
      for(int i = 0; i < tiles.length; i++)
      {
        //make sure that the tile is near the edge
        if(tiles[i].getX() == (mapWidth() - 1) * playerID() + offset)
        {
          boolean hangarPresent = false;
          //check for hangar
          for(int z = 0; z < droids.length; z++)
          {
            if(droids[z].getX() == tiles[i].getX() && droids[z].getY() == tiles[i].getY())
            {
              hangarPresent = true;
              break;
            }
          }
          if(!hangarPresent)
          {
            spawnX = tiles[i].getX();
            spawnY = tiles[i].getY();
            found = true;
            break;
          }
        }
      }
      //if nothing was found then move away from the edge
      if(!found)
      {
        //if on the left
        if(playerID() == 0)
        {
          offset++;
        }
        else
        {
          //on the right
          offset--;
        }
      }
    }
  }

  //This function is called once, after your last turn
  public void end() {}


  public AI(Pointer c)
  {
    super(c);
  }

  //This functions returns a reference to a tile
  Tile getTile(int x, int y)
  {
    if(x >= mapWidth() || x < 0 || y >= mapHeight() || y < 0)
    {
      return null;
    }
    return tiles[y + x * mapHeight()];
  }
}
