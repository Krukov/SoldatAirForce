#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame


class Effect(pygame.sprite.Sprite):
    """ Effect"""

    def __init__(self, frames, x_pos, y_pos, fps=100):

        pygame.sprite.Sprite.__init__(self)
        self._images = frames

        self._frame = 0
        self.image = self._images[self._frame]

        self.x, self.y = x_pos, y_pos
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.remove_flag = 0

    def update(self, shift=0):
        if self._frame < len(self._images) - 1:
            self._frame += 1
            self.x -= shift
            self.image = self._images[self._frame]
            self.rect.center = self.x, self.y
        else:
            self.remove_flag = 1

    def render(self, screen):
        """ drawing Unit on screen"""
        screen.blit(self.image, self.rect)
