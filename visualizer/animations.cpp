#include "animations.h"
#include "droids.h"
#include <iomanip>

namespace visualizer
{
	void RenderProgressBar(const IRenderer& renderer,
					   float xPos, float yPos,
					   float width, float height,
					   float A, float B,
					   const Color& col, const Color& backgroundColor,
					   ProgressBarTextMode textMode,
					   bool bDrawDivider)
	{
		float percent = A / B;
		float leftWidth = percent * width;

		renderer.setColor(col);
		renderer.drawQuad(xPos,yPos, leftWidth, height);

		// Render the health bars
		renderer.setColor(backgroundColor);
		renderer.drawQuad(xPos + width,yPos, -(1.0f - percent) * width, height); // height

		if(textMode != Off)
		{
			ostringstream stream;
			float middle = (xPos + (width / 2.0f));
			renderer.setColor(Color(1.0f,1.0f,1.0f,1.0f));
			if(textMode == Percent)
			{
				stream << fixed << setprecision(2) << percent * 100 << '%';
			}
			else
			{
				stream << A << "/" << B;
			}

			renderer.drawText(middle,yPos - 0.1f,"Roboto",stream.str(),5.0f*height,IRenderer::Center);
		}

		if(bDrawDivider)
		{
			// todo: this needs to be changed
			renderer.setColor(Color(0.0f,0.0f,0.0f,1.0f));
			renderer.drawQuad(xPos + leftWidth,yPos, 0.2f, height);
		}
	}

	void ColorSprite::animate(const float &t, AnimData*, IGame *game)
	{
		float alpha = m_color.a;
		if(m_fade != None)
		{
			alpha *= t;

			if(m_fade == FadeOut)
			{
				alpha = m_color.a - alpha;
			}
		}

		game->renderer->setColor( Color(m_color.r, m_color.g, m_color.b, alpha) );
	}

	DrawProgressBar::DrawProgressBar(const glm::vec2& pos, float width, float height, float percent) :
		m_pos(pos), m_width(width), m_height(height), m_percent(percent)
	{
	}

	DrawProgressBar::DrawProgressBar(float width, float height, float percent) :
		m_width(width), m_height(height), m_percent(percent)
	{
	}

	void DrawProgressBar::animate(const float &t, AnimData* d, IGame *game)
	{
		RenderProgressBar(*game->renderer,m_pos.x,m_pos.y,m_width,m_height,m_percent,1.0f,Color(1.0f,0.0f,0.0f,0.5f));
	}

	void DrawSmoothSpriteProgressBar::animate(const float &t, AnimData *d, IGame *game)
	{
		DrawFlippedSmoothMoveSprite::animate(t,d,game);

		m_pProgressBar->SetPos(m_pos + glm::vec2(0.0f,-0.1f));
		m_pProgressBar->animate(t,d,game);
	}

	void DrawSprite::animate(const float &t, AnimData *d, IGame *game)
	{
		ColorSprite::animate(t,d,game);
		game->renderer->drawTexturedQuad(m_sprite->m_pos.x, m_sprite->m_pos.y, m_sprite->m_scale.x, m_sprite->m_scale.y,1.0f,m_sprite->m_sprite);
	}

	void DrawRotatedSprite::animate(const float &t, AnimData *d, IGame *game)
	{
		ColorSprite::animate(t,d,game);
		game->renderer->drawRotatedTexturedQuad(m_sprite->m_pos.x, m_sprite->m_pos.y,
				  m_sprite->m_scale.x, m_sprite->m_scale.y, 1.0f, m_rot, m_sprite->m_sprite);
	}

	void DrawSmoothMoveSprite::animate(const float &t, AnimData *d, IGame *game)
	{
		unsigned int index = (unsigned int)(m_Sprite->m_Moves.size() * t);
		float subT = m_Sprite->m_Moves.size() * t - index;
		MoveableSprite::Move& thisMove = m_Sprite->m_Moves[index];

		glm::vec2 diff = thisMove.to - thisMove.from;
		m_pos = thisMove.from + diff * subT;

		ColorSprite::animate(t, d, game);
	}

	void DrawFlippedSmoothMoveSprite::animate(const float &t, AnimData *d, IGame *game)
	{
		DrawSmoothMoveSprite::animate(t, d, game);
		game->renderer->drawTexturedQuad(m_pos.x, m_pos.y, m_Sprite->m_scale.x, m_Sprite->m_scale.y, 1.0f, m_Sprite->m_sprite, m_Flipped);
	}

	void DrawRotatedSmoothMoveSprite::animate(const float &t, AnimData *d, IGame *game)
	{
		DrawSmoothMoveSprite::animate(t, d, game);
		game->renderer->drawRotatedTexturedQuad(m_pos.x, m_pos.y, m_Sprite->m_scale.x, m_Sprite->m_scale.y, 1.0f, m_angle, m_Sprite->m_sprite);
	}

	void DrawAnimatedSprite::animate(const float &t, AnimData*d, IGame* game)
	{
		ColorSprite::animate(t, d, game);

		float animTime = m_Sprite->m_SingleFrame ? t : 1.0f;
		game->renderer->drawAnimQuad( m_Sprite->m_pos.x, m_Sprite->m_pos.y, m_Sprite->m_scale.x, m_Sprite->m_scale.y, m_Sprite->m_sprite , (int)(m_Sprite->m_Frames * animTime));

		//game->renderer->drawProgressBar()
	}

	void DrawTextBox::animate(const float &, AnimData*, IGame* game)
	{
		game->renderer->setColor(Color(m_Color.r, m_Color.g, m_Color.b, m_Color.a));

		game->renderer->drawText(m_Pos.x, m_Pos.y, "Roboto", m_Text, m_Size, m_Alignment);
	}

	void DrawSplashScreen::animate(const float &t, AnimData*, IGame *game)
	{
		if(game->options->getNumber("Enable Victory Screen") > 0.0f)
		{
			//game->timeManager->setSpeed(1 - t);

			game->renderer->setColor(Color(1.0f,1.0f,1.0f,0.8f * t));

			game->renderer->drawQuad(0.0f,0.0f,m_SplashScreen->width,m_SplashScreen->height);

			game->renderer->setColor(Color(m_SplashScreen->color.r,m_SplashScreen->color.g,m_SplashScreen->color.b,1.0f));
			game->renderer->drawText(m_SplashScreen->width / 2.0f,
									 m_SplashScreen->height / 2.0f,
									 "Roboto",
									 m_SplashScreen->winReason,8.0f,
									 IRenderer::Center);

			/*if(game->timeManager->getSpeed() >= 0.0f && game->timeManager->getSpeed() <= 0.01f )
			{
				game->timeManager->setSpeed(1.0f);
			}*/
		}
	}

}
