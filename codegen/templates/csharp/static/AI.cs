using System;
using System.Runtime.InteropServices;

/// <summary>
/// The class implementing gameplay logic.
/// </summary>
class AI : BaseAI
{
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
    return true;
  }

  /// <summary>
  /// This function is called once, before your first turn.
  /// </summary>
  public override void init() { }

  /// <summary>
  /// This function is called once, after your last turn.
  /// </summary>
  public override void end() { }

  public AI(IntPtr c) 
      : base(c) { }
}
