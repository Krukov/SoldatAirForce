#!/usr/bin/python
#-*- coding: utf-8 -*-

from unit import Weapon
from math import sin, radians

import pygame


class Missle(Weapon):

    def __init__(self, parameters, x_pos, y_pos, factor, speed=1.0, angle=0.0,
                                                             member='missle'):
        Weapon.__init__(self, parameters, x_pos, y_pos, factor, speed=speed,
                                                 angle=angle, member=member)

        self.assel = self.param['assel']
        self.fuel = self.live
        self.wfire_bitmap = pygame.image.load(self.param['bitmap_path_wf']
                                                            ).convert_alpha()
        self.wfire_bitmap = pygame.transform.scale(self.wfire_bitmap,
                list((int(i * factor) for i in self.wfire_bitmap.get_size())))

        self.radius = self.param['detected_radius'] * self.factor
        self.smoke = self.param['effect2']

    def update(self, shift=0.0):

        if self.fuel > 0:
            self.speed += self.assel
            self.fuel -= 1
        elif self.fuel == 0:
            self.fuel -= 1
            self.org_bitmap = self.wfire_bitmap
            self.bitmap = self.wfire_bitmap
            self.bitmap = pygame.transform.rotate(self.org_bitmap, self.angle)
            self.rect = self.bitmap.get_rect()
            self.rect.center = self.x, self.y
            self.mask = pygame.mask.from_surface(self.bitmap)
        else:
            self.g_force += 0.05
            self.speed -= self.assel / 10

        Weapon.update(self, shift=shift)

        if self.speed <= 0:
            self.remove_flag = 1

    def down(self):
        self.rotate(-1)

    def up(self):
        self.rotate(1)

    def destroy(self):
        pass


class Cannon(Weapon):
    """"""

    def __init__(self, parameters, x_pos, y_pos, factor, speed=0.0, angle=0.0,
                                                             member='cannon'):
        Weapon.__init__(self, parameters, x_pos, y_pos, factor, speed=speed,
                                                angle=angle, member=member)

    def update(self, shift=0.0):

        Weapon.update(self, shift=shift)
        self.live -= 1
        if self.live == 0:
            self.remove_flag = 1

    def destroy(self):
        del self


class Snag(Weapon):

    def __init__(self, parameters, x_pos, y_pos, factor, speed=0.0, angle=0.0,
                                                               member='snag'):
        Weapon.__init__(self, parameters, x_pos, y_pos, factor, speed=speed,
                                                angle=angle, member=member)
        self.health = self.live
        self.step = 0

    def update(self, shift=0.0):

        if self.speed > 0:
            self.speed -= 0.1
        else:
            self.speed = 0
        if -90 < self.angle <= 90:
            self.angle -= 0.5
        else:
            self.angle += 0.5

        Weapon.update(self, shift=shift)

        self.health -= 1
        self.rect.center = self.x, self.y
        self.pxarray = pygame.PixelArray(self.bitmap)
        pxa_len_x = len(self.pxarray)
        pxa_len_y = len(self.pxarray[0])
        for x in range(pxa_len_x):
            for y in range(pxa_len_y):
                G = self.bitmap.unmap_rgb(self.pxarray[x][y])[1] + 5
                if G > 255:
                    G = 0
                self.pxarray[x][y] = (255,
                                      G,
                                      0,
                                      self.bitmap.unmap_rgb(self.pxarray[x][y])[3])

        del self.pxarray

    def destroy(self):
        del self


class Bomb(Weapon):
    """"""
    def __init__(self, parameters, x_pos, y_pos, factor, speed=0.0, angle=0.0,
                                                             member='bomb'):
        Weapon.__init__(self, parameters, x_pos, y_pos, factor, speed=speed,
                                                 angle=angle, member=member)

    def update(self, shift=0.0):
        self.norm_angle()

        if 90 < self.angle < 269:
            self.rotate(1, 1)
        elif 269 < self.angle < 271:
            pass
        else:
            self.rotate(-1, 1)

        self.rect.normalize()

        sin_y = sin(radians(self.angle))

        speed_y = self.speed * sin_y

        self.x -= shift  # forvard, back
        self.y -= (speed_y - self.g_force)   # up, down
        self.rect.center = self.x, self.y

        self.live -= 1
        if self.live == 0:
            self.remove_flag = 1
