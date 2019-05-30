import arcade
from random import*
from math import*

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class AI(arcade.Sprite):

    def __init__(self):
        super().__init__('image/rouge.png', 0.3)
        self.speed = 1.5 * 100 / 60   # in tiles per second
        self.shoot = False
        self.reload_speed = 0.3 * 60  # in shoots per second
        self.reload = 0
        self.hp = 0
        self.center_x = randint(100, 4000)
        self.center_y = randint(100, 2900)
        self.range = 5 * 100



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

        # map, for better view press ctrl + F + 1
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

        # player sprite
        self.player_sprite = None

        # bullet sprite
        self.player_bullet_sprite = None

        # shooting variables
        self.shoot = False
        self.reload_speed = 0.3 * 60  # in shoots per second
        self.reload = 0
        self.bullet_range = 5 * 100

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

        for i in range(len(self.map)):
            if self.map[i] == 1:
                wall = arcade.Sprite('image/wall.png', 1)
                wall.center_x = i % self.map_length * 100 + 50
                wall.center_y = (len(self.map) - i - 1) // self.map_length * 100 + 50
                self.wall_list.append(wall)

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

        if (self.move_up or self.move_down) and (self.move_left or self.move_right):
            self.player_speed = 1.5 * sqrt(2)/2 * 100 / 60
        else:
            self.player_speed = 1.5 * 100 / 60

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.move_up = False
        if key == arcade.key.A:
            self.move_left = False
        if key == arcade.key.S:
            self.move_down = False
        if key == arcade.key.D:
            self.move_right = False
        if self.move_up or self.move_down:
            if not self.move_left or not self.move_right:
                self.player_speed = 1.5 * 100 / 60
        if self.move_left or self.move_right:
            if not self.move_up or not self.move_down:
                self.player_speed = 1.5 * 100 / 60

    def update(self, delta_time):

        self.player_list.update()

        if self.shoot and self.reload <= 0:
            arrow = arcade.Sprite('image/arrow.png', 0.2)
            self.reload += self.reload_speed

            arrow.angle = self.player_sprite.angle

            arrow.origin_x = self.player_sprite.center_x + 10 * cos(radians(arrow.angle))
            arrow.origin_y = self.player_sprite.center_y + 10 * sin(radians(arrow.angle))

            arrow.center_x = arrow.origin_x
            arrow.center_y = arrow.origin_y

            self.player_bullet_list.append(arrow)

        if self.reload > 0:
            self.reload -= 1

        for bullet in self.player_bullet_list:
            bullet.center_x += 15 * cos(radians(bullet.angle))
            bullet.center_y += 15 * sin(radians(bullet.angle))
            if (round(bullet.center_x - bullet.origin_x))^2 + (round(bullet.center_y - bullet.origin_y))^2 > self.bullet_range^2:
                bullet.kill()

        for wall in self.wall_list:
            wall_hit_list = arcade.check_for_collision_with_list(wall, self.player_bullet_list)
            for bullet in wall_hit_list:
                bullet.kill()

        physics_engine = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
        changed = False

        print(self.player_speed)
        print(self.move_up, self.move_down, self.move_left, self.move_right)

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

        if len(physics_engine) > 0:
            changed = False

            if self.player_sprite.right - physics_engine[0].left < physics_engine[0].top - self.player_sprite.bottom and self.player_sprite.right - physics_engine[0].left < self.player_sprite.top - physics_engine[0].bottom:
                if physics_engine[0].left < self.player_sprite.right and physics_engine[0].center_x > self.player_sprite.center_x:
                    self.player_sprite.right = physics_engine[0].left
                    physics_engine = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
            if physics_engine != []:
                if physics_engine[0].right - self.player_sprite.left < physics_engine[0].top - self.player_sprite.bottom and physics_engine[0].right - self.player_sprite.left < self.player_sprite.top - physics_engine[0].bottom:
                    if physics_engine[0].right > self.player_sprite.left and physics_engine[0].center_x < self.player_sprite.center_x:
                        self.player_sprite.left = physics_engine[0].right
                        physics_engine = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
            if physics_engine != []:
                if physics_engine[0].top > self.player_sprite.bottom and physics_engine[0].center_y < self.player_sprite.center_y:
                    self.player_sprite.bottom = physics_engine[0].top
                if physics_engine[0].bottom < self.player_sprite.top and physics_engine[0].center_y > self.player_sprite.center_y:
                    self.player_sprite.top = physics_engine[0].bottom

        self.view_left = self.player_sprite.center_x - 500
        self.view_bottom = self.player_sprite.center_y - 400

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
