import arcade
from math import*

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class MyGame(arcade.Window):

    def __init__(self):
        # initialize the screen
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, 'RPG game')

        # sprite lists
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.wall_list = None

        # player sprite
        self.player_sprite = None

        # bullet sprite
        self.player_bullet_sprite = None

        # physics engine
        self.physics_engine = None

        # manage the view point
        self.view_left = 0
        self.view_bottom = 0

        # setup the score
        self.score = 0

    def setup(self):

        # set background color
        arcade.set_background_color(arcade.color.WHITE)

        # Reset the view port
        self.view_left = 0
        self.view_bottom = 0

        # setup sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # reset the score
        self.score = 0

        # create the player
        self.player_sprite = arcade.Sprite('image/rouge.png', 0.3)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)

    def on_mouse_motion(self, x, y, dx, dy):
        if x - self.player_sprite.center_x == 0:
            if y > self.player_sprite.center_y:
                self.player_sprite.angle = 90
            else:
                self.player_sprite.angle = 270
        elif x > self.player_sprite.center_x:
            self.player_sprite.angle = degrees(atan((y - self.player_sprite.center_y)/(x - self.player_sprite.center_x)))
            print(degrees(atan((y - self.player_sprite.center_y)/(x - self.player_sprite.center_x))))
        else:
            self.player_sprite.angle = 180 + degrees(atan((y - self.player_sprite.center_y)/(x - self.player_sprite.center_x)))

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.player_bullet_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            arrow = arcade.Sprite('arrow.png', 0.2)

            self.player_bullet_list.append(self.player_bullet_sprite)

    def update(self, delta_time):
        self.player_list.update()
        self.player_bullet_list.update()

def main():
    window = MyGame()
    window.setup()
    arcade.run()

main()
