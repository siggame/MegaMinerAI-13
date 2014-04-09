#include "droids.h"
#include "droidsAnimatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include <utility>
#include <time.h>
#include <list>

namespace visualizer
{
  Droids::Droids()
  {
    m_game = 0;
    m_suicide=false;
    m_NumHangers = 0;
    m_Player0Hangars = 0;
    m_Player1Hangars = 0;
  } // Droids::Droids()

  Droids::~Droids()
  {
    destroy();
  }

  void Droids::destroy()
  {
	m_suicide=true;
	wait();
	animationEngine->registerGame(0, 0);

	clear();
	delete m_game;
	m_game = 0;

	// Clear your memory here

	programs.clear();

  } // Droids::~Droids()

  void Droids::preDraw()
  {
	renderer->push();
	renderer->translate(GRID_OFFSET, GRID_OFFSET);

	UpdateHangarCount();
	RenderGrid();
    DrawHUD();

    // Handle player input here
  }

  void Droids::postDraw()
  {
	  renderer->pop();
  }

  void Droids::GetSelectedRect(Rect &out) const
  {
      const Input& input = gui->getInput();

      int x = input.x - GRID_OFFSET;
      int y = input.y - GRID_OFFSET;
      int width = input.sx - x - GRID_OFFSET;
      int height = input.sy - y - GRID_OFFSET;

      int right = x + width;
      int bottom = y + height;

      out.left = min(x,right);
      out.top = min(y,bottom);
      out.right = max(x,right);
      out.bottom = max(y,bottom);
  }

  glm::vec3 Droids::GetTeamColor(int owner) const
  {
    return owner == 1 ? glm::vec3(0.5f,1.0f,0.5f) : glm::vec3(0.5f,0.5f,1.0f);
  }

  PluginInfo Droids::getPluginInfo()
  {
    PluginInfo i;
    i.searchLength = 1000;
    i.gamelogRegexPattern = "Droids";
    i.returnFilename = false;
    i.spectateMode = false;
    i.pluginName = "MegaMinerAI: Droids Plugin";


    return i;
  } // PluginInfo Droids::getPluginInfo()

  void Droids::setup()
  {
    gui->checkForUpdate( "Droids", "./plugins/droids/checkList.md5", VERSION_FILE );
    options->loadOptionFile( "./plugins/droids/droids.xml", "droids" );
    resourceManager->loadResourceFile( "./plugins/droids/resources.r" );
  }
  
  // Give the Debug Info widget the selected object IDs in the Gamelog
  list<int> Droids::getSelectedUnits()
  {
    // TODO Selection logic
    return list<int>();  // return the empty list
  }

  void Droids::RenderGrid() const
  {
      const float gustLength = 2.0f;
      static float time = 0.0f;
      static float nextGust = rand() % 4 + 2.0f;
      static bool direction = 0;

	  time += timeManager->getDt();

	  renderer->setColor({0.9,0.9, 0.9, 1.0f});
	  renderer->drawSubTexturedQuad(-m_mapWidth,-m_mapHeight,m_mapWidth*3,m_mapHeight*3,0,0, 16/1.5, 9/1.5,"cliffside");


      renderer->setColor({1.0, 0.0, 0.0, 0.4});
	  renderer->drawRotatedTexturedQuad(-m_mapWidth,-m_mapHeight,m_mapWidth*3,m_mapHeight*3,2.0f, time, "grid");

	  renderer->setColor({0.7, 0.8, 0.8, 0.5});
	  renderer->drawRotatedTexturedQuad(-m_mapWidth,-m_mapHeight,m_mapWidth*3,m_mapHeight*3,2.2f, -time/2, "grid");


      renderer->setColor({1.0f,1.0f,1.0f,1.0f});
	  renderer->drawSubTexturedQuad(0,0,m_mapWidth,m_mapHeight, 0, 0, 2, 1,"desolate");

      for(int i = 0; i < m_mapWidth; i++)
      {
          renderer->drawTexturedQuad(i, -1, 1, 1, 1, "rivet");
          renderer->drawRotatedTexturedQuad(i, m_mapHeight, 1, 1, 1, 180, "rivet");
      }

      for(int i = 0; i < m_mapHeight; i++)
      {
          renderer->drawRotatedTexturedQuad(-1, i, 1, 1, 1, 270, "rivet");
          renderer->drawRotatedTexturedQuad(m_mapWidth, i, 1, 1, 1, 90, "rivet");
      }

      renderer->drawTexturedQuad(-1, -1, 1, 1, 1, "rivet_corner");
      renderer->drawRotatedTexturedQuad(m_mapWidth, -1, 1, 1, 1, 90, "rivet_corner");
      renderer->drawRotatedTexturedQuad(-1, m_mapHeight, 1 , 1, 1, 270, "rivet_corner");
      renderer->drawRotatedTexturedQuad(m_mapWidth, m_mapHeight, 1, 1, 1, 180, "rivet_corner");

      if(time > nextGust + gustLength)
      {
          nextGust = time + rand() % 4 + 4.0f;
          direction = !direction;
      }

      if(time > nextGust)
      {
        float alphaValue = 0.15f * sin( ((time - nextGust)/ gustLength) * 3.141592f );
        renderer->setColor({1.0f, 1.0f, 1.0f, alphaValue});
      }
      else
      {
        renderer->setColor({1.0f, 1.0f, 1.0f,0.0f});
      }

      if (direction)
      {
        renderer->drawSubTexturedQuad(-m_mapWidth,-m_mapHeight,m_mapWidth*3,m_mapHeight*3, 0, 0, 16, 9, "dust", fmod(time, 1.0f) * 5, fmod(time, 1.0f));
      }
      else
      {
        renderer->drawSubTexturedQuad(-m_mapWidth,-m_mapHeight,m_mapWidth*3,m_mapHeight*3, 0, 0, 16, 9, "dust", -fmod(time, 1.0f) * 5, fmod(time, 1.0f));
      }

	  // Draw horizontal lines
	  renderer->setColor({0.0f,0.0f,0.0f,1.0f});
	  for(int i = 0; i <= m_mapHeight; i++)
	  {
		  renderer->drawLine(0,i,m_mapWidth,i,1.0f);
	  }

	  // Draw vertical lines
	  for(int i = 0; i <= m_mapWidth; i++)
	  {
		  renderer->drawLine(i,0,i,m_mapHeight,1.0f);
	  }
  }

  void Droids::DrawHUD() const
  {
      float x = m_mapWidth / 2;
      float y = m_mapHeight + 1.5;

      const float boxOffset = 16;
      const float boxWidth = 10;
      const float boxHeight = 3.5;

      const float healthBarOffset = 6;
      const float healthBarWidth = 6;
      const float healthBarHeight = healthBarWidth/ 2;

      const float pipeHeight = healthBarHeight /2;
      const float pipeLength = (x - healthBarOffset - (healthBarWidth/2)) - (x - boxOffset + (boxWidth/2)) ;
      const int numPipeSections = static_cast<int>(pipeLength) * 2;
      float pipeSectionWidth = pipeLength/ numPipeSections;

      const float healthWidth = healthBarWidth - 1.5f;
      const float healthHeight = healthBarHeight - 0.2f;
      const float healthUnitWidth = healthWidth/m_NumHangers;

      // player 0 health
      int interval = 0;
      glm::vec3 color = GetTeamColor(0);

	  std::cout << m_NumHangers << "   " << m_Player0Hangars << "  " << m_Player1Hangars <<  std::endl;
	  for(interval = 0; interval < m_Player0Hangars; interval++)
      {
          // bars for alive hangars
          // too dark, i'm doing it manulally
          renderer->setColor(Color(color.r, color.g, color.b, 1.0f));
          renderer->drawTexturedQuad((x - healthBarOffset - (healthWidth)/2) + (interval*healthUnitWidth),
                                    (y + (boxHeight/2) - (healthHeight/2)),
                                     healthUnitWidth, healthHeight - 0.2f, 1, "pipe_section");
      }

      for(;interval < m_NumHangers; interval++)
      {
          // bars for dead hangars
          renderer->setColor(Color(0.85, 0.85, 1.0f, 1.0f));
          renderer->drawTexturedQuad((x - healthBarOffset - (healthWidth)/2) + (interval*healthUnitWidth),
                                    (y + (boxHeight/2) - (healthHeight/2)),
                                     healthUnitWidth, healthHeight - 0.2f, 1, "pipe_section");
      }


      // player 1 health
      color = GetTeamColor(1);
      for(interval = 0; interval < m_NumHangers - m_Player1Hangars; interval++)
      {
          // bars for dead hangars
          renderer->setColor(Color(color.r, color.g, color.b, 1.0f));
          renderer->drawTexturedQuad((x + healthBarOffset - (healthWidth)/2) + (interval*healthUnitWidth),
                                    (y + (boxHeight/2) - (healthHeight/2)),
                                     healthUnitWidth, healthHeight - 0.2f, 1, "pipe_section");
      }

      for(;interval < m_NumHangers; interval ++)
      {
          // bars for alive hangars
          renderer->setColor(Color(color.r * 0.5, color.g * 0.5, color.b * 0.5, 1.0f));
          renderer->drawTexturedQuad((x + healthBarOffset - (healthWidth)/2) + (interval*healthUnitWidth),
                                    (y + (boxHeight/2) - (healthHeight/2)),
                                     healthUnitWidth, healthHeight - 0.2f, 1, "pipe_section");
      }

      for(int side : {-1,1})
      {
          // render the pipe from the health tank to the status screen
          renderer->setColor(Color(1.0f, 1.0f, 1.0f, 1.0f));
          for(int i = 0; i < numPipeSections; i++)
          {
              if(side == -1)
              {
                  renderer->drawTexturedQuad((x + (side * boxOffset) + (boxWidth/2) ) + (pipeSectionWidth * i),
                                              y + (boxHeight/2) - (pipeHeight/2),
                                             pipeSectionWidth, pipeHeight,  1, "pipe_section");
              }
              else
              {
                  renderer->drawTexturedQuad((x + (side * healthBarOffset) + (healthBarWidth/2) ) + (pipeSectionWidth * i),
                                              y + (boxHeight/2) - (pipeHeight/2),
                                             pipeSectionWidth, pipeHeight,  1, "pipe_section");
              }
          }

          // render the status screen
          renderer->setColor(Color(0.0f, 0.0f, 0.0f, 1.0f));
          renderer->drawQuad(x + (side * boxOffset) - boxWidth/2, y,
                             boxWidth, boxHeight);

          renderer->setColor(Color(1.0f, 1.0f, 1.0f, 1.0f));
          for(int i = 1; i < (boxWidth * 2) - 1; i++)
          {
              renderer->drawTexturedQuad((x + (side * boxOffset) - boxWidth /2) + i/2.0f, y,
                                         0.5, 0.5, 1, "rivet");
              renderer->drawRotatedTexturedQuad((x + (side * boxOffset)  - boxWidth /2) + i/2.0f, y + boxHeight,
                                                0.5, 0.5, 1, 180, "rivet");
          }

          for(int i = 1; i < (boxHeight * 2); i++)
          {
              renderer->drawRotatedTexturedQuad(x + (side * boxOffset) - boxWidth/2, y + i/2.0f,
                                         0.5, 0.5, 1, 270, "rivet");
              renderer->drawRotatedTexturedQuad(x + (side * boxOffset) + boxWidth/2 - 0.5, y + i/2.0f,
                                         0.5, 0.5, 1, 90, "rivet");
          }

          renderer->drawTexturedQuad(x + (side* boxOffset) - boxWidth/2, y,
                                     0.5, 0.5, 1, "rivet_corner");
          renderer->drawRotatedTexturedQuad(x + (side* boxOffset) + boxWidth/2 - 0.5, y,
                                     0.5, 0.5, 1, 90, "rivet_corner");
          renderer->drawRotatedTexturedQuad(x + (side * boxOffset) - boxWidth/2 , y + boxHeight,
                                            0.5, 0.5, 1, 270, "rivet_corner");
          renderer->drawRotatedTexturedQuad(x + (side * boxOffset) + boxWidth/2 - 0.5, y + boxHeight,
                                            0.5, 0.5, 1, 180, "rivet_corner");

          // draw the health tank
          renderer->drawTexturedQuad(x + (side *healthBarOffset) - healthBarWidth/2, (y + (boxHeight/2) - (healthBarHeight /2)),
                                     healthBarWidth, healthBarHeight , 1, "health_bar");


      }

      // draw the names of the teams on the status screen
      for (int owner : {0,1})
      {
          int namePos = owner == 0 ? (x - boxOffset - (boxWidth/2) + 1) : (x + boxOffset + (boxWidth/2) - 1);
          IRenderer::Alignment alignment = owner == 0 ? IRenderer::Left : IRenderer::Right;

          glm::vec3 playerColor = GetTeamColor(owner);

          renderer->setColor( Color(playerColor.r,playerColor.g,playerColor.b, 1.0f));
          renderer->drawText(namePos, y+(1/2.0f) , "Roboto", m_game->states[0].players[owner].playerName, 3.0f, alignment);

      }
  }

  void Droids::UpdateHangarCount()
  {
	int curTurn = timeManager->getTurn();
	auto & curState = m_game->states[curTurn];

	m_Player0Hangars = m_Player1Hangars = 0;

	for(auto& droid : curState.droids)
	{
		if(droid.second.variant == DROID_HANGAR)
		{
			if(droid.second.owner == 0)
				m_Player0Hangars++;
			else
				m_Player1Hangars++;
		}
	}
  }

  void Droids::loadGamelog( std::string gamelog )
  {
    if(isRunning())
    {
      m_suicide = true;
      wait();
    }
    m_suicide = false;

    // BEGIN: Initial Setup
    setup();

    delete m_game;
    m_game = new parser::Game;

    if( !parser::parseGameFromString( *m_game, gamelog.c_str() ) )
    {
      delete m_game;
      m_game = 0;
      WARNING(
          "Cannot load gamelog, %s", 
          gamelog.c_str()
          );
    }
    // END: Initial Setup

	assert("Gamelog is empty" && !m_game->states.empty());

	m_mapWidth = m_game->states[0].mapWidth;
    m_mapHeight = m_game->states[0].mapHeight;

	renderer->setCamera( 0, 0, m_mapWidth + GRID_OFFSET*2, m_mapHeight + 4 + GRID_OFFSET*2);
	renderer->setGridDimensions( m_mapWidth + GRID_OFFSET*2, m_mapHeight + 4 + GRID_OFFSET*2);
 
    start();
  } // Droids::loadGamelog()
  
  // The "main" function
  void Droids::run()
  {
    Frame * turn = new Frame;
    Frame * nextTurn = new Frame;

	gui->setDebugOptions(this);
    timeManager->setNumTurns( 0 );

    animationEngine->registerGame(0, 0);

    for(auto & droid : m_game->states[0].droids)
    {
        if(droid.second.variant == DROID_HANGAR && droid.second.owner == 0)
        {
            m_NumHangers++;
        }
    }

	std::cout << m_NumHangers << "  " << m_Player0Hangars << "  " << m_Player1Hangars << std::endl;

	// Look through each turn in the gamelog
	for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
    {
        //cout << "Turn " << state << " there are " << m_game->states[state].droids.size() << " droids" << endl;

        PrepareUnits(state, *turn, *nextTurn);
        PrepareTiles(state, *turn, *nextTurn);

        animationEngine->buildAnimations(*turn);
        addFrame(*turn);

		// Register the game and begin playing delayed due to multithreading
		if(state > 5)
		{
			timeManager->setNumTurns(state - 5);
			animationEngine->registerGame( this, this );
			if(state == 6)
			{
				animationEngine->registerGame(this, this);
				timeManager->setTurn(0);
				timeManager->play();
			}
		}

        delete turn;
        turn = nextTurn;
        nextTurn = new Frame;
	}

	if(!m_suicide)
	{
		timeManager->setNumTurns( m_game->states.size() );
        timeManager->play();
	}

    delete turn;
    delete nextTurn;
  } // Droids::run()

  void Droids::PrepareUnits(const int& frameNum, Frame& turn, Frame& nextFrame)
  {
      std::string texture;
      parser::GameState& currentState = m_game->states[frameNum];

      for(auto& it: currentState.droids)
      {
          parser::Droid& unit = it.second;
          switch(unit.variant)
          {
			case DROID_CLAW:
				  texture = "claw";
				  break;
			case DROID_ARCHER:
				  texture = "archer";
				  break;
			case DROID_REPAIRER:
				  texture = "repairer";
				  break;
			case DROID_HACKER:
				  texture = "hacker";
				  break;
			case DROID_TURRET:
				  texture = "turret";
				  break;
			case DROID_WALL:
				  texture = "wall";
				  break;
			case DROID_TERMINATOR:
				  texture = "terminator";
				  break;
			case DROID_HANGAR:
				  texture = "hangar";
				  break;
			default:
				  assert("Unknown Droid Variant" && false);
          }

          SmartPointer<MoveableSprite> sprite = new MoveableSprite(texture);

          const auto& iter = currentState.animations.find(unit.id);
          if(iter != currentState.animations.end())
          {
              for(auto& anim : iter->second)
              {
                  switch(anim->type)
                  {
                      case parser::MOVE:
                      {
                          parser::move& move = (parser::move&)*anim;
                          sprite->m_Moves.push_back(MoveableSprite::Move(glm::vec2(move.toX, move.toY), glm::vec2(move.fromX, move.fromY)));
                          break;
                      }
                      case parser::SPAWN:
                      {
                          break;
                      }
                      case parser::HACK:
                      {
                          break;
                      }
                      case parser::ORBITALDROP:
                      {
                          break;
                      }
                      case parser::REPAIR:
                      {
                          break;
                      }
                      case parser::ATTACK:
                      {
                          break;
                      }
                      default:
                      break;
                  }
              }
          }

          // check for deaths
		  if(frameNum < m_game->states.size() - 1)
          {
              auto& nextState = m_game->states[frameNum+1];
              auto next = nextState.droids.find(unit.id);

              if(next == nextState.droids.end())
              {
                  SmartPointer<AnimatedSprite> deathAnim = new AnimatedSprite(glm::vec2(unit.x, unit.y), glm::vec2(1.0f, 1.0f), "death", 63);
                  deathAnim->addKeyFrame(new DrawAnimatedSprite(deathAnim, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f)));
                  nextFrame.addAnimatable(deathAnim);

				  std::cout << "FRAME: " << frameNum << std::endl;
				  switch(unit.variant)
				  {
					  case DROID_CLAW:
						  std::cout << "claw died\n";
						  break;
					  case DROID_ARCHER:
						  std::cout << "archer died\n";
						  break;
					  case DROID_HACKER:
						  std::cout << "hacker died\n";
						  break;
					  case DROID_REPAIRER:
						  std::cout << "repairer died\n";
						  break;
					  case DROID_TERMINATOR:
						  std::cout << "terminator died\n";
						  break;
					  case DROID_TURRET:
						  std::cout << "turret died\n";
						  break;
					  case DROID_WALL:
						  std:cout << "wall died\n";
						  break;
					  case DROID_HANGAR:
					  {
						  std::cout << "hangar died\n";
						  if(unit.owner == 0)
							  m_Player0Hangars--;
						  if(unit.owner == 1)
							  m_Player1Hangars--;
						  break;
					 }
				  }

              }
          }

          if(sprite->m_Moves.empty())
          {
                sprite->m_Moves.push_back(MoveableSprite::Move(glm::vec2(unit.x, unit.y), glm::vec2(unit.x, unit.y)));
          }
          sprite->addKeyFrame(new DrawSmoothMoveSprite(sprite, glm::vec4(GetTeamColor(unit.owner), 1.0f)));
          turn.addAnimatable(sprite);

      }
  }

  void Droids::PrepareTiles(const int &frameNum, Frame &turn, Frame& nextTurn)
  {

  }

} // visualizer

Q_EXPORT_PLUGIN2( Droids, visualizer::Droids );
