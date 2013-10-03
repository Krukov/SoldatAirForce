#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import math
import os

from pygame.color import *
from pygame.locals import *
from random import randint


class Control(object):
    """docstring for Control"""
    def __init__(self):
        self.pressed = {self.down: False,
                        self.up: False,
                        self.left: False,
                        self.right: False,
                        self.shoot: False,
                        self.sec_shoot: False,
                        self.snag_shoot: False}

    def control(self, event):

        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.pressed[self.down] = True
            elif event.key == K_UP:
                self.pressed[self.up] = True
            if event.key == K_a:
                self.pressed[self.left] = True
            elif event.key == K_z:
                self.pressed[self.right] = True
            if event.key == K_SPACE:
                self.pressed[self.shoot] = True
            if event.key == K_LSHIFT:
                self.pressed[self.sec_shoot] = True
            if event.key == K_LCTRL:
                self.pressed[self.snag_shoot] = True
            if event.key == K_1:
                self.step = 1
            if event.key == K_2:
                self.step = 2
            if event.key == K_3:
                self.step = 3
            if event.key == K_4:
                self.step = 4
            if event.key == K_5:
                self.step = 5
            if event.key == K_6:
                self.step = 6
            if event.key == K_7:
                self.step = 7
            if event.key == K_8:
                self.step = 8
            if event.key == K_9:
                self.step = 9
            if event.key == K_0:
                self.step = 10

        elif event.type == KEYUP:
            if event.key == K_DOWN:
                self.pressed[self.down] = False
            elif event.key == K_UP:
                self.pressed[self.up] = False
            if event.key == K_a:
                self.pressed[self.left] = False
            elif event.key == K_z:
                self.pressed[self.right] = False
            if event.key == K_SPACE:
                self.pressed[self.shoot] = False
            if event.key == K_LSHIFT:
                self.pressed[self.sec_shoot] = False
            if event.key == K_LCTRL:
                self.pressed[self.snag_shoot] = False

    def do_action(self):
        for action in self.pressed.keys():
            if self.pressed[action]:
                action()

    def down(self):
        pass

    def up(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

    def shoot(self):
        pass

    def sec_shoot(self):
        pass

    def snag_shoot(self):
        pass


class Unit(pygame.sprite.Sprite, Control):
    """ Super class for majority of object of game
    parameters - take in unit_param
    x_pos - x position
    y_pos - y position
    factor - koefisient of scale size
    direction - direction of unit image - ('right' - default image direction
                                     'left' - left direction)
    speed - speed unit
    angle - angle of unit
    member = like name"""

    def __init__(self, parameters, x_pos, y_pos, factor, speed=0.0, angle=0.0, member=''):

        pygame.sprite.Sprite.__init__(self)
        Control.__init__(self)

        self.param = parameters
        self.x, self.y = x_pos, y_pos
        self.factor = factor
        self.x_speed, self.y_speed, self.speed = 0, 0, speed
        if self.speed == None:
            try:
                self.speed = self.param['max_speed'] * self.factor
            except:
                self.speed = 0
        self.angle = angle
        self.member = member

        bitmap_path = self.param['bitmap_path']
        self.org_bitmap = pygame.image.load(bitmap_path).convert_alpha()

        self.org_bitmap = pygame.transform.scale(self.org_bitmap,
                    list((int(i * factor) for i in self.org_bitmap.get_size())))
        self.bitmap = self.org_bitmap
        self.rect = self.org_bitmap.get_rect()
        self.rect.center = (self.x, self.y)

        self.rotate(1, rotate_angle=0)
        self.mask = pygame.mask.from_surface(self.bitmap)
        try:
            self.mass = self.param['mass']
        except:
            self.mass = 0
        self.G = 2 * self.factor
        self.g_force = self.mass * self.G
        self.effect = self.param['effect']

    def update(self):
        pass

    def render(self, screen):
        """ drawing Unit on screen"""
        screen.blit(self.bitmap, self.rect)

    def rotate(self, rotate_direction, rotate_angle=None):
        """ Rotate Unit on rotate_angle"""
        if rotate_angle == None:
            try:
                rotate_angle = self.param['maneuver_ability']
            except:
                rotate_angle = 1

        self.angle += rotate_angle * rotate_direction
        self.bitmap = pygame.transform.rotate(self.org_bitmap, self.angle)
        self.rect = self.bitmap.get_rect()
        self.rect.center = self.x, self.y
        self.mask = pygame.mask.from_surface(self.bitmap)

    def scale(self, factor):
        self.bitmap = pygame.transform.scale(self.org_bitmap,
                    list((i / factor for i in self.org_bitmap.get_size())))
        self.rect = self.bitmap.get_rect()
        self.rect.center = self.x, self.y
        self.mask = pygame.mask.from_surface(self.bitmap)

    def norm_angle(self):
        ch_negativ = lambda x: x + 360 if x < 0 else x
        ch360 = lambda x: x - 360 if x > 360 else x
        self.angle = ch_negativ(self.angle)
        self.angle = ch360(self.angle)


class Machine(Unit):

    """docstring for Machine"""
    def __init__(self, parameters, x_pos, y_pos, factor, direction,
                speed=0.0, angle=0.0, member='machine', weapon_group=None):
        Unit.__init__(self, parameters, x_pos, y_pos, factor, speed=speed, angle=angle, member=member)
        self.direction = direction
        self.x, self.y = x_pos * self.factor, y_pos * self.factor

        self.bitmap = self.org_bitmap
        if self.member == 'enemy':
            self.color()

        if weapon_group != None:
            self.weapon_group = weapon_group

        self.health = self.param['health']
        self.health_bitmap = pygame.image.load(os.path.join(u'bin', 'image',
                                         'health.png')).convert_alpha()

        self.health_bitmap = pygame.transform.scale(self.health_bitmap,
                    list((int(i * factor) for i in self.org_bitmap.get_size())))
        self.health_bitmap_h = self.org_bitmap.get_height()
        self.health_bitmap_w = self.org_bitmap.get_width()
        self.health_k = float(self.health_bitmap_h) / self.health
        self.health_rect = self.health_bitmap.get_rect()
        self.health_topside = self.org_bitmap.get_height() + 2
        self.health_rect.center = self.x, self.y - self.health_topside

        self.main_weapon = self.param['main_weapon']
        self.main_reload_time = self.main_weapon['time_to_reload']
        self.sec_weapon = self.param['sec_weapon']
        self.sec_reload_time = self.sec_weapon['time_to_reload']
        self.snag = self.param['snag']
        self.snag_reload_time = self.snag['time_to_reload']
        self.not_reload = 0
        self.sec_not_reload = 0
        self.snag_not_reload = 0
        self.radius = self.param['detected_radius'] * self.factor

        if self.direction == 'left':
            self.flip()

    def update(self):
        self.not_reload -= 1
        self.sec_not_reload -= 1
        self.snag_not_reload -= 1
        self.rect.center = self.x, self.y
        self.health_rect.center = self.x, self.y - self.health_topside
        px_health = pygame.PixelArray(self.health_bitmap)
        px_health[1: self.health_bitmap_h - int(self.health_k * self.health), 1: self.health_bitmap_w] = 255, 0, 0, 143
        del px_health

    def player_update(self):  # call if map must move
        self.player_pos = float(self.x)
        self.update()
        self.shift = float(self.x)
        self.x = self.player_pos

        return self.shift - self.player_pos

    def color(self):
        '''Change (mix) colors in image (to select enemy or friend unit'''
        pxarray = pygame.PixelArray(self.org_bitmap)
        pxa_len_x = len(pxarray)
        pxa_len_y = len(pxarray[0])
        for x in range(pxa_len_x):
            for y in range(pxa_len_y):
                pxarray[x][y] = (self.bitmap.unmap_rgb(pxarray[x][y])[0],
                                 self.bitmap.unmap_rgb(pxarray[x][y])[0],
                                 self.bitmap.unmap_rgb(pxarray[x][y])[0],
                                 self.bitmap.unmap_rgb(pxarray[x][y])[3])
        del pxarray

    def flip(self):
        self.bitmap = pygame.transform.flip(self.org_bitmap, False, True)
        self.org_bitmap = self.bitmap
        self.rect = self.bitmap.get_rect()
        self.rect.center = self.x, self.y
        self.mask = pygame.mask.from_surface(self.bitmap)
        if 90 < self.angle < 270:
            self.angle = 0
            self.direction = 'right'
        else:
            self.angle = 180
            self.direction = 'left'
        self.rotate(1, rotate_angle=0)

    def down(self):
        self.rotate(-1)

    def right(self):
        self.step += 1

    def left(self):
        self.step -= 1

    def shoot(self):  # cannon
        if self.not_reload < 0:
            weapon = self.main_weapon["type"](self.main_weapon, self.x,
                 self.y, self.factor, speed=self.speed, angle=self.angle)
            weapon.speed = self.main_weapon["speed"] * self.factor
            weapon.add(self.weapon_group)
            self.not_reload = self.main_reload_time

    def sec_shoot(self):  # missle
        if self.sec_not_reload < 0:
            weapon = self.sec_weapon["type"](self.sec_weapon, self.x,
                 self.y, self.factor, speed=self.speed, angle=self.angle)
            weapon.add(self.weapon_group)
            self.sec_not_reload = self.sec_reload_time

    def snag_shoot(self):  # snag
        if self.snag_not_reload < 0:
            snag = self.snag["type"](self.snag, self.x, self.y,
                     self.factor, speed=randint(3, 9), angle=90)
            snag.add(self.weapon_group)

            self.snag_not_reload = self.snag_reload_time


class Weapon(Unit):
    """docstring for Weapon"""

    def __init__(self, parameters, x_pos, y_pos, factor, speed=1.0, angle=0.0, member='weapon'):
        Unit.__init__(self, parameters, x_pos, y_pos, factor, speed=speed, angle=angle, member=member)
        self.live = self.param['time_to_live']
        self.remove_flag = 0
        self.damage = self.param['damage']

    def update(self, shift=0.0):
        self.is_update = 1
        self.rect.normalize()

        sin, cos = math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle))
        speed_x = self.speed * cos
        speed_y = self.speed * sin

        self.x += speed_x - shift  # forvard, back
        self.y -= (speed_y - self.g_force)   # up, down
        self.rect.center = self.x, self.y

    def down(self):
        self.rotate(-1)

    def up(self):
        self.rotate(1)

    def flip(self):
        pass
