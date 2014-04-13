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

    ProcessInput();

    UpdateHangarCount();
	RenderGrid();
    DrawHUD();

    // Handle player input here
  }

  void Droids::postDraw()
  {
	  renderer->pop();

      DrawObjectSelection();
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

  void Droids::ProcessInput()
  {
      const Input& input = gui->getInput();
      int turn = timeManager->getTurn();
      int unitSelectable = gui->getDebugOptionState("Units Selectable");
      int tilesSelectable = gui->getDebugOptionState("Tiles Selectable");

      if(input.leftRelease && turn < (int) m_game->states.size())
      {
          Rect R;
          GetSelectedRect(R);

          m_SelectedUnits.clear();

          if(unitSelectable)
          {
              for(auto& iter : m_game->states[turn].droids)
              {
                  const auto& unit = iter.second;

                  if(R.left <= unit.x && R.right >= unit.x &&
                     R.top <= unit.y && R.bottom >= unit.y )
                  {
                      m_SelectedUnits.push_back(unit.id);
                  }
              }
          }

          if(tilesSelectable)
          {
              for(auto& iter : m_game->states[turn].tiles)
              {
                  const auto& tile = iter.second;

                  if(R.left <= tile.x && R.right >= tile.x &&
                     R.top <= tile.y && R.bottom >= tile.y)
                  {
                      m_SelectedUnits.push_back(tile.id);
                  }
              }
          }

          gui->updateDebugWindow();
          gui->updateDebugUnitFocus();
      }
  }

  void Droids::pruneSelection()
  {
      int turn = timeManager->getTurn();
      bool changed = false;
      int focus = gui->getCurrentUnitFocus();

      if(turn < (int) m_game->states.size())
      {
          auto iter = m_SelectedUnits.begin();

          while(iter != m_SelectedUnits.end())
          {
              if(m_game->states[turn].droids.find(*iter) == m_game->states[turn].droids.end() &&
                (m_game->states[turn].tiles.find(*iter) == m_game->states[turn].tiles.end()))
              {
                  iter = m_SelectedUnits.erase(iter);
                  changed = true;
              }
              else
                  iter++;

              if(changed == true)
                gui->updateDebugWindow();

              if(std::find(m_SelectedUnits.begin(), m_SelectedUnits.end(), focus) == m_SelectedUnits.end())
                gui->updateDebugUnitFocus();
          }
      }
  }

  void Droids::DrawObjectSelection() const
  {
      int turn = timeManager->getTurn();
      if(turn < (int) m_game->states.size())
      {
          for(auto& iter: m_SelectedUnits)
          {
              if(m_game->states[turn].tiles.find(iter) != m_game->states[turn].tiles.end())
              {
                  auto tile = m_game->states[turn].tiles.at(iter);

                  DrawQuadAroundObj(parser::Mappable({tile.id, tile.x +2, tile.y +2}), glm::vec4(0.3, 0.0, 1.0f, 0.4));
              }
          }

          for(auto & iter : m_SelectedUnits)
          {
              if(m_game->states[turn].droids.find(iter) != m_game->states[turn].droids.end())
              {
                  auto & droid = m_game->states[turn].droids.at(iter);
                  DrawQuadAroundObj(parser::Mappable({droid.id, droid.x + 2, droid.y + 2}), glm::vec4(1.0f, 0.4, 0.4, 0.6));
              }
          }

          int focus = gui->getCurrentUnitFocus();

          if(focus >= 0)
          {
              if(m_game->states[turn].droids.find(focus) != m_game->states[turn].droids.end())
              {
                  auto& droid = m_game->states[turn].droids.at(focus);
                  DrawBoxAroundObj(parser::Mappable({droid.id, droid.x + 2, droid.y + 2}), glm::vec4(1.0f, 1.0f, 0.0f, 1.0f));
              }
          }
      }
  }

  std::list<IGUI::DebugOption> Droids::getDebugOptions()
  {
      return std::list<IGUI::DebugOption>({{"Units Selectable", true},
                                          {"Tiles Selectable", false}
                                         });

  }

  void Droids::DrawBoxAroundObj(const parser::Mappable& obj, const glm::vec4 &color) const
  {
      renderer->setColor(Color(color.r, color.g, color.b, color.a));
      renderer->drawLine(obj.x + 0.1f, obj.y + 0.1f, obj.x + 0.9, obj.y + 0.1);
      renderer->drawLine(obj.x + 0.1f, obj.y + 0.1f, obj.x + 0.1, obj.y + 0.9);
      renderer->drawLine(obj.x + 0.9f, obj.y + 0.1f, obj.x + 0.9, obj.y + 0.9);
      renderer->drawLine(obj.x + 0.1f, obj.y + 0.9f, obj.x + 0.9, obj.y + 0.9);
    }

  void Droids::DrawBoxAroundObj(const glm::vec2 topLeft, const int width, const int height, const glm::vec4 color) const
  {
      renderer->setColor(Color(color.r, color.g, color.b, color.a));
      renderer->drawLine(topLeft.x + 0.1f, topLeft.y + 0.1f, topLeft.x + (width - 0.1), topLeft.y + 0.1);
      renderer->drawLine(topLeft.x + 0.1f, topLeft.y + 0.1f, topLeft.x + 0.1, topLeft.y + (height - 0.1));
      renderer->drawLine(topLeft.x + (width - 0.1), topLeft.y + 0.1f, topLeft.x + (width - 0.1), topLeft.y + (height - 0.1));
      renderer->drawLine(topLeft.x + 0.1f, topLeft.y + (height - 0.1), topLeft.x + (width - 0.1), topLeft.y + (height - 0.1));

  }

  void Droids::DrawQuadAroundObj(const parser::Mappable& obj, const glm::vec4 &color) const
  {
      renderer->setColor( Color( color.r, color.g, color.b, color.a) );
      renderer->drawQuad(obj.x,obj.y,1,1);
  }

  void Droids::DrawQuadAroundObj(const glm::vec2 topLeft, const int width, const int height, const glm::vec4 color) const
  {
      renderer->setColor(Color(color.r, color.g, color.b, color.a));
          renderer->drawQuad(topLeft.x, topLeft.y, width, height);
  }

  std::list<int> Droids::getSelectedUnits()
  {
      return m_SelectedUnits;
  }

  glm::vec3 Droids::GetTeamColor(int owner) const
  {
    return owner == 1 ? glm::vec3(0.75f,1.0f,0.75f) : glm::vec3(0.75f,0.75f,1.0f);
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

      const int pieChartResolution = 100;
      const int pieChartRadius = 1.5;

      // player 0 health
      int interval = 0;
      glm::vec3 color = GetTeamColor(0);

      for(interval = 0; interval < m_Player0Hangars; interval++)
      {
          // bars for alive hangars
          // too dark, i'm doing it manually
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
          renderer->setColor(Color(color.r * 0.5, color.g * 0.5, color.b * 0.5, 1.0f));
          renderer->drawTexturedQuad((x + healthBarOffset - (healthWidth)/2) + (interval*healthUnitWidth),
                                    (y + (boxHeight/2) - (healthHeight/2)),
                                     healthUnitWidth, healthHeight - 0.2f, 1, "pipe_section");
      }

      for(;interval < m_NumHangers; interval ++)
      {
          // bars for alive hangars
          renderer->setColor(Color(color.r, color.g, color.b, 1.0f));
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


          // scrap chart
          {
              int curPlayer = (side == -1)?0:1;
              auto player = m_game->states[timeManager->getTurn()].players.find(curPlayer);

              if(player != m_game->states[timeManager->getTurn()].players.end())
              {
                  const float pieCenterX = (x +(side*boxOffset) + (side* boxWidth/2)) + (-side*8.0);
                  const float pieCenterY = (y + 1.8f);
                  float percentScrap = static_cast<float>(player->second.scrapAmount) / m_game->states[timeManager->getTurn()].maxScrap;
                  std::stringstream stream;
                  stream << player->second.scrapAmount << " / " << m_game->states[timeManager->getTurn()].maxScrap;

                  glm::vec3 col = (side == -1)?GetTeamColor(0):GetTeamColor(1);
                  renderer->setColor(Color(col.x, col.y, col.z, 1.0f));
                  renderer->drawLine(pieCenterX, pieCenterY, pieCenterX + side, pieCenterY + 1);
                  renderer->drawLine(pieCenterX + side, pieCenterY + 1, pieCenterX +side + (side*2.0), pieCenterY + 1);
                  renderer->drawText(pieCenterX + side + (side * 2.0), pieCenterY + 0.4, "Roboto", stream.str(), 1.8f,  (curPlayer)?(IRenderer::Right):(IRenderer::Left));
                  renderer->drawText(pieCenterX + side + (side *1.5),pieCenterY + 1.0f, "Roboto", "scrap", 2.0f, (curPlayer)?(IRenderer::Right):(IRenderer::Left));

                  renderer->setColor(Color(col.x, col.y, col.z, 1.0f));
                  renderer->drawCircle(pieCenterX, pieCenterY, pieChartRadius, percentScrap, pieChartResolution);

                  renderer->setColor(Color(col.x*0.5, col.y *0.5, col.z * 0.5, 1.0f));
                  renderer->drawCircle(pieCenterX, pieCenterY, pieChartRadius, 1 - percentScrap, pieChartResolution, 2*PI * percentScrap);

               }

          }


          // draw the health tank
          renderer->setColor(Color(1.0f, 1.0f, 1.0f, 1.0f));
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

  void Droids::DrawScrapAmount() const
  {

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

	// Look through each turn in the gamelog
	for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
    {
        PrepareTiles(state, *turn, *nextTurn);
        PrepareUnits(state, *turn, *nextTurn);

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

    PrepareLastFrame(m_game->states.size() - 1, *turn);
    animationEngine->buildAnimations(*turn);
    addFrame(*turn);
    timeManager->setNumTurns( timeManager->getNumTurns() + 1);

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
              }
          }

          if(sprite->m_Moves.empty())
          {
                sprite->m_Moves.push_back(MoveableSprite::Move(glm::vec2(unit.x, unit.y), glm::vec2(unit.x, unit.y)));
          }

		  sprite->addKeyFrame(new DrawSmoothSpriteProgressBar(sprite, 1.0f, 0.2f,
															  unit.healthLeft / (float)unit.maxHealth, glm::vec4(GetTeamColor(unit.owner),1.0)));
          turn.addAnimatable(sprite);

          turn[unit.id]["id"] = unit.id;
          turn[unit.id]["X"] = unit.x;
          turn[unit.id]["Y"] = unit.y;
          turn[unit.id]["owner"] = unit.owner;
          turn[unit.id]["variant"] = unit.variant;
          turn[unit.id]["attackLeft"] = unit.attacksLeft;
          turn[unit.id]["maxAttacks"] = unit.maxAttacks;
          turn[unit.id]["healthLeft"] = unit.healthLeft;
          turn[unit.id]["maxHealth"] = unit.maxHealth;
          turn[unit.id]["movementLeft"] = unit.movementLeft;
          turn[unit.id]["maxMovement"] = unit.maxMovement;
          turn[unit.id]["range"] = unit.range;
          turn[unit.id]["attack"] = unit.attack;
          turn[unit.id]["armor"] = unit.armor;
          turn[unit.id]["maxArmor"] = unit.maxArmor;
          turn[unit.id]["scrapWorth"] = unit.scrapWorth;
          turn[unit.id]["turnsToBeHacked"] = unit.turnsToBeHacked;
          turn[unit.id]["hackedTurnsLeft"] = unit.hackedTurnsLeft;
          turn[unit.id]["hackets"] = unit.hackets;
          turn[unit.id]["hacketsMax"] = unit.hacketsMax;
      }
  }

  void Droids::PrepareTiles(const int &frameNum, Frame &turn, Frame& nextTurn)
  {
      auto& tiles = m_game->states[frameNum].tiles;

      SmartPointer<MoveableSprite> sprite;

      for(auto & tile : tiles)
      {
          if(tile.second.turnsUntilAssembled == 1 && frameNum - 1 >= 0)
          {
              auto& prevState = m_game->states[frameNum - 1];

              if(prevState.tiles[tile.second.id].turnsUntilAssembled == 1)
              {
                  float h = sqrt( pow(3, 2) + pow(tile.second.y +3, 2));
                  float angle = asin( tile.second.y / h);
                  angle = 180/PI + 180;


                  sprite = new MoveableSprite("fireball");
                  sprite->addKeyFrame(new DrawSmoothMoveRotatedSprite(sprite, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f), angle));
                  sprite->m_Moves.push_back(MoveableSprite::Move(glm::vec2( tile.second.x, tile.second.y), glm::vec2(tile.second.x - 3, -3)));
                  turn.addAnimatable(sprite);
              }
          }

          if(tile.second.turnsUntilAssembled > 2 && tile.second.owner == 0 || tile.second.owner == 1)
          {
              SmartPointer<BaseSprite> reticle;
              reticle = new BaseSprite(glm::vec2(tile.second.x, tile.second.y), glm::vec2(1, 1), "med_reticle");
              glm::vec3 col = GetTeamColor(tile.second.owner);
              reticle->addKeyFrame(new DrawDeltaRotater(reticle, glm::vec4(col.x, col.y, col.z, 0.5)));
              turn.addAnimatable(reticle);
          }

          turn[tile.second.id]["x"] = tile.second.x;
          turn[tile.second.id]["y"] = tile.second.y;
          turn[tile.second.id]["id"] = tile.second.id;
          turn[tile.second.id]["owner"] = tile.second.owner;
          turn[tile.second.id]["turnsUntilAssembled"] = tile.second.turnsUntilAssembled;
          turn[tile.second.id]["variantToAssemble"] = tile.second.variantToAssemble;
      }
  }

  void Droids::PrepareLastFrame(const int &frameNum, Frame &turn)
  {
      std::string texture;
      auto& lastState = m_game->states[frameNum];

      for(auto & droid: lastState.droids)
      {
          switch(droid.second.variant)
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

          auto droidAnims = lastState.animations.find(droid.second.id);
          if(droidAnims == lastState.animations.end())
          {
              SmartPointer<BaseSprite> sprite = new BaseSprite(glm::vec2(droid.second.x, droid.second.y), glm::vec2(1,1), "texture");
              sprite->addKeyFrame(new DrawSprite(sprite, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f)));
              turn.addAnimatable(sprite);
          }
          else
          {
              bool died = false;

              for(auto& anim : droidAnims->second)
              {

                  if(anim->type == parser::ORBITALDROP)
                  {
                      died = true;
                  }
              }

              if(!died)
              {
                  SmartPointer<BaseSprite> sprite = new BaseSprite(glm::vec2(droid.second.x, droid.second.y), glm::vec2(1,1), "texture");
                  sprite->addKeyFrame(new DrawSprite(sprite, glm::vec4(1.0f, 1.0f, 1.0f, 1.0f)));
                  turn.addAnimatable(sprite);
              }
          }

      }
  }
} // visualizer

Q_EXPORT_PLUGIN2( Droids, visualizer::Droids );
