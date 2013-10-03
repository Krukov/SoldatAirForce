#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import os


class Map(pygame.sprite.Sprite):

    def __init__(self, name):

        pygame.sprite.Sprite.__init__(self)

        self.map_im = pygame.image.load(os.path.join('maps', name, 'map.png')
                                                    ).convert_alpha()
        self.map_mask = pygame.image.load(os.path.join('maps', name, 'mask.png')
                                                    ).convert_alpha()
        self.scale_factor = pygame.display.Info().current_h / float(
                                                    self.map_im.get_height())

        self.map_im = pygame.transform.scale(self.map_im, list((
                                                    int(i * self.scale_factor)
            for i in self.map_im.get_size())))
        self.map_mask = pygame.transform.scale(self.map_mask, list((
                                                    int(i * self.scale_factor)
            for i in self.map_mask.get_size())))

        self.rect = self.map_im.get_rect()
        self.x, self.y = self.rect.center
        self.mask = pygame.mask.from_surface(self.map_mask)

    def update(self, shift=0.0):
        self.x -= shift
        self.rect.center = self.x, self.y

    def render(self, window):
        window.blit(self.map_im, self.rect)

    def get_scale_factor(self):
        return self.scale_factor
