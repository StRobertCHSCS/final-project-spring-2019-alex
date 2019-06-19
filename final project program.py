import arcade
from random import*
from math import*

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class Archer(arcade.Sprite):

    def __init__(self):

        # variables for enemy archers
        super().__init__('image/rouge.png', 0.3)
        self.speed = 1.5 * 100 / 60   # in tiles per second
        self.shoot = False
        self.reload_speed = 0.3 * 60  # in shoots per second
        self.reload = 0
        self.max_hp = 100
        self.hp = 100
        self.center_x = randint(100, 4000)
        self.center_y = randint(100, 2900)
        self.range = 8 * 100
        self.angle_change_restriction = 5 * 60
        self.turning_restriction = 0.15 * 60
        self.bullet_list = arcade.SpriteList()
        self.lock_on_adjustment_cooldown = 2 * 60
        self.lock_on_speed_x = 0
        self.lock_on_speed_y = 0
        self.bullet_speed = 10
        self.damage = 10

    def shooting(self):

        # check for the reload time
        if self.reload <= 0:

            # made a sprite of arrow and reset the reload speed
            arrow = arcade.Sprite('image/arrow.png', 0.2)
            self.reload += self.reload_speed

            # set the angle of the arrow to the angle of the enemy
            arrow.angle = self.angle

            # create the arrow in front of the player
            arrow.origin_x = self.center_x + self.bullet_speed * cos(radians(arrow.angle))
            arrow.origin_y = self.center_y + self.bullet_speed * sin(radians(arrow.angle))

            # set the origin coordinate of the arrow
            arrow.center_x = arrow.origin_x
            arrow.center_y = arrow.origin_y

            # append it into the bullet list of the enemy
            self.bullet_list.append(arrow)

    def shooting_mechanics(self, wall_list):

        # reduce the reload time
        if self.reload > 0:
            self.reload -= 1

        # make the bullet move based on the speed and angle, and determine if it has reached its range or not
        for bullet in self.bullet_list:
            bullet.center_x += self.bullet_speed * cos(radians(bullet.angle)) * 100 / 60
            bullet.center_y += self.bullet_speed * sin(radians(bullet.angle)) * 100 / 60
            if (round(bullet.center_x - bullet.origin_x)) ** 2 + (round(bullet.center_y - bullet.origin_y)) ** 2 > self.range ** 2:
                bullet.kill()

        # determine if the bullet has hit the wall
        for wall in wall_list:
            wall_hit_list = arcade.check_for_collision_with_list(wall, self.bullet_list)
            for bullet in wall_hit_list:
                bullet.kill()


class Mage(arcade.Sprite):

    def __init__(self):

        # variables for enemy archers
        super().__init__('image/mage.png', 0.2)
        self.speed = 1.5 * 100 / 60   # in tiles per second
        self.shoot = False
        self.reload_speed = 0.75 * 60  # in shoots per second
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
        self.bullet_speed = 5
        self.damage = 35

    def shooting(self):

        # check for the reload time
        if self.reload <= 0:

            # made a sprite of arrow and reset the reload speed
            arrow = arcade.Sprite('image/fireball.png', 0.35)
            angle_change = 0
            while angle_change == 0:
                angle_change = randrange(-10, 10)
            self.angle += angle_change
            self.reload += self.reload_speed

            # set the angle of the arrow to the angle of the enemy
            arrow.angle = self.angle

            # create the arrow in front of the player
            arrow.origin_x = self.center_x + self.bullet_speed * cos(radians(arrow.angle))
            arrow.origin_y = self.center_y + self.bullet_speed * sin(radians(arrow.angle))

            # set the origin coordinate of the arrow
            arrow.center_x = arrow.origin_x
            arrow.center_y = arrow.origin_y

            # append it into the bullet list of the enemy
            self.bullet_list.append(arrow)

    def shooting_mechanics(self, wall_list):

        # reduce the reload time
        if self.reload > 0:
            self.reload -= 1

        # make the bullet move based on the speed and angle, and determine if it has reached its range or not
        for bullet in self.bullet_list:
            bullet.center_x += self.bullet_speed * cos(radians(bullet.angle)) * 100 / 60
            bullet.center_y += self.bullet_speed * sin(radians(bullet.angle)) * 100 / 60
            if (round(bullet.center_x - bullet.origin_x)) ** 2 + (round(bullet.center_y - bullet.origin_y)) ** 2 > self.range ** 2:
                bullet.kill()

        # determine if the bullet has hit the wall
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
        if randint(0, 2) == 0:
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
        else:
            self.map = [
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1,
                1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        self.map_length = 41
        self.map_width = 30

        # player sprite
        self.player_sprite = None
        self.player_hp_bar_sprite = None
        self.player_hp = 100
        self.player_hp_max = 100
        self.rejuvenate_cooldown = 5 * 60
        self.damage = 0
        self.player_hero = None

        # bullet sprite
        self.player_bullet_sprite = None

        # shooting variables
        self.shoot = False
        self.reload_speed = 0.3 * 60  # in shoots per second
        self.reload = 0
        self.bullet_range = 5 * 100
        self.bullet_speed = 0
        self.bullet_sprite = None

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

        # game state variable
        self.game_state = 1
        self.archer = None
        self.mage = None

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

        # reset everything
        self.score = 0
        self.player_hp = 100
        self.game_state = 1
        arcade.set_viewport(self.view_left,
                            SCREEN_WIDTH + self.view_left - 1,
                            self.view_bottom,
                            SCREEN_HEIGHT + self.view_bottom - 1)

        # create the wall
        for i in range(len(self.map)):
            if self.map[i] == 1:
                wall = arcade.Sprite('image/wall.png', 1)
                wall.center_x = i % self.map_length * 100 + 50
                wall.center_y = (len(self.map) - i - 1) // self.map_length * 100 + 50
                self.wall_list.append(wall)

        # create AI
        for i in range(10):
            if randint(0, 2) == 0:
                bot = Archer()
            else:
                bot = Mage()
            hit_list = arcade.check_for_collision_with_list(bot, self.wall_list)
            while hit_list != [] or self.view_left <= bot.center_x <= self.view_left + SCREEN_WIDTH or self.view_bottom <= bot.center_y <= self.view_bottom + SCREEN_HEIGHT:
                if randint(0, 2) == 0:
                    bot = Archer()
                else:
                    bot = Mage()
                hit_list = arcade.check_for_collision_with_list(bot, self.wall_list)
            self.enemy_list.append(bot)
            hp_bar_sprite = arcade.Sprite('image/hp_bar.png', 1)
            self.enemy_hp_list.append(hp_bar_sprite)

    def on_mouse_motion(self, x, y, dx, dy):

        # check to see if player is still alive
        if self.player_hp > 0 and self.game_state == 2:

            # set the angle to 90 or 270 degrees in certain special case
            if x + self.view_left - self.player_sprite.center_x == 0:
                if y + self.view_bottom > self.player_sprite.center_y:
                    self.player_sprite.angle = 90
                else:
                    self.player_sprite.angle = 270

            # set the angle based on the position of the mouse icon
            elif x + self.view_left > self.player_sprite.center_x:
                self.player_sprite.angle = degrees(atan((y + self.view_bottom - self.player_sprite.center_y)/(x + self.view_left - self.player_sprite.center_x)))
            else:
                self.player_sprite.angle = 180 + degrees(atan((y + self.view_bottom - self.player_sprite.center_y)/(x + self.view_left - self.player_sprite.center_x)))

    def on_draw(self):

        arcade.start_render()

        if self.game_state == 1:
            self.archer = Archer()
            self.archer.center_x = SCREEN_WIDTH / 3
            self.archer.center_y = SCREEN_HEIGHT / 2
            self.mage = Mage()
            self.mage.center_x = SCREEN_WIDTH / 3 * 2
            self.mage.center_y = SCREEN_HEIGHT / 2
            self.archer.draw()
            self.mage.draw()
            arcade.draw_text('Choose your hero', SCREEN_WIDTH/2, 600, arcade.color.WHITE, 36, anchor_x='center')
            arcade.draw_text('archer', SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2 - 70,  arcade.color.WHITE, 18, anchor_x='center')
            arcade.draw_text('mage', SCREEN_WIDTH / 3 * 2, SCREEN_HEIGHT / 2 - 70, arcade.color.WHITE, 18, anchor_x='center')

        if self.game_state == 2:
            # draw everything
            self.player_list.draw()
            self.player_bullet_list.draw()
            self.wall_list.draw()
            self.enemy_list.draw()
            self.enemy_hp_list.draw()
            self.player_hp_bar_sprite.draw()

            # draw the text of the score
            for enemy in self.enemy_list:
                enemy.bullet_list.draw()
            output = f"Score: {self.score}"
            arcade.draw_text(output, 10 + self.view_left, 10 + self.view_bottom, arcade.color.WHITE, 18)

            # draw the end game screen if the player died
            if self.player_hp <= 0:
                arcade.draw_rectangle_filled(SCREEN_WIDTH/2 + self.view_left, SCREEN_HEIGHT/2 + self.view_bottom, 300, 100, arcade.color.BLACK)
                output = f"YOU DIED"
                arcade.draw_text(output, SCREEN_WIDTH/2 + self.view_left, SCREEN_HEIGHT/2 + 5 + self.view_bottom, arcade.color.WHITE, 32, 0, align='center', anchor_x='center', anchor_y='bottom')
                output = f'Score: {self.score}'
                arcade.draw_text(output, SCREEN_WIDTH / 2 + self.view_left, SCREEN_HEIGHT / 2 + self.view_bottom, arcade.color.WHITE, 18, 0, align='center', anchor_x='center', anchor_y='top')
                output = f'Click anywhere to restart'
                arcade.draw_text(output, SCREEN_WIDTH/2 + self.view_left, SCREEN_HEIGHT/2 - 35 + self.view_bottom, arcade.color.WHITE, 18, 0, align='center', anchor_x='center', anchor_y='bottom')

    def on_mouse_press(self, x, y, button, modifiers):

        if self.game_state == 1:
            if self.archer.left <= x <= self.archer.right and self.archer.bottom <= y <= self.archer.top:
                self.player_hero = 'archer'
                self.bullet_range = 8 * 100
                self.bullet_speed = 10
                self.damage = 10
                self.reload_speed = 0.3 * 60
                self.bullet_sprite = arcade.Sprite('image/arrow.png', 0.2)
                self.player_sprite = arcade.Sprite('image/rouge.png', 0.3)
                self.player_sprite.center_x = 500
                self.player_sprite.center_y = 400
                self.player_list.append(self.player_sprite)
                self.player_hp_bar_sprite = arcade.Sprite('image/red_hp_bar.png', 1)
                self.game_state = 2
            if self.mage.left <= x <= self.mage.right and self.mage.bottom <= y <= self.mage.top:
                self.player_hero = 'mage'
                self.bullet_range = 5 * 100
                self.bullet_speed = 5
                self.damage = 25
                self.reload_speed = 0.75 * 60
                self.bullet_sprite = arcade.Sprite('image/fireball.png', 0.35)
                self.player_sprite = arcade.Sprite('image/mage.png', 0.2)
                self.player_sprite.center_x = 500
                self.player_sprite.center_y = 400
                self.player_list.append(self.player_sprite)
                self.player_hp_bar_sprite = arcade.Sprite('image/red_hp_bar.png', 1)
                self.game_state = 2
        if self.game_state == 2:
            # enable shooting
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.shoot = True
                if self.player_hp <= 0:
                    self.player_hp_bar_sprite.kill()
                    self.setup()


    def on_mouse_release(self, x, y, button, modifiers):

        # disable shooting
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot = False

    def on_key_press(self, key, modifiers):

        # enable movement
        if key == arcade.key.W:
            self.move_up = True
        if key == arcade.key.A:
            self.move_left = True
        if key == arcade.key.S:
            self.move_down = True
        if key == arcade.key.D:
            self.move_right = True

        # prevent extra speed from pressing 2 keys at once
        if (self.move_up or self.move_down) and (self.move_left or self.move_right):
            self.player_speed = 1.5 * sqrt(2)/2 * 100 / 60
        else:
            self.player_speed = 1.5 * 100 / 60

    def on_key_release(self, key, modifiers):

        # disable movement
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

        # check if the player is still alive
        if self.player_hp > 0 and self.game_state == 2:

            # updated the player's sprite
            self.player_list.update()

            # check to see if the player is going to shoot
            if self.shoot and self.reload <= 0:

                # spawn the arrow and reset the reload speed
                if self.player_hero == 'archer':
                    arrow = arcade.Sprite('image/arrow.png', 0.2)
                else:
                    arrow = arcade.Sprite('image/fireball.png', 0.35)
                self.reload += self.reload_speed

                # set the angle of the arrow to that of the player
                arrow.angle = self.player_sprite.angle

                # spawn the arrow in front of the player
                arrow.origin_x = self.player_sprite.center_x + 10 * cos(radians(arrow.angle))
                arrow.origin_y = self.player_sprite.center_y + 10 * sin(radians(arrow.angle))

                # set the original coordinates of the arrow
                arrow.center_x = arrow.origin_x
                arrow.center_y = arrow.origin_y

                # append the arrow into the bullet list
                self.player_bullet_list.append(arrow)

            # decrease the reload by 1 every time the method is ran
            if self.reload > 0:
                self.reload -= 1

            # reset the rejuvenate cooldown if the player shot
            if self.shoot:
                self.rejuvenate_cooldown = 5 * 60

            # move the bullet based on the angle and the speed, and determined if it has reached its range
            for bullet in self.player_bullet_list:
                bullet.center_x += self.bullet_speed * cos(radians(bullet.angle)) * 100 / 60
                bullet.center_y += self.bullet_speed * sin(radians(bullet.angle)) * 100 / 60
                if (round(bullet.center_x - bullet.origin_x)) ** 2 + (round(bullet.center_y - bullet.origin_y)) ** 2 > self.bullet_range ** 2:
                    bullet.kill()

            # determine if the bullet has hit the wall
            for wall in self.wall_list:
                wall_hit_list = arcade.check_for_collision_with_list(wall, self.player_bullet_list)
                for bullet in wall_hit_list:
                    bullet.kill()

            # check with sprite list to see if the player has collide with a wall
            physics_engine = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
            changed = False

            # move the player into a new coordinate
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

            # over-ride the changeing variable if the player hits a wall
            if len(physics_engine) > 0:
                changed = False

                # reset the coordinates of the player if it collides with a wall
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

            # set the new view port boundary
            self.view_left = self.player_sprite.center_x - 500
            self.view_bottom = self.player_sprite.center_y - 400

            # set the new view port
            if changed:
                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left - 1,
                                    self.view_bottom,
                                    SCREEN_HEIGHT + self.view_bottom - 1)

            # set the new length of the health bar based on the hp of player, and reset its coordinate
            self.player_hp_bar_sprite.width = self.player_hp
            self.player_hp_bar_sprite.center_x = self.player_sprite.center_x
            self.player_hp_bar_sprite.center_y = self.player_sprite.top + 5

            # set the the in_combat local variable
            in_combat = False

            # loop through all enemy in the list and to execute certain action
            for enemy in self.enemy_list:

                # determine if the player is in range of the enemy
                if -400 <= self.player_sprite.center_x - enemy.center_x <= 400 and -300 <= self.player_sprite.center_y - enemy.center_y <= 300 and enemy.turning_restriction == 0:

                    # turn its angle and shot if the player is in range
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

                # move at another random angle after a certain time if the player is NOT in range
                elif enemy.angle_change_restriction <= 0:
                    enemy.angle_change_restriction = 10 * 60
                    angle = randint(0, 360)
                    enemy.angle = angle

                # move at another angle facing the front after hitting a wall
                enemy.angle_change_restriction -= 1
                if enemy.turning_restriction > 0:
                    enemy.turning_restriction -= 1
                if enemy.turning_restriction == 1:
                    enemy.angle += randint(-60, 60)

                # determine if the player is in range enough, so that the enemy will stop enaging and stand still
                if -300 <= self.player_sprite.center_x - enemy.center_x <= 300 and -200 <= self.player_sprite.center_y - enemy.center_y <= 200 and enemy.turning_restriction == 0:
                    enemy.speed = 0

                    # if the player is not moving, start moving in random motion
                    if not self.move_up and not self.move_down and not self.move_left and not self.move_right and enemy.lock_on_adjustment_cooldown <= 0:
                        enemy.lock_on_speed_x = randrange(-15, 15) / 10 * 100 / 60
                        enemy.lock_on_speed_y = randrange(-15, 15) / 10 * 100 / 60
                        enemy.lock_on_adjustment_cooldown = 3 * 60
                    enemy.center_x += enemy.lock_on_speed_x
                    enemy.center_y += enemy.lock_on_speed_y
                    enemy.lock_on_adjustment_cooldown -= 1

                # reset the speed if the player is not in range enough to stand still
                else:
                    enemy.speed = 1.5 * 100 / 60

                # set up the hit list
                physics_engine_enemy = arcade.check_for_collision_with_list(enemy, self.wall_list)

                # determine what to execute after hitting a wall
                if physics_engine_enemy != []:
                    if enemy.turning_restriction <= 0:

                        # stop moving if the enemy is chasing the player and hit a wall
                        if -400 <= self.player_sprite.center_x - enemy.center_x <= 400 and -300 <= self.player_sprite.center_y - enemy.center_y <= 300:
                            enemy.speed = 0

                        # move in the completely opposite direction immediately after hitting a wall
                        else:
                            enemy.speed = 1.5 * 100 / 60
                            enemy.turning_restriction = 0.5 * 60
                            enemy.angle = 180 + enemy.angle
                            if physics_engine != []:
                                if enemy.right - physics_engine[0].left < physics_engine[0].top - enemy.bottom and enemy.right - physics_engine[0].left < enemy.top - physics_engine[0].bottom:
                                    if physics_engine[0].left < enemy.right and physics_engine[0].center_x > enemy.center_x:
                                        enemy.right = physics_engine[0].left
                                        physics_engine = arcade.check_for_collision_with_list(enemy, self.wall_list)
                            if physics_engine != []:
                                if physics_engine[0].right - enemy.left < physics_engine[0].top - enemy.bottom and physics_engine[0].right - enemy.left < enemy.top - physics_engine[0].bottom:
                                    if physics_engine[0].right > enemy.left and physics_engine[0].center_x < enemy.center_x:
                                        enemy.left = physics_engine[0].right
                                        physics_engine = arcade.check_for_collision_with_list(enemy, self.wall_list)
                            if physics_engine != []:
                                if physics_engine[0].top > enemy.bottom and physics_engine[0].center_y < enemy.center_y:
                                    enemy.bottom = physics_engine[0].top
                                if physics_engine[0].bottom < enemy.top and physics_engine[0].center_y > enemy.center_y:
                                    enemy.top = physics_engine[0].bottom

                    # move in the opposite direction if the player is not moving and the enemy is moving in random motion
                    if -300 <= self.player_sprite.center_x - enemy.center_x <= 300 and -200 <= self.player_sprite.center_y - enemy.center_y <= 200:
                        enemy.lock_on_speed_x *= -1
                        enemy.lock_on_speed_y *= -1
                        enemy.lock_on_adjustment_cooldown = 5 * 60

                # move the enemy to a new coordinate
                enemy.center_x += enemy.speed * cos(radians(enemy.angle))
                enemy.center_y += enemy.speed * sin(radians(enemy.angle))

                # update the coordinate of the health bar of the enemy
                for i in range(len(self.enemy_hp_list)):
                    self.enemy_hp_list[i].center_x = self.enemy_list[i].center_x
                    self.enemy_hp_list[i].center_y = self.enemy_list[i].top + 5
                self.enemy_hp_list.update()

                # call the shooting mechanics of the enemy
                enemy.shooting_mechanics(self.wall_list)
                hit_list = arcade.check_for_collision_with_list(self.player_sprite, enemy.bullet_list)

                # deal damage to the player if hit, and reset the rejuvenate cooldown
                for bullet in hit_list:
                    self.player_hp -= enemy.damage
                    self.rejuvenate_cooldown = 5 * 60
                    bullet.kill()

                # set the player's status to be 'in-combat'
                if hit_list != []:
                    in_combat = True

                # reset the length of the player's health bar
                self.player_hp_bar_sprite.width = self.player_hp / self.player_hp_max * 100

            # reduce the rejuvenate cooldown if the player is not shooting and in- combat
            if not self.shoot and not in_combat:
                self.rejuvenate_cooldown -= 1

                # start rejuvenating hp if the cooldown is less than 0
                if self.rejuvenate_cooldown <= 0 and self.player_hp < self.player_hp_max:
                    self.player_hp += 0.5

                # cap-out the player's hp
                if self.player_hp > self.player_hp_max:
                    self.player_hp = self.player_hp_max

            # check the bullet shot by player, and see if it has hit any enemy
            for bullet in self.player_bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

                # reduce the enemy's hp if hit, and make coresponding changes to its health bar
                for enemy in hit_list:
                    bullet.kill()
                    enemy.hp -= self.damage
                    index = 0
                    for i in range(len(self.enemy_list)):
                        if self.enemy_list[i] == hit_list[0]:
                            index = i
                    self.enemy_hp_list[index].width = enemy.hp / enemy.max_hp * 100

                    # kill the enemy if its health drop below 0 and added points
                    if enemy.hp <= 0:
                        enemy.kill()
                        self.enemy_hp_list[index].kill()
                        self.score += 100

                        # spawn another enemy
                        if randint(0, 2) == 0:
                            bot = Archer()
                        else:
                            bot = Mage()
                        hit_list = arcade.check_for_collision_with_list(bot, self.wall_list)
                        while hit_list != [] or self.view_left <= bot.center_x <= self.view_left + SCREEN_WIDTH or self.view_bottom <= bot.center_y <= self.view_bottom + SCREEN_HEIGHT:
                            if randint(0, 2) == 0:
                                bot = Archer()
                            else:
                                bot = Mage()
                            hit_list = arcade.check_for_collision_with_list(bot, self.wall_list)
                        self.enemy_list.append(bot)
                        hp_bar_sprite = arcade.Sprite('image/hp_bar.png', 1)
                        self.enemy_hp_list.append(hp_bar_sprite)

# main function that calls the game
def main():
    window = MyGame()
    window.setup()
    arcade.run()

# calls the main function to start the game
main()