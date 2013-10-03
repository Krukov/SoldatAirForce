#!/usr/bin/python
#-*- coding: utf-8 -*-

from unit import Machine

import math


class Airplane(Machine):
    """docstring for Airplane"""

    def __init__(self, parameters, x_pos, y_pos, factor, direction,
                speed=0.0, angle=0.0, member='airplane', weapon_group=None):
        Machine.__init__(self, parameters, x_pos, y_pos, factor, direction,
                speed=speed, angle=angle, member=member, weapon_group=weapon_group)
        self.max_speed = self.param['max_speed'] * self.factor

        self.count_step = 10  # number of gears
        self.step_func = lambda step: self.max_speed * step / self.count_step

        self.step = int(self.speed / (float(self.max_speed) / self.count_step))

        self.assel_func = lambda step: math.sqrt(step / 10000.0)
        self.sh_step = lambda y: y if self.count_step > y else self.count_step
        self.sh_step0 = lambda x: 0 if x <= 0 else x

        self.up_force_val = lambda speed:  speed * self.max_speed / self.g_force
        self.up_force = 0

    def update(self, shift=0.0):
        """This Method describe movement of airplane and
        other actions have in every iteration"""
        self.rect.normalize()
        self.norm_angle()

        # movements
        self.step = self.sh_step(self.step)
        self.step = self.sh_step0(self.step)

        speed_to_go = self.step_func(self.step)
        self.assel = self.assel_func(self.step)
        if speed_to_go < self.speed:
            self.speed -= (self.assel_func(10) - self.assel / 3)
        elif speed_to_go > self.speed:
            self.speed += self.assel

        rad_angle = math.radians(self.angle)

        sin, cos = math.sin(rad_angle), math.cos(rad_angle)
        speed_x = self.speed * cos
        speed_y = self.speed * sin

        self.up_force = self.up_force_val(self.speed)

        if self.up_force > self.g_force:
            self.up_force = self.g_force

        self.x += speed_x - shift  # forvard, back
        self.y -= (speed_y + self.up_force - self.g_force)   # up, down

        Machine.update(self)

        if self.up_force < 0.9 * self.g_force or self.step == 0:  # TODO: make rotate dependent by speed
            if self.direction == 'right':
                if self.angle < 90 or self.angle > 290:
                    self.rotate(-1, rotate_angle=0.5)
                elif 250 > self.angle > 90:
                    self.rotate(1, rotate_angle=0.5)
            elif self.direction == 'left':
                if 250 > self.angle > 90:
                    self.rotate(1, rotate_angle=0.5)
                elif self.angle < 90 or self.angle > 290:
                    self.rotate(-1, rotate_angle=0.5)

    def render(self, screen):
        """ drawing Unit on screen"""
        screen.blit(self.bitmap, self.rect)
        screen.blit(self.health_bitmap, self.health_rect)

    def up(self):
        if self.up_force > 0.9 * self.g_force or self.step == 0:
            self.rotate(1)
