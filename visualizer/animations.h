#ifndef ANIMATIONS_H
#define ANIMATIONS_H

#include "droidsAnimatable.h"
#include <glm/glm.hpp>
#include <ctime>
#include <chrono>

namespace visualizer
{
	enum ProgressBarTextMode
	{
		Off,
		Percent,
		Value
	};

	void RenderProgressBar(const IRenderer& renderer,
						   float xPos, float yPos,
						   float width, float height,
                           float A, float B,
						   const Color& col, const Color& backgroundColor = Color(0,0,0,0.8f),
						   ProgressBarTextMode textMode = Off,
                           bool bDrawDivider = false);

	// NOTE: consider combining color sprite and DrawSprite since they are
	//    essentially the same, except that DrawSprite is drawn with white.
	class ColorSprite : public Anim
	{
	public:

		enum Fade
		{
			None,
			FadeIn,
			FadeOut
		};

		ColorSprite(const glm::vec4& c, Fade f = None) : m_color(c), m_fade(f)
		{
		}

	   void animate( const float& t, AnimData* d, IGame* game );

	private:
		glm::vec4 m_color;
		Fade m_fade;
	};

	/** @name DrawSprite
	  * @inherits ColorSprite
	  * @purpose Draws an unmoving sprite at the grid coordinates specified with
	  *     the color added to the textures color.
	  */
	class DrawSprite : public ColorSprite
	{
	public:
		DrawSprite( BaseSprite* sprite, const glm::vec4& c, Fade f = None) : ColorSprite(c,f), m_sprite(sprite) {}
		void animate( const float& t, AnimData* d, IGame* game );

	private:
		BaseSprite* m_sprite;
	};

	/** @name DrawRotatedSprite
	  * @inherits ColorSprite
	  * @purpose Draws an unmoving sprite at the grid coordinate with the color
	  *     added to the textures color. The texture will also be rotated by
	  *     the amount specified (in degrees).
	  */
	class DrawRotatedSprite :
		public ColorSprite
	{
	public:
		DrawRotatedSprite( BaseSprite* sprite, const glm::vec4& c, const float& rot ) :
			m_sprite(sprite),
			ColorSprite(c),
			m_rot(rot)
			{}

		void animate( const float& t, AnimData* d, IGame* game);

	private:
		const float m_rot;
		BaseSprite* m_sprite;
	};

	/** @name DrawSmoothMoveSprite
	  * @inherits Anim
	  * @purpose Will draw any MoveableSprite. These sprites contain a list
	  *     of moves to adjacent squares in a single turn. The animation engine
	  *     will interpolate over all these moves to move the sprite smoothly
	  *     in a single turn. These moves must be placed in
	  *     MoveableSprite::m_Moves before you try to render the animation.
	  *     WARNING - a MoveableSprite requires at least one valid move. This
	  *     can be to and from the same position should the object not move at
	  *     all that turn.
	  */
	class DrawSmoothMoveSprite :
		public ColorSprite
	{
	public:
		DrawSmoothMoveSprite(MoveableSprite * sprite, const glm::vec4& c, Fade f = None) : ColorSprite(c,f), m_Sprite(sprite) {}

		void animate( const float& t, AnimData* d, IGame* game );

	protected:

		MoveableSprite * m_Sprite;
		glm::vec2 m_pos;

	};

    class DrawSmoothMoveRotatedSprite :
        public ColorSprite
    {
    public:
        DrawSmoothMoveRotatedSprite(MoveableSprite * sprite, const glm::vec4& c, const float& rotation, Fade f = None) :
            ColorSprite(c),
            m_Sprite(sprite),
            m_Rotation(rotation)
            {}

        void animate( const float& t, AnimData* d, IGame* game );

    protected:
        MoveableSprite * m_Sprite;
        const float m_Rotation;
        glm::vec2 m_pos;
    };

    class DrawDeltaRotater :
        public ColorSprite
    {
    public:
        DrawDeltaRotater(BaseSprite * sprite, const glm::vec4& c) :
            ColorSprite(c),
            m_Sprite(sprite)
            {}

        void animate(const float& t, AnimData* d, IGame* game);

    private:
        BaseSprite * m_Sprite;
        static float m_Rotation;
    };

    class DrawDeltaScalar :
		public ColorSprite
    {
    public:
        DrawDeltaScalar(BaseSprite* sprite, const glm::vec4 c, const glm::vec2 start, const glm::vec2 end) :
            ColorSprite(c),
            m_Sprite(sprite),
            m_Start(start),
            m_End(end)
            {}

        void animate(const float& t, AnimData* d, IGame * game);

    private:
        BaseSprite* m_Sprite;
        glm::vec2 m_Start;
        glm::vec2 m_End;
        float m_Scale;
        std::chrono::steady_clock::time_point m_prev;
    };

	class DrawSmoothSpriteProgressBar : public DrawSmoothMoveSprite
	{
	public:

		DrawSmoothSpriteProgressBar(MoveableSprite * sprite,
									float width, float height, float percent,
									const glm::vec4& c,
									Fade f = None) :
			DrawSmoothMoveSprite(sprite,c,f), m_width(width), m_height(height), m_percent(percent)  {}


		void animate( const float& t, AnimData* d, IGame* game );

	private:
		float m_width;
		float m_height;
		float m_percent;
	};

	/** @name DrawAnimatedSprite
	  * @inherits Anim
	  * @prupose Will draw an animated sprite. Must know the number of frames
	  *   contained in the sprite to render correctly
	  */
	class DrawAnimatedSprite :
		public ColorSprite
	{
	public:
		DrawAnimatedSprite(AnimatedSprite* sprite, const glm::vec4& c, Fade f = None) :
			ColorSprite(c, f),
			m_Sprite(sprite)
			{}

        void animate( const float& t, AnimData* d, IGame* game );

	private:
		AnimatedSprite * m_Sprite;
	};

    /** @name DrawRotatedAnimatedSprite
     *  @inherits Anim
     *  @purpose Will draw a rotated animated sprite. Must know the number of frames
     *     contained in the sprite to render correctly
     */
    class DrawRotatedAnimatedSprite :
        public ColorSprite
    {
    public:
        DrawRotatedAnimatedSprite(AnimatedSprite* sprite, const glm::vec4& c, const float& degrees, Fade f = None) :
            ColorSprite(c, f),
            m_Sprite(sprite),
            m_Rotation(degrees)
            {}

        void animate( const float& t, AnimData* d, IGame* game);

    private:
        AnimatedSprite * m_Sprite;
        float m_Rotation;
    };

	/** @name DrawTextBox
	  * @inherits Anim
	  * @purpose Draws the TextBox to the screen.
	  */
	class DrawTextBox :
		public Anim
	{
	public:
		DrawTextBox(const std::string& text, const glm::vec2& pos, const glm::vec4& color,
				const float& size, IRenderer::Alignment align = IRenderer::Alignment::Center) :
			m_Text(text),
			m_Pos(pos),
			m_Color(color),
			m_Size(size),
			m_Alignment(align)
			{}

		void animate(const float &t, AnimData *d, IGame *game);

	private:
		std::string m_Text;
		glm::vec2 m_Pos;
		glm::vec4 m_Color;
		float m_Size;
		IRenderer::Alignment m_Alignment;
	};

	class DrawSplashScreen : public Anim
	{
	public:

		DrawSplashScreen(SplashScreen* screen) : m_SplashScreen(screen) {}

		void animate(const float &t, AnimData *d, IGame *game);

	private:
		SplashScreen* m_SplashScreen;
	};

	class DrawAnimatedMovingSprite :
		public ColorSprite
	{
	public:
		DrawAnimatedMovingSprite(MoveableSprite * sprite, const glm::vec4& c, const int numFrames, const float start) :
			ColorSprite(c),
			m_Sprite(sprite),
			m_numFrames(numFrames),
			m_startTime(start)
			{}

		void animate(const float &t, AnimData *d, IGame *game);

	private:
		MoveableSprite * m_Sprite;

		int m_numFrames;
		float m_startTime;
	};

}

#endif // ANIMATION_H
