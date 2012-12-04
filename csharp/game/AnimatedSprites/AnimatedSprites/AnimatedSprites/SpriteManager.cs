using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Audio;
using Microsoft.Xna.Framework.Content;
using Microsoft.Xna.Framework.GamerServices;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using Microsoft.Xna.Framework.Media;


namespace AnimatedSprites
{
    /// <summary>
    /// This is a game component that implements IUpdateable.
    /// </summary>
    public class SpriteManager : Microsoft.Xna.Framework.DrawableGameComponent
    {
        SpriteBatch spriteBatch;
        UserControlledSprite player;
        List<Sprite> spriteList = new List<Sprite>();

        public SpriteManager(Game game)
            : base(game)
        {
            // TODO: Construct any child components here
        }

        /// <summary>
        /// Allows the game component to perform any initialization it needs to before starting
        /// to run.  This is where it can query for any required services and load content.
        /// </summary>
        public override void Initialize()
        {
            // TODO: Add your initialization code here

            base.Initialize();
        }

        protected override void LoadContent()
        {
            spriteBatch = new SpriteBatch(Game.GraphicsDevice);

            player = new UserControlledSprite(
                Game.Content.Load<Texture2D>(@"images/threerings"),
                Vector2.Zero, new Point(75, 75), 10, new Point(0, 0),
                new Point(6, 8), new Vector2(6, 6));

            spriteList.Add(new AutomatedSprite(
                Game.Content.Load<Texture2D>(@"images/skullball"),
                new Vector2(150, 150), new Point(75, 75), 10, new Point(0, 0),
                new Point(6, 8), Vector2.Zero));

            spriteList.Add(new AutomatedSprite(
                Game.Content.Load<Texture2D>(@"images/skullball"),
                new Vector2(300, 150), new Point(75, 75), 10, new Point(0, 0),
                new Point(6, 8), Vector2.Zero));

            spriteList.Add(new AutomatedSprite(
                Game.Content.Load<Texture2D>(@"images/skullball"),
                new Vector2(150, 300), new Point(75, 75), 10, new Point(0, 0),
                new Point(6, 8), Vector2.Zero));

            spriteList.Add(new AutomatedSprite(
                Game.Content.Load<Texture2D>(@"images/skullball"),
                new Vector2(600, 400), new Point(75, 75), 10, new Point(0, 0),
                new Point(6, 8), Vector2.Zero));

            
            base.LoadContent();
        }
        /// <summary>
        /// Allows the game component to update itself.
        /// </summary>
        /// <param name="gameTime">Provides a snapshot of timing values.</param>
        public override void Update(GameTime gameTime)
        {
            // TODO: Add your update code here
            player.Update(gameTime, Game.Window.ClientBounds);

            foreach (Sprite s in spriteList)
            {
                s.Update(gameTime, Game.Window.ClientBounds);
            }

            base.Update(gameTime);
        }

        public override void Draw(GameTime gameTime)
        {
            spriteBatch.Begin(SpriteSortMode.FrontToBack, BlendState.AlphaBlend);

            player.Draw(gameTime, spriteBatch);

            foreach (Sprite s in spriteList)
                s.Draw(gameTime, spriteBatch);
            spriteBatch.End();

            base.Draw(gameTime);
        }
    }
}
