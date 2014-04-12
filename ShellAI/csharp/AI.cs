using System;
using System.Runtime.InteropServices;

enum Unit
{
  CLAW = 0,
  ARCHER = 1,
  REPAIRER = 2,
  HACKER = 3,
  TURRET = 4,
  WALL = 5,
  TERMINATOR = 6,
  HANGAR = 7,
};


/// <summary>
/// The class implementing gameplay logic.
/// </summary>
class AI : BaseAI
{
    int spawnX = 4, spawnY = 4;

  public override string username()
  {
    return "Shell AI";
  }

  public override string password()
  {
    return "password";
  }

  /// <summary>
  /// This function is called each time it is your turn.
  /// </summary>
  /// <returns>True to end your turn. False to ask the server for updated information.</returns>
  public override bool run()
  {
      //try to spawn a claw near your side
      //make sure you own enough scrap
      if (players[playerID()].ScrapAmount >= modelVariants[(int)Unit.CLAW].Cost)
      {
          //make sure nothing is spawning there
          if (getTile(spawnX, spawnY).TurnsUntilAssembled == 0)
          {
              bool spawn = true;
              //make sure there isn't a hangar there
              for (int i = 0; i < droids.Length; i++)
              {
                  //if the droid's x and y is the same as the spawn point
                  if (droids[i].X == spawnX && droids[i].Y == spawnY)
                  {
                      //if the droid is a hangar
                      if (droids[i].Variant == (int) Unit.HANGAR)
                      {
                          //can't spawn on top of hangars
                          spawn = false;
                          break;
                      }
                  }
              }
              if (spawn)
              {
                  //spawn the claw
                  players[playerID()].orbitalDrop(spawnX, spawnY, (int)Unit.CLAW);
              }
          }
      }
      //loop through all of the droids
      for (int i = 0; i < droids.Length; i++)
      {
          //if you have control of the droid
          if ((droids[i].Owner == playerID() && droids[i].HackedTurnsLeft <= 0) ||
             (droids[i].Owner != playerID() && droids[i].HackedTurnsLeft > 0))
          {
              //if there are any moves to be done
              if (droids[i].MovementLeft > 0)
              {
                  //try to move towards the enemy
                  int changeX = 1;
                  //if on the right move towards the left
                  if (playerID() == 1)
                  {
                      changeX = -1;
                  }
                  bool move = true;
                  //check if there is a droid on that tile
                  for (int z = 0; z < droids.Length; z++)
                  {
                      //if the two droids are different
                      if (droids[z].Id != droids[i].Id)
                      {
                          //if there is a droid to run into
                          if (droids[z].X == droids[i].X + changeX && droids[z].Y == droids[i].Y)
                          {
                              //don't move
                              move = false;
                          }
                      }
                  }
                  //move if okay and within map boundaries
                  if (move && droids[i].X + changeX >= 0 && droids[i].X + changeX < mapWidth())
                  {
                      droids[i].move(droids[i].X + changeX, droids[i].Y);
                  }
              }
              //if there are any attacks left
              if (droids[i].AttacksLeft > 0)
              {
                  //find a target towards the enemy
                  int changeX = 1;
                  //enemy is to the left if playerID is one
                  if (playerID() == 1)
                  {
                      changeX = -1;
                  }
                  Droid target = null;
                  for (int z = 0; z < droids.Length; z++)
                  {
                      //if the droid is there make it a target
                      if (droids[z].X == droids[i].X + changeX && droids[z].Y == droids[i].Y && droids[z].HealthLeft > 0)
                      {
                          target = droids[z];
                      }
                  }
                  //if a target was found
                  if (target != null)
                  {
                      //repairer logic
                      if (droids[i].Variant == (int)Unit.REPAIRER)
                      {
                          //only try to heal your units or hacked enemy units
                          if ((target.Owner == playerID() && target.HackedTurnsLeft <= 0) ||
                             (target.Owner != playerID() && target.HackedTurnsLeft > 0))
                          {
                              //heal the target
                              droids[i].operate(target.X, target.Y);
                          }
                      }
                      //hacker unit logic
                      else if (droids[i].Variant == (int)Unit.HACKER)
                      {
                          //only operate on non-hacked enemy units
                          if (target.Owner != playerID() && target.HackedTurnsLeft > 0)
                          {
                              //don't hack hangars or walls
                              if (target.Variant != (int)Unit.HANGAR && target.Variant != (int)Unit.WALL)
                              {
                                  //hack the target
                                  droids[i].operate(target.X, target.Y);
                              }
                          }
                      }
                      //other unit logic
                      else
                      {
                          //only operate on hacked friendly units or enemy units
                          if ((target.Owner == playerID() && target.HackedTurnsLeft > 0) ||
                             (target.Owner != playerID() && target.HackedTurnsLeft <= 0))
                          {
                              //attack the target
                              droids[i].operate(target.X, target.Y);
                          }
                      }
                  }
              }
          }
      }
      return true;
  }

  /// <summary>
  /// This function is called once, before your first turn.
  /// </summary>
  public override void init()
  {
    int offset = 0;
    bool found = false;
    while(!found)
    {
      //find a location without a hangar
      for(int i = 0; i < tiles.Length; i++)
      {
        //make sure that the tile is near the edge
        if(tiles[i].X == (mapWidth() - 1) * playerID() + offset)
        {
          bool hangarPresent = false;
          //check for hangar
          for(int z = 0; z < droids.Length; z++)
          {
            if(droids[z].X == tiles[i].X && droids[z].Y == tiles[i].Y)
            {
              hangarPresent = true;
              break;
            }
          }
          if(!hangarPresent)
          {
            spawnX = tiles[i].X;
            spawnY = tiles[i].Y;
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

  /// <summary>
  /// This function is called once, after your last turn.
  /// </summary>
  public override void end() { }


//This functions returns a pointer to a tile, or returns null for an invalid tile
Tile getTile(int x, int y)
{
  if(x >= mapWidth() || x < 0 || y >= mapHeight() || y < 0)
  {
    return null;
  }
  return tiles[y + x * mapHeight()];
}

  public AI(IntPtr c)
      : base(c) { }
}
