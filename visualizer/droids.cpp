#include "droids.h"
#include "droidsAnimatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include <utility>
#include <time.h>
#include <list>
#include <glm/glm.hpp>

namespace visualizer
{
  Droids::Droids()
  {
    m_game = 0;
    m_suicide=false;
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

	RenderGrid();


    // Handle player input here
  }

  void Droids::postDraw()
  {

	  renderer->pop();
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

	  time += timeManager->getDt();

      renderer->setColor({0.7,0.7, 0.7, 1.0f});
      renderer->drawSubTexturedQuad(-m_mapWidth,-m_mapHeight,m_mapWidth*3,m_mapHeight*3,0,0, 16/1.5, 9/1.5,"cliffside");

      renderer->setColor({1.0f,1.0f,1.0f,1.0f});
      renderer->drawSubTexturedQuad(0,0,m_mapWidth,m_mapHeight, 0, 0, 2, 1,"desolate");

      if(time > nextGust + gustLength)
      {
          nextGust = time + rand() % 4 + 4.0f;
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

      renderer->drawSubTexturedQuad(-m_mapWidth,-m_mapHeight,m_mapWidth*3,m_mapHeight*3, 0, 0, 16, 9, "dust", fmod(time, 1.0f) * 5, fmod(time, 1.0f));

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
	cout << "Map Width: " << m_mapWidth << endl;
	cout << "Map Height: " << m_mapHeight << endl;
	renderer->setCamera( 0, 0, m_mapWidth + GRID_OFFSET*2, m_mapHeight + 4 + GRID_OFFSET*2);
	renderer->setGridDimensions( m_mapWidth + GRID_OFFSET*2, m_mapHeight + 4 + GRID_OFFSET*2);
 
    start();
  } // Droids::loadGamelog()
  
  // The "main" function
  void Droids::run()
  {
	gui->setDebugOptions(this);
    timeManager->setNumTurns( 0 );

    animationEngine->registerGame(0, 0);

	// Look through each turn in the gamelog
	for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
	{
		Frame turn;  // The frame that will be drawn

        //cout << "Turn " << state << " there are " << m_game->states[state].droids.size() << " droids" << endl;

        PrepareUnits(state, turn);
        PrepareStructures(state, turn);


		animationEngine->buildAnimations(turn);
		addFrame(turn);

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
	}

	if(!m_suicide)
	{
		timeManager->setNumTurns( m_game->states.size() );
		timeManager->play();
	}

  } // Droids::run()

  void Droids::PrepareUnits(const int& frameNum, Frame& turn) const
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
            case DROID_TERMINATOR:
              texture = "terminator";
              break;
            default:
              std::cout << "ouch\n";
          }

          const auto& iter = currentState.animations.find(unit.id);
          if(iter != currentState.animations.end())
          {
              std::vector<SmartPointer<parser::Animation> >& animList = iter->second;
              SmartPointer<MoveableSprite> sprite = new MoveableSprite(texture);
              for(auto& anim: animList)
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

              turn.addAnimatable(sprite);
          }
          else
          {
              SmartPointer<BaseSprite> sprite = new BaseSprite(glm::vec2(unit.x, unit.y), glm::vec2(1.0f, 1.0f), texture);
              sprite->addKeyFrame(new DrawSprite(sprite, glm::vec4(1.0f,1.0f,1.0f,1.0f)));
              turn.addAnimatable(sprite);
          }
          std::cout << "unit made.\n";
      }
  }

  void Droids::PrepareStructures(const int &frameNum, Frame &turn) const
  {
      parser::GameState& currentState = m_game->states[frameNum];

      for(auto& it : currentState.tiles)
      {
          parser::Tile& tile = it.second;

          /*
          std::string texture;
          if(tile.owner != 2)
          {
              std::cout << "tile owner: " << tile.owner << std::endl;
              switch(tile.type)
              {
                case STRUCTURE_WALL:
                  texture = "wall";
                  break;
                case STRUCTURE_HANGER:
                  texture = "hanger";
                  break;
                default:
                  //std::cout << "ouch";
                  break;
              }

              SmartPointer<BaseSprite> sprite = new BaseSprite(glm::vec2(tile.x, tile.y), glm::vec2(1.0f,1.0f), texture);
              sprite->addKeyFrame(new DrawSprite(sprite, glm::vec4(1.0f,1.0f,1.0f,1.0f)));
              turn.addAnimatable(sprite);
          }
          */
      }
  }

} // visualizer

Q_EXPORT_PLUGIN2( Droids, visualizer::Droids );
