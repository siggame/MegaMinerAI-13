using System;
using System.Runtime.InteropServices;

/// <summary>
/// This class implements most the code an AI would need to interface with the lower-level game code.
/// AIs should extend this class to get a lot of builer-plate code out of the way. The provided AI class does just that.
/// </summary>
public abstract class BaseAI
{
% for model in models:
%   if model.type == 'Model':
  public static ${model.name}[] ${lowercase(model.plural)};
%   endif
% endfor

  IntPtr connection;
  public static int iteration;
  bool initialized;

  public BaseAI(IntPtr c)
  {
    connection = c;
  }

  /// <summary>
  /// Make this your username, which should be provided.
  /// </summary>
  /// <returns>Returns the username of the player.</returns>
  public abstract String username();

  /// <summary>
  /// Make this your password, which should be provided.
  /// </summary>
  /// <returns>Returns the password of the player.</returns>
  public abstract String password();

  /// <summary>
  /// This is run once on turn one before run().
  /// </summary>
  public abstract void init();

  /// <summary>
  /// This is run every turn.
  /// </summary>
  /// <returns>
  /// Return true to end turn, false to resynchronize with the 
  /// server and run again.
  /// </returns>
  public abstract bool run();

  /// <summary>
  /// This is run once after your last turn.
  /// </summary>
  public abstract void end();

  /// <summary>
  /// Synchronizes with the server, then calls run().
  /// </summary>
  /// <returns>
  /// Return true to end turn, false to resynchronize with the 
  /// server and run again.
  /// </returns>
  public bool startTurn()
  {
    int count = 0;
    iteration++;

% for model in models:
%   if model.type == 'Model':
    count = Client.get${model.name}Count(connection);
    ${lowercase(model.plural)} = new ${model.name}[count];
    for(int i = 0; i < count; i++)
      ${lowercase(model.plural)}[i] = new ${model.name}(Client.get${model.name}(connection, i));

%   endif
% endfor
    if(!initialized)
    {
      initialized = true;
      init();
    }

    return run();
  }
% for datum in globals:

  /// <summary>
  /// ${datum.doc}
  /// </summary>
  /// <returns>Returns ${lowercase(datum.doc)}</returns>
  public ${types[datum.type]} ${datum.name}()
  {
    ${types[datum.type]} value = Client.get${capitalize(datum.name)}(connection);
%   if datum.type is str:
    return Marshal.PtrToStringAuto(value);
%   else:
    return value;
%   endif
  }
% endfor
}
