#ifndef DROIDS_ANIMATABLE_H
#define DROIDS_ANIMATABLE_H

//#include "marsAnimatable.h"
#include "irenderer.h"
#include "parser/structures.h"

#include "math.h"
#include <glm/glm.hpp>

namespace visualizer
{
	/** @name BaseSprite
	  * @inherits Animatable
	  * @purpose this object is a container for the sprite data of an immobile sprite.
	  *      The position and scale vectors must be set for Anim interfaces to render
	  *      correctly.
	  */
    struct  BaseSprite : public Animatable
	{
		BaseSprite(const glm::vec2& pos, const glm::vec2& scale, const string& sprite, const string& tag = "") :
			m_pos(pos), m_scale(scale), m_sprite(sprite), Animatable(tag)  {}

		glm::vec2 m_pos;
		glm::vec2 m_scale;
		string m_sprite;
	};


	/** @name BaseSprite
	  * @inherits Animatable
	  * @purpose this object is a container for the sprite data of a moving object.
	  *      Each move between adjacent squares must be placed into the m_Moves
	  *      vector.
	  *      WARNING - at least 1 Move must be in the m_Moves vector for the Anim
	  *      structures to render it correctly.
	  */
	struct MoveableSprite :
		public BaseSprite
	{
		MoveableSprite(const string& sprite, const glm::vec2& scale = glm::vec2(1.0f)) : BaseSprite(glm::vec2(0.0f),scale,sprite) {}

		struct Move
		{
			Move() {}
			Move(const glm::vec2& t, const glm::vec2&f) :
				to(t),
				from(f)
				{}

			glm::vec2 to;
			glm::vec2 from;
		};

		std::vector<Move> m_Moves;
	};

	/** @name AnimatedSprite
	  * @inherits Animatable
	  * @purpose this object is a container for the sprite data of an
	  *    animated sprite. needs the sprite name and the number of frames.
	  */
	struct AnimatedSprite :
		public BaseSprite
	{
		AnimatedSprite(const glm::vec2& pos, const glm::vec2& scale, const std::string& sprite, const int& frames, bool singleFrame = false) :
			BaseSprite(pos, scale, sprite),
			m_Frames(frames), m_SingleFrame(singleFrame)
			{}

		int m_Frames;
		bool m_SingleFrame;
	};

	struct SplashScreen : public Animatable
	{
		SplashScreen(const string& reason, const glm::vec3& col, int w, int h) :
			winReason(reason), color(col), width(w), height(h) {}

		string winReason;
		glm::vec3 color;
		int width;
		int height;
	};

} // visualizer

#endif // DROIDS_ANIMATABLE_H
