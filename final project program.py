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

        # map
        self.map = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1,
            1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.map_length = 41
        self.map_width = 30
        print(len(self.map))

        # player sprite
        self.player_sprite = None

        # bullet sprite
        self.player_bullet_sprite = None

        # physics engine
        self.physics_engine = None

        # shooting variables
        self.shoot = False
        self.reload_speed = 0.3 * 60  # in shoots per second
        self.reload = 0

        # manage the view point
        self.view_left = 0
        self.view_bottom = 0

        # setup the score
        self.score = 0

        # moving variables
        self.player_speed = 1.5 * 100 / 60  # in tiles per second
        self.move_up = False
        self.move_down = False
        self.move_right = False
        self.move_left = False

    def setup(self):

        # set background color
        arcade.set_background_color(arcade.color.AMAZON)

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

        '''
        # read the map
        map = arcade.read_tiled_map("map.tmx", 1)
        self.wall_list = arcade.generate_sprites(map, 'map', 1)
        print(self.wall_list)
        '''
        for i in range(len(self.map)):
            if self.map[i] == 1:
                wall = arcade.Sprite('image/wall.png', 1)
                wall.center_x = i % self.map_length * 100 + 50
                wall.center_y = (len(self.map) - i - 1) // self.map_length * 100 + 50
                self.wall_list.append(wall)
                print(i // 10 * 100 + 50)
                print(i)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_mouse_motion(self, x, y, dx, dy):
        if x + self.view_left - self.player_sprite.center_x == 0:
            if y + self.view_bottom > self.player_sprite.center_y:
                self.player_sprite.angle = 90
            else:
                self.player_sprite.angle = 270
        elif x + self.view_left > self.player_sprite.center_x:
            self.player_sprite.angle = degrees(atan((y + self.view_bottom - self.player_sprite.center_y)/(x + self.view_left - self.player_sprite.center_x)))
        else:
            self.player_sprite.angle = 180 + degrees(atan((y + self.view_bottom - self.player_sprite.center_y)/(x + self.view_left - self.player_sprite.center_x)))

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.player_bullet_list.draw()
        self.wall_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.move_up = True
        if key == arcade.key.A:
            self.move_left = True
        if key == arcade.key.S:
            self.move_down = True
        if key == arcade.key.D:
            self.move_right = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.move_up = False
        if key == arcade.key.A:
            self.move_left = False
        if key == arcade.key.S:
            self.move_down = False
        if key == arcade.key.D:
            self.move_right = False

    def update(self, delta_time):

        self.player_list.update()

        self.physics_engine.update()

        if self.shoot and self.reload <= 0:
            arrow = arcade.Sprite('image/arrow.png', 0.2)
            self.reload += self.reload_speed

            arrow.angle = self.player_sprite.angle

            arrow.center_x = self.player_sprite.center_x + 10 * cos(radians(arrow.angle))
            arrow.center_y = self.player_sprite.center_y + 10 * sin(radians(arrow.angle))

            self.player_bullet_list.append(arrow)

        if self.reload > 0:
            self.reload -= 1

        for bullet in self.player_bullet_list:
            bullet.center_x += 15 * cos(radians(bullet.angle))
            bullet.center_y += 15 * sin(radians(bullet.angle))

        for wall in self.wall_list:
            wall_hit_list = arcade.check_for_collision_with_list(wall, self.player_bullet_list)
            for bullet in wall_hit_list:
                bullet.kill()

        changed = False
        if self.move_up:
            self.view_bottom += self.player_speed
            self.player_sprite.center_y += self.player_speed
            changed = True
        if self.move_down:
            self.view_bottom -= self.player_speed
            self.player_sprite.center_y -= self.player_speed
            changed = True
        if self.move_left:
            self.view_left -= self.player_speed
            self.player_sprite.center_x -= self.player_speed
            changed = True
        if self.move_right:
            self.view_left += self.player_speed
            self.player_sprite.center_x += self.player_speed
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom - 1)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()
