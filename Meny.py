#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame
import os
import unit_param
import levels

from pygame.locals import *

pygame.init()
default_font = pygame.font.get_default_font()
font = pygame.font.SysFont(default_font, 40, False)
font2 = pygame.font.SysFont(default_font, 20, False)
img_dir = os.path.join(u'bin', 'image') + os.sep


class Button(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, text, event, args=None):
        pygame.sprite.Sprite.__init__(self)
        self.org_pos = pos_x, pos_y
        self.x, self.y = pos_x, pos_y
        self.text = text
        self.event = event
        self.args = args
        if self.args == None:
            self.args = self.text

        self.image = pygame.image.load(img_dir + 'button.png'
                                                        ).convert_alpha()
        self.org_image = self.image
        self.rect = self.image.get_rect()
        self.img_w, self.img_h = self.image.get_size()
        self.rect.center = (self.x, self.y)
        self.but_text = font.render(self.text, True, (128, 107, 42))
        self.but_rect = self.but_text.get_rect()
        self.but_rect.center = (self.x, self.y)

    def update(self):
        self.event(self.args)
        self.anim = 0

    def on_click(self):
        self.update()
        self.image = pygame.image.load(img_dir + 'ch_button.png'
                                                ).convert_alpha()

    def render(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.but_text, self.but_rect)

    def not_choosen(self):
        self.image = self.org_image


class Meny(object):

    def __init__(self, screen, location='Main'):

        self.screen = screen
        self.w, self.h = self.screen.get_size()

        self.map_name = None
        self.player = None
        self.level = None

        self.image = pygame.image.load(img_dir + 'background2.png'
                                                ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.w / 2, self.h / 2

        maps_path = r'%s/maps' % os.getcwd()
        self.maps = os.listdir(maps_path)
        self.cord_matrix = []
        up = 240
        for x in xrange(3):
            for y in xrange(3):
                cord = [self.w / 2 - 370 + 210 * x, self.h / 2 - up - 70 * (1 - y)]
                self.cord_matrix.append(cord)

        play_buttons = []
        for i, map_name in enumerate(self.maps):
            but = Button(self.cord_matrix[i][0], self.cord_matrix[i][1],
                                    map_name, self.set_name)
            play_buttons.append(but)

        for i, player_name in enumerate(unit_param.player):
            but = Button(self.cord_matrix[i][0], self.cord_matrix[i][1] + 2 * up,
                        player_name['name'], self.set_player, unit_param.player[i])
            play_buttons.append(but)

        for i, level in enumerate(('Easy', 'Medium', 'Hard', 'Wave')):
            but = Button(self.cord_matrix[i][0], self.cord_matrix[i][1] + up,
                        level, self.set_level)
            play_buttons.append(but)

        x_plus = 300
        y_plus = 80

        self.play = Button(x_plus + self.w / 2, y_plus * -1 + self.h / 2,
                            'Play', self.ch_location)
        self.help = Button(x_plus + self.w / 2, y_plus * 0 + self.h / 2,
                            'Help', self.ch_location)
        self.exit = Button(x_plus + self.w / 2, y_plus * 1 + self.h / 2,
                            'Exit', self.ch_location)
        self.back = Button(x_plus + self.w / 2, y_plus * 1 + self.h / 2,
                            'Main', self.ch_location)
        self.go = Button(x_plus + self.w / 2, y_plus * 0 + self.h / 2,
                            'Go', self.start)
        play_buttons.extend((self.back, self.go))

        self.dirs = {'Main': (self.play, self.help, self.exit),
                     'Play': play_buttons,
                     'Help': (self.back, )}
        self.location = location  # can be Main, Play, HHelp, retry

        self.player_param = ('max_speed', 'maneuver_ability', 'health',
                            'main_weapon', 'sec_weapon')

        self.forms = {}
        for i in range(3):
            form_img = pygame.image.load(img_dir + 'form.png').convert_alpha()
            form_rect = form_img.get_rect()
            form_rect.center = [self.w / 2, self.h / 2 - up * (1 - i)]
            self.forms[form_img] = form_rect

    def draw(self, mouse_pos):

        if self.location == 'Exit':
            return False
        elif self.location == 'Go':
            self.location = 'Main'
            return 'Go'

        self.screen.blit(self.image, self.rect)
        if self.location == 'Play':
            self.load_form()
            self.load_player_img()
            self.load_minimap()
        elif self.location == 'Help':
            self.load_help()

        for button in self.dirs[self.location]:
            button.render(self.screen)

            if button.rect.collidepoint(mouse_pos):
                button.on_click()
            else:
                button.not_choosen()

        return True

    def ch_location(self, loc):
        self.location = loc

    def start(self, loc):
        if (self.map_name and self.player and self.level) != None:
            self.location = loc

    def set_name(self, name):
        self.map_name = name

    def set_player(self, name):
        self.player = name

    def set_level(self, name):
        if self.map_name != None:
            if name != 'Wave':
                self.level = eval('levels.%s.%s' % (self.map_name, name))
            else:
                self.level = name

    def load_player_img(self):
        if self.player == None:
            player_img = pygame.image.load(img_dir + 'player.png'
                                                        ).convert_alpha()
        else:
            player_img = pygame.image.load(self.
                        player['bitmap_path']).convert_alpha()
            for i, param in enumerate(self.player_param):
                par_text = font2.render(param, True, (128, 107, 42))
                par_text2 = font2.render(str(self.player[param]), True,
                                                (128, 107, 42))
                if type(self.player[param]).__name__ == 'dict':
                    par_text2 = font2.render(str(self.player[param]['name']),
                                True, (128, 107, 42))
                par_rect = par_text.get_rect()
                par_rect2 = par_text2.get_rect()

                par_rect.topleft = 240 + self.w / 2, - 20 * i + 240 + self.h / 2
                par_rect2.topleft = 360 + self.w / 2, - 20 * i + 240 + self.h / 2

                self.screen.blit(par_text, par_rect)
                self.screen.blit(par_text2, par_rect2)

        player_rect = player_img.get_rect()
        player_rect.center = 320 + self.w / 2, self.h / 2 + 300

        self.screen.blit(player_img, player_rect)

    def load_minimap(self):
        if self.map_name == None:
            minimap = pygame.image.load(img_dir + 'map.png').convert_alpha()
        else:
            map_path = os.path.join(u'maps', self.map_name, 'minimap.png')
            minimap = pygame.image.load(map_path).convert_alpha()
        minimap_rect = minimap.get_rect()
        minimap_rect.center = 220 + self.w / 2, -250 + self.h / 2

        self.screen.blit(minimap, minimap_rect)

    def load_form(self):
        for form in self.forms:
            self.screen.blit(form, self.forms[form])

    def load_help(self):
        help_img = pygame.image.load(img_dir + 'help.png').convert_alpha()
        help_rect = help_img.get_rect()
        help_rect.center = self.w / 2, self.h / 2

        self.screen.blit(help_img, help_rect)
