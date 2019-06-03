import arcade
from random import*
from math import*

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class Archer(arcade.Sprite):

    def __init__(self):
        super().__init__('image/rouge.png', 0.3)
        self.speed = 1.5 * 100 / 60   # in tiles per second
        self.shoot = False
        self.reload_speed = 0.3 * 60  # in shoots per second
        self.reload = 0
        self.max_hp = 100
        self.hp = 100
        self.center_x = randint(100, 4000)
        self.center_y = randint(100, 2900)
        self.range = 5 * 100
        self.angle_change_restriction = 5 * 60
        self.turning_restriction = 0.15 * 60
        self.bullet_list = arcade.SpriteList()
        self.lock_on_adjustment_cooldown = 2 * 60
        self.lock_on_speed_x = 0
        self.lock_on_speed_y = 0

    def shooting(self):
        if self.reload <= 0:
            arrow = arcade.Sprite('image/arrow.png', 0.2)
            self.reload += self.reload_speed

            arrow.angle = self.angle

            arrow.origin_x = self.center_x + 10 * cos(radians(arrow.angle))
            arrow.origin_y = self.center_y + 10 * sin(radians(arrow.angle))

            arrow.center_x = arrow.origin_x
            arrow.center_y = arrow.origin_y

            self.bullet_list.append(arrow)

    def shooting_mechanics(self, wall_list):
        if self.reload > 0:
            self.reload -= 1

        for bullet in self.bullet_list:
            bullet.center_x += 10 * cos(radians(bullet.angle)) * 100 / 60
            bullet.center_y += 10 * sin(radians(bullet.angle)) * 100 / 60
            if (round(bullet.center_x - bullet.origin_x)) ^ 2 + (round(bullet.center_y - bullet.origin_y)) ^ 2 > self.range ^ 2:
                bullet.kill()

        for wall in wall_list:
            wall_hit_list = arcade.check_for_collision_with_list(wall, self.bullet_list)
            for bullet in wall_hit_list:
                bullet.kill()


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
        self.enemy_hp_list = None

        # map, for better view press ctrl + F + 1
        self.map = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
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
            1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,
            1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,
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
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.map_length = 41
        self.map_width = 30

        # player sprite
        self.player_sprite = None
        self.player_hp_bar_sprite = None
        self.player_hp = 100
        self.player_hp_max = 100
        self.rejuvenate_cooldown = 5 * 60

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
        self.enemy_hp_list = arcade.SpriteList()

        # reset the score
        self.score = 0

        # create the player
        self.player_sprite = arcade.Sprite('image/rouge.png', 0.3)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)
        self.player_hp_bar_sprite = arcade.Sprite('image/red_hp_bar.png', 1)

        for i in range(len(self.map)):
            if self.map[i] == 1:
                wall = arcade.Sprite('image/wall.png', 1)
                wall.center_x = i % self.map_length * 100 + 50
                wall.center_y = (len(self.map) - i - 1) // self.map_length * 100 + 50
                self.wall_list.append(wall)

        # create AI
        for i in range(10):
            bot = Archer()
            hit_list = arcade.check_for_collision_with_list(bot, self.wall_list)
            while hit_list != []:
                bot = Archer()
                hit_list = arcade.check_for_collision_with_list(bot, self.wall_list)
            self.enemy_list.append(bot)
            hp_bar_sprite = arcade.Sprite('image/hp_bar.png', 1)
            self.enemy_hp_list.append(hp_bar_sprite)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.player_hp > 0:
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
        self.enemy_list.draw()
        self.enemy_hp_list.draw()
        self.player_hp_bar_sprite.draw()
        for enemy in self.enemy_list:
            enemy.bullet_list.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10 + self.view_left, 10 + self.view_bottom, arcade.color.WHITE, 18)
        if self.player_hp <= 0:
            arcade.draw_rectangle_filled(SCREEN_WIDTH/2 + self.view_left, SCREEN_HEIGHT/2 + self.view_bottom, 200, 100, arcade.color.BLACK)
            output = f"YOU DIED"
            arcade.draw_text(output, SCREEN_WIDTH/2 + self.view_left, SCREEN_HEIGHT/2 + self.view_bottom, arcade.color.WHITE, 32, 0, align='center', anchor_x='center', anchor_y='bottom')
            output = f'Score: {self.score}'
            arcade.draw_text(output, SCREEN_WIDTH / 2 + self.view_left, SCREEN_HEIGHT / 2 - 5 + self.view_bottom, arcade.color.WHITE, 18, 0, align='center', anchor_x='center', anchor_y='top')

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot = True

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_speed = 10

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
            if not self.move_left and not self.move_right:
                self.player_speed = 1.5 * 100 / 60
        if self.move_left or self.move_right:
            if not self.move_up and not self.move_down:
                self.player_speed = 1.5 * 100 / 60

    def update(self, delta_time):

        if self.player_hp > 0:

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

            if self.shoot:
                self.rejuvenate_cooldown = 5 * 60

            for bullet in self.player_bullet_list:
                bullet.center_x += 10 * cos(radians(bullet.angle)) * 100 / 60
                bullet.center_y += 10 * sin(radians(bullet.angle)) * 100 / 60
                if (round(bullet.center_x - bullet.origin_x))^2 + (round(bullet.center_y - bullet.origin_y))^2 > self.bullet_range^2:
                    bullet.kill()

            for wall in self.wall_list:
                wall_hit_list = arcade.check_for_collision_with_list(wall, self.player_bullet_list)
                for bullet in wall_hit_list:
                    bullet.kill()

            physics_engine = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
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

            self.player_hp_bar_sprite.width = self.player_hp
            self.player_hp_bar_sprite.center_x = self.player_sprite.center_x
            self.player_hp_bar_sprite.center_y = self.player_sprite.top + 5

            in_combat = False

            for enemy in self.enemy_list:

                if -400 <= self.player_sprite.center_x - enemy.center_x <= 400 and -300 <= self.player_sprite.center_y - enemy.center_y <= 300 and enemy.turning_restriction == 0:
                    enemy.shooting()
                    if enemy.center_x - self.player_sprite.center_x == 0:
                        if enemy.center_y < self.player_sprite.center_y:
                            enemy.angle = 90
                        elif enemy.center_y > self.player_sprite.center_y:
                            enemy.angle = 270
                    elif self.player_sprite.center_x > enemy.center_x:
                        enemy.angle = degrees(atan((self.player_sprite.center_y - enemy.center_y) / (
                                self.player_sprite.center_x - enemy.center_x)))
                    else:
                        enemy.angle = 180 + degrees(atan((self.player_sprite.center_y - enemy.center_y) / (
                                self.player_sprite.center_x - enemy.center_x)))

                elif enemy.angle_change_restriction <= 0:
                    enemy.angle_change_restriction = 10 * 60
                    angle = randint(0, 360)
                    enemy.angle = angle

                enemy.angle_change_restriction -= 1
                if enemy.turning_restriction > 0:
                    enemy.turning_restriction -= 1
                if enemy.turning_restriction == 1:
                    enemy.angle += randint(-60, 60)

                if -300 <= self.player_sprite.center_x - enemy.center_x <= 300 and -200 <= self.player_sprite.center_y - enemy.center_y <= 200 and enemy.turning_restriction == 0:
                    enemy.speed = 0
                    if not self.move_up and not self.move_down and not self.move_left and not self.move_right and enemy.lock_on_adjustment_cooldown <= 0:
                        enemy.lock_on_speed_x = randrange(-15, 15) / 10 * 100 / 60
                        enemy.lock_on_speed_y = randrange(-15, 15) / 10 * 100 / 60
                        enemy.lock_on_adjustment_cooldown = 3 * 60
                    enemy.center_x += enemy.lock_on_speed_x
                    enemy.center_y += enemy.lock_on_speed_y
                    enemy.lock_on_adjustment_cooldown -= 1

                else:
                    enemy.speed = 1.5 * 100 / 60

                physics_engine_enemy = arcade.check_for_collision_with_list(enemy, self.wall_list)

                if physics_engine_enemy != []:
                    if enemy.turning_restriction <= 0:
                        if -400 <= self.player_sprite.center_x - enemy.center_x <= 400 and -300 <= self.player_sprite.center_y - enemy.center_y <= 300:
                            enemy.speed = 0
                        else:
                            enemy.speed = 1.5 * 100 / 60
                            enemy.turning_restriction = 0.15 * 60
                            enemy.angle = 180 + enemy.angle
                    if -300 <= self.player_sprite.center_x - enemy.center_x <= 300 and -200 <= self.player_sprite.center_y - enemy.center_y <= 200:
                        enemy.lock_on_speed_x *= -1
                        enemy.lock_on_speed_y *= -1
                        enemy.lock_on_adjustment_cooldown = 5 * 60

                enemy.center_x += enemy.speed * cos(radians(enemy.angle))
                enemy.center_y += enemy.speed * sin(radians(enemy.angle))

                for i in range(len(self.enemy_hp_list)):
                    self.enemy_hp_list[i].center_x = self.enemy_list[i].center_x
                    self.enemy_hp_list[i].center_y = self.enemy_list[i].top + 5
                self.enemy_hp_list.update()

                enemy.shooting_mechanics(self.wall_list)
                hit_list = arcade.check_for_collision_with_list(self.player_sprite, enemy.bullet_list)
                for bullet in hit_list:
                    self.player_hp -= 10
                    self.rejuvenate_cooldown = 5 * 60
                    bullet.kill()

                if hit_list != []:
                    in_combat = True

                self.player_hp_bar_sprite.width = self.player_hp / self.player_hp_max * 100

            if not self.shoot and not in_combat:
                self.rejuvenate_cooldown -= 1
                if self.rejuvenate_cooldown <= 0 and self.player_hp < self.player_hp_max:
                    self.player_hp += 0.5
                if self.player_hp > self.player_hp_max:
                    self.player_hp = self.player_hp_max

            for bullet in self.player_bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

                for enemy in hit_list:
                    bullet.kill()
                    enemy.hp -= 10
                    index = 0
                    for i in range(len(self.enemy_list)):
                        if self.enemy_list[i] == hit_list[0]:
                            index = i
                    self.enemy_hp_list[index].width = enemy.hp / enemy.max_hp * 100
                    if enemy.hp <= 0:
                        enemy.kill()
                        self.enemy_hp_list[index].kill()
                        self.score += 100



def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()