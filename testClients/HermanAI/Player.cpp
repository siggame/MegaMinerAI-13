// -*-c++-*-

#include "Player.h"
#include "game.h"


Player::Player(_Player* pointer)
{
    ptr = (void*) pointer;
}

int Player::id()
{
  return ((_Player*)ptr)->id;
}

char* Player::playerName()
{
  return ((_Player*)ptr)->playerName;
}

float Player::time()
{
  return ((_Player*)ptr)->time;
}

int Player::scrapAmount()
{
  return ((_Player*)ptr)->scrapAmount;
}


bool Player::talk(char* message)
{
  return playerTalk( (_Player*)ptr, message);
}

bool Player::orbitalDrop(int x, int y, int variant)
{
  return playerOrbitalDrop( (_Player*)ptr, x, y, variant);
}



std::ostream& operator<<(std::ostream& stream,Player ob)
{
  stream << "id: " << ((_Player*)ob.ptr)->id  <<'\n';
  stream << "playerName: " << ((_Player*)ob.ptr)->playerName  <<'\n';
  stream << "time: " << ((_Player*)ob.ptr)->time  <<'\n';
  stream << "scrapAmount: " << ((_Player*)ob.ptr)->scrapAmount  <<'\n';
  return stream;
}
