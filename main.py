#!/usr/bin/python
#-*- coding: utf-8 -*-


__author__ = "Dmitry Krukow"
__email__ = "Glebov.ru@gmail.com"
__date__ = "$26.07.2012 17:09:16$"

import pygame
import time
import sys
import math
import random

from pygame.color import *
from pygame.locals import *

import Meny
import effect_param
import unit_param
from bin import *


def is_ok(func):
    def call_f(*arg, **kwards):
        t1 = time.time()
        f = func(*arg, **kwards)
        t2 = time.time()

        print '%s is done.  time - %s ' % (func.__name__, t2 - t1)
        return f
    return call_f


def load_effects(array, factor):
    all_images = {}
    for effect in array:

        images = []
        master_image = pygame.image.load(effect["bitmap_path"]).convert_alpha()

        master_width, master_height = master_image.get_size()
        w, h = effect["width"], effect["height"]
        for j in xrange(int(master_height / h)):
            for i in xrange(int(master_width / w)):
                frame = master_image.subsurface((i * w, j * h, w, h))
                frame = pygame.transform.scale(frame,
                    list((int(i / (factor + 1)) for i in frame.get_size())))

                images.append(frame)
        all_images[effect["name"]] = images
    return all_images


class Storige(object):
    """Storige to vars"""
    map_name = None
    player = None


class GeneralWindow(object):
    """docstring for GeneralWindow"""

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(1, 1)
        w = pygame.display.Info().current_w
        h = pygame.display.Info().current_h
        self.size = (w, h)
        pygame.display.set_mode(self.size, FULLSCREEN, 32)
        pygame.display.set_caption("SoldatAirForce")
        self.location = 0


class MenyWindow(object):

    def __init__(self):
        self.window = pygame.display.get_surface()

        self.meny = Meny.Meny(self.window)

        self.all_effects_img = load_effects(effect_param.all_effects, -0.1)
        self.effects_group = pygame.sprite.Group()
        self.mouse_pos = 0, 0

    def draw(self):
        """rendering window"""
        self.window.fill((0, 0, 0))
        res = self.meny.draw(self.mouse_pos)
        for obj in self.effects_group:
            obj.update()
            obj.render(self.window)
        pygame.display.flip()
        self.mouse_pos = 0, 0

        Storige.map_name = self.meny.map_name
        Storige.player = self.meny.player
        Storige.level = self.meny.level

        return res

    def control(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.effects_group.add(Effect(self.all_effects_img["explosion_4"],
                                    event.pos[0],  event.pos[1]))
            self.mouse_pos = event.pos


class GameWindow(object):

    def __init__(self):
        '''Manager - loading'''

        self.window = pygame.display.get_surface()
        default_font = pygame.font.match_font("symap")
        self.create_group()
        self.load_map()
        if Storige.level != 'Wave':
            self.load_level()
        else:
            self.start_wave()
        self.all_effects_img = load_effects(effect_param.all_effects,
                                                            self.factor)

        w, h = self.window.get_size()
        self.font = pygame.font.SysFont(default_font, int(500 * self.factor),
                                                                    False)
        self.font_step = pygame.font.SysFont(default_font, int(60 * self.factor),
                                                                    False)
        self.game_over_text = self.font.render("Game over", True,
                                                 (255, 50, 42, 120))
        self.win_text = self.font.render("You WIN", True, (255, 107, 42))
        self.text_rect = self.game_over_text.get_rect()
        self.text_rect.center = (w / 2, h / 2)
        self.stop_timer = 400

    @is_ok
    def create_group(self):
        self.all_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.friend_group = pygame.sprite.Group()
        self.enemy_weapon_group = pygame.sprite.Group()
        self.friend_weapon_group = pygame.sprite.Group()
        self.effects_group = pygame.sprite.Group()

    @is_ok
    def load_map(self):
        self.game_map = Map(Storige.map_name)
        self.factor = self.game_map.get_scale_factor()

    @is_ok
    def load_level(self):
        # create units and add to group
        level = Storige.level
        self.wave = False
        self.Player = Storige.player['type'](Storige.player, level['player'][0],
                    level['player'][1], self.factor, level['player'][2], speed=level['player'][3],
                    member='player', weapon_group=self.friend_weapon_group)
        self.Player.add(self.friend_group)

        for enemy in level['enemy']:
            enemy_obj = enemy[0]['type'](enemy[0], enemy[1], enemy[2], self.factor,
            enemy[3], speed=enemy[4], member='enemy', weapon_group=self.enemy_weapon_group)
            enemy_obj.add(self.all_group, self.enemy_group)

        for friend in level['friends']:
            friend_obj = friend[0]['type'](friend[0], friend[1], friend[2], self.factor,
            friend[3], speed=enemy[4], member='friend', weapon_group=self.friend_weapon_group)

            friend_obj.add(self.all_group, self.friend_group)

    def start_wave(self):
        self.Player = Storige.player['type'](Storige.player, 200, 200, self.factor, 'right',
                speed=None, member='player', weapon_group=self.friend_weapon_group)
        self.Player.add(self.friend_group)
        self.wave = 1

    def draw(self):
        '''Manager - rendering'''
        self.window.fill((255, 255, 255))
        self.Player.do_action()

        self.shift_y = 0

        self.map_move_manager()  # include units update calling

        self.game_map.render(self.window)
        self.Player.render(self.window)

        self.render_remove_manager()  # check unit-map position and check unit health, render units
        pygame.display.flip()
        self.collide_detected()
        if self.stop_timer < 0:
            self.Player.__class__.__name__ = 'Airplane'
            return "Meny"

        return True

    def map_move_manager(self):
        win_width = self.window.get_width()

        if (((self.Player.angle < 90 or self.Player.angle > 270) and self.Player.x >= win_width / 3) or
            (90 < self.Player.angle < 270 and self.Player.x <= 2 * win_width / 3)):
            if (self.game_map.rect.left <= -10 and 90 < self.Player.angle <= 270) or (
                self.game_map.rect.right >= (win_width + 10) and (270 <= self.Player.angle <= 360 or
                0 <= self.Player.angle <= 90)):

                self.shift_y = self.Player.player_update()
            else:
                self.Player.update()
        else:
            self.Player.update()

        if self.game_map.rect.right + 50 < self.Player.x or -50 > self.Player.x:
            self.Player.flip()

        self.game_map.update(shift=self.shift_y)

        # update block
        for obj in self.all_group:
            obj.update(shift=self.shift_y)
            obj.step += 1

        for obj in self.enemy_weapon_group:
            obj.update(shift=self.shift_y)
            if obj.member == 'snag':
                obj.remove(self.enemy_weapon_group)
                obj.add(self.enemy_group, self.all_group)

        for obj in self.friend_weapon_group:
            obj.update(shift=self.shift_y)
            if obj.member == 'snag':
                obj.remove(self.friend_weapon_group)
                obj.add(self.friend_group, self.all_group)

        for obj in self.effects_group:
            obj.update(shift=self.shift_y)

    def collide_detected(self):
        # check map collided
        map_all_collide = pygame.sprite.spritecollide(self.game_map, self.all_group,
                                    False, collided=pygame.sprite.collide_mask)

        map_fwep_collide = pygame.sprite.spritecollide(self.game_map, self.friend_weapon_group,
                                    True, collided=pygame.sprite.collide_mask)

        map_ewep_collide = pygame.sprite.spritecollide(self.game_map, self.enemy_weapon_group,
                                    True, collided=pygame.sprite.collide_mask)

        player_map_collide = pygame.sprite.collide_mask(self.game_map, self.Player)

        for obj in map_all_collide:
            if obj.__class__.__name__ == 'Airdefence':
                obj.g_force = 0
            else:
                obj.remove(self.all_group, self.friend_group, self.enemy_group)
                self.effect_add(obj)
                del obj

        for obj in map_fwep_collide:
            if obj.member == 'bomb':
                imag = self.all_effects_img[obj.effect]
                self.effects_group.add(Effect(imag, obj.x,
                                    obj.y - imag[0].get_width() / 2))
            else:
                self.effect_add(obj)
            del obj

        for obj in map_ewep_collide:
            if obj.member == 'bomb':
                imag = self.all_effects_img[obj.effect]
                self.effects_group.add(Effect(imag, obj.x,
                                     obj.y - imag[0].get_width() / 2))
            else:
                self.effect_add(obj)
            del obj

        if player_map_collide:
            self.Player.health = -100
            self.effect_add(self.Player, 10)
        # end map collide

        # check units collide
        # enemy => friend unit
        self.al_collide_manager(self.enemy_group, self.friend_group,
                                                self.friend_weapon_group)
        # friend => enemy unit
        self.al_collide_manager(self.friend_group, self.enemy_group,
                                                self.enemy_weapon_group)

        #friend weapon <=> enemy weapon
        for obj in self.friend_weapon_group:

            f_e_weapon_collide = pygame.sprite.spritecollide(obj,
                self.enemy_weapon_group, True, collided=pygame.sprite.collide_rect)

            if f_e_weapon_collide:
                for i in f_e_weapon_collide:
                    del i
                    try:
                        obj.remove(self.friend_weapon_group)
                        self.effect_add(obj)
                        del obj
                    except:
                        pass

    def al_collide_manager(self, group, target_group, target_weapon_group):
        for obj in group:

            group_weapon_collide_cycle = pygame.sprite.spritecollide(obj, target_weapon_group,
                            False, collided=pygame.sprite.collide_circle)

            group_weapon_collide = pygame.sprite.spritecollide(obj, target_weapon_group,
                            True, collided=pygame.sprite.collide_mask)

            if group_weapon_collide:
                for wep in group_weapon_collide:
                    obj.health -= wep.damage
                    self.effect_add(wep)

            if obj.member != 'snag':
                group_collide = pygame.sprite.spritecollide(obj, target_group,
                                False, collided=pygame.sprite.collide_mask)

                group_collide_cycle = pygame.sprite.spritecollide(obj, target_group,
                                False, collided=pygame.sprite.collide_circle)
                ## unit al
                if group_collide_cycle:
                    target = None
                    for i in group_collide_cycle:
                        if i.__class__.__name__ in ('Airplane', 'Airdefence') \
                                                and obj.member != 'player':
                            target = i
                            break

                    if target != None:
                        distance = math.sqrt((obj.x - target.x) ** 2
                                                + (obj.y - target.y) ** 2)
                        obj.sec_shoot()
                        if distance < obj.radius / 2 and \
                                    obj.__class__.__name__ != 'Airdefence':
                            if obj.direction == 'left':
                                obj.down()
                            else:
                                obj.up()
                        else:
                            alfa = math.atan2(obj.x - target.x,
                                        obj.y - target.y)
                            ch_negativ = lambda x: x + 360 if x < 0 else x
                            ch360 = lambda x: x - 360 if x > 360 else x
                            alfa = ch360(ch_negativ(math.degrees(alfa)) + 90)
                            alfa_res = alfa - obj.angle
                            if 0 < alfa_res < 15 or 345 < alfa_res < 360:
                                obj.shoot()
                            if abs(alfa_res) > 180:

                                if alfa_res < 0:
                                    obj.up()

                                elif alfa_res > 0:
                                    obj.down()
                            else:
                                if alfa_res < 0:
                                    obj.down()

                                elif alfa_res > 0:
                                    obj.up()

                    elif obj.__class__.__name__ == 'Airplane' and obj.member != 'player':

                        if obj.direction == 'left':
                            if obj.angle > 180:
                                obj.up()
                            elif obj.angle < 180:
                                obj.down()
                            if obj.y < 0:
                                obj.down()
                        else:
                            if obj.angle > 0:
                                obj.down()
                            elif obj.angle < 0:
                                obj.up()
                            if obj.y < 0:
                                obj.up()

                else:
                    if obj.__class__.__name__ == 'Airplane' and obj.member != 'player':

                        if obj.direction == 'left':
                            if obj.angle > 180:
                                obj.up()
                            elif obj.angle < 180:
                                obj.down()
                        else:
                            if obj.angle > 0:
                                obj.down()
                            elif obj.angle < 0:
                                obj.up()

                        if obj.y < 0 and (240 > obj.angle > -60):
                            obj.down()

            ## missle al
            if group_weapon_collide_cycle:
                for i in group_weapon_collide_cycle:

                    if i.member == 'missle' and i.fuel > 1:
                        missle = i
                        alfa = math.atan2(missle.y - obj.y, obj.x - missle.x)
                        ch_negativ = lambda x: x + 360 if x < 0 else x
                        ch360 = lambda x: x - 360 if x > 360 else x
                        ch360_ = lambda x: x + 360 if x < -360 else x
                        alfa_res = ch360_(ch360(missle.angle)) - math.degrees(alfa)
                        if abs(alfa_res) > 180:
                            if alfa_res < 0 or alfa_res > 360:
                                missle.down()
                            elif alfa_res > 0:
                                missle.up()
                        else:
                            if alfa_res < 0:
                                missle.up()
                            elif alfa_res > 0:
                                missle.down()

                        if obj.member != 'player':
                            obj.snag_shoot()

    def render_remove_manager(self):
        for obj in self.all_group:
            if ((self.game_map.rect.right + 50 < obj.x or -50 > obj.x) and
                                not self.game_map.rect.contains(obj.rect)):
                obj.flip()
            obj.render(self.window)
            if obj.health < 0:
                self.effects_group.add(Effect(self.all_effects_img['smoke_1'],
                                     obj.x,  obj.y - 42 * self.factor))
                if obj.member == 'snag' or obj.health < -2000:
                    obj.remove(self.all_group, self.enemy_group, self.friend_group)
                    self.effect_add(obj)
                    del obj
                else:
                    obj.member = 'player'
                    obj.step = 3
                    obj.health -= 10

        for obj in self.enemy_weapon_group:
            obj.render(self.window)
            if obj.member == 'missle' and obj.fuel > 0:
                self.effects_group.add(Effect(self.all_effects_img[obj.smoke], obj.x, obj.y - 24 * self.factor))
            if not self.game_map.rect.contains(obj.rect) or obj.remove_flag:
                obj.remove(self.enemy_weapon_group)
                try:
                    del obj
                except:
                    pass

        for obj in self.friend_weapon_group:
            obj.render(self.window)
            if obj.member == 'missle' and obj.fuel > 0:
                self.effects_group.add(Effect(self.all_effects_img[obj.smoke], obj.x, obj.y - 24 * self.factor))
            if not self.game_map.rect.contains(obj.rect) or obj.remove_flag:
                obj.remove(self.friend_weapon_group)
                try:
                    del obj
                except:
                    pass

        for obj in self.effects_group:
            obj.render(self.window)
            if obj.remove_flag:
                obj.remove(self.effects_group)
                try:
                    del obj
                except:
                    pass

        if self.Player.health < 0:
            self.window.blit(self.game_over_text, self.text_rect)
            self.stop_timer -= 1
            self.effects_group.add(Effect(self.all_effects_img['smoke_1'],
                     self.Player.x,  self.Player.y - 20))
            self.Player.step = 3
            self.Player.health -= 10
            self.Player.__class__.__name__ = 'Not_alive'

        if not self.enemy_group:
            if self.wave:
                self.wave += 1
                if self.wave > len(unit_param.player) - 1:
                    self.wave = 1
                enemy = unit_param.player[self.wave]
                enemy['type'](enemy, 5000, 200, self.factor, 'left', speed=None,
                     member='enemy', weapon_group=self.enemy_weapon_group).add(self.all_group, self.enemy_group)

            else:
                self.window.blit(self.win_text, self.text_rect)
                self.stop_timer -= 1

        self.step_text = self.font_step.render(str(self.Player.step), True, (255, 107, 42))
        self.step_text_rect = self.step_text.get_rect()
        self.step_text_rect.center = 30, 30
        self.window.blit(self.step_text, self.step_text_rect)

    def control(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.enemy_group = []
        self.Player.control(event)

    def effect_add(self, obj, size=1):
        dx, dy = 0, 0
        rad = 60
        for i in xrange(size):
            self.effects_group.add(Effect(self.all_effects_img[obj.effect],
                                     obj.x + dx,  obj.y + dy))
            dx, dy = random.randint(-rad, rad), random.randint(-rad, rad)


def main():
    t1 = time.time()
    general = GeneralWindow()
    meny = MenyWindow()

    general.location = meny  # start location
    Location = general.location

    clock = pygame.time.Clock()
    running = True
    t2 = time.time()
    print 'init time = ', t2 - t1
    while running:
        t1 = time.time()
        for event in pygame.event.get():
            Location.control(event)

        running = Location.draw()
        if running == 'Go':
            running = ' '
            Location = GameWindow()
        if running == 'Meny':
            del Location
            running = ' '
            Location = meny
        clock.tick(60)
        t2 = time.time()
        # print clock.get_fps(), t2 - t1


if __name__ == '__main__':
    sys.exit(main())
    pygame.quit()
