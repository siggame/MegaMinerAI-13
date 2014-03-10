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
	//const Input& input = gui->getInput();

	RenderGrid();
    
    // Handle player input here
  }

  void Droids::postDraw()
  {
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
	  renderer->drawTexturedQuad(0,0,m_mapWidth,m_mapHeight,4.0f,"grid");

	  // Draw horizontal lines
	  renderer->setColor(Color(0.0f,0.0f,0.0f,1.0f));
	  for(int i = 0; i < m_mapHeight; i++)
	  {
		  renderer->drawLine(0,i,m_mapWidth,i,1.0f);
	  }

	  // Draw vertical lines
	  for(int i = 0; i < m_mapWidth; i++)
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
	renderer->setCamera( 0, 0, m_mapWidth, m_mapHeight );
	renderer->setGridDimensions( m_mapWidth, m_mapHeight );
 
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

	  // Do stuff here

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

} // visualizer

Q_EXPORT_PLUGIN2( Droids, visualizer::Droids );
