#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame

from unit import Machine


class Airdefence(Machine):

    def __init__(self, parameters, x_pos, y_pos, factor, direction,
                speed=0.0, angle=0.0, member='airdefence', weapon_group=None):
        Machine.__init__(self, parameters, x_pos, y_pos, factor, direction,
                speed=speed, angle=angle, member=member, weapon_group=weapon_group)
        self.base_img = pygame.image.load(self.param['base']).convert_alpha()
        self.base_rect = self.base_img.get_rect()
        dx, self.dy = self.org_bitmap.get_size()
        self.mask = pygame.mask.from_surface(self.base_img)
        self.step = 0

    def update(self, shift=0.0):
        self.rect.normalize()
        self.norm_angle()
        self.x -= shift  # forvard, back
        self.y += self.g_force   # up, down
        self.base_rect.center = (self.x, self.y + self.dy / 2)

        Machine.update(self)

    def render(self, screen):
        """ drawing Unit on screen"""
        screen.blit(self.health_bitmap, self.health_rect)
        screen.blit(self.base_img, self.base_rect)
        screen.blit(self.bitmap, self.rect)

    def up(self):
        self.rotate(1)
