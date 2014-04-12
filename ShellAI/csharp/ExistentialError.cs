/// <summary>
/// Represents an error that arises when trying to use an object that no longer exists.
/// </summary>
public class ExistentialError : System.ApplicationException
{
  public ExistentialError()
    : base("Object does not exist anymore.")
  { }
}