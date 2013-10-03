#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
# all of effects must be in list all_effects
img_dir = os.path.join(u'bin', 'image', 'effects') + os.sep
explosion_1 = {
                "bitmap_path":  img_dir + 'explosion_1.png',
                "width":        128,
                "height":       128,
                "fps":          100,
                "name":         "explosion_1"
                }

explosion_2 = {
                "bitmap_path":  img_dir + 'explosion_2.png',
                "width":        128,
                "height":       128,
                "fps":          100,
                "name":         "explosion_2"
                }

explosion_3 = {
                "bitmap_path":  img_dir + 'explosion_3.png',
                "width":        128,
                "height":       128,
                "fps":          100,
                "name":         "explosion_3"
                }

explosion_4 = {
                "bitmap_path":  img_dir + 'explosion_4.png',
                "width":        128,
                "height":       128,
                "fps":          100,
                "name":         "explosion_4"
                }

explosion_5 = {
                "bitmap_path":  img_dir + 'explosion_5.png',
                "width":        128,
                "height":       128,
                "fps":          100,
                "name":         "explosion_5"
                }

explosion_6 = {
                "bitmap_path":  img_dir + 'explosion_6.png',
                "width":        128,
                "height":       128,
                "fps":          100,
                "name":         "explosion_6"
                }

smoke_1 = {
                "bitmap_path":  img_dir + 'smoke_1.png',
                "width":        128,
                "height":       128,
                "fps":          100,
                "name":         "smoke_1"
                }

smoke_1_s = {
                "bitmap_path":  img_dir + 'smoke_1_s.png',
                "width":        64,
                "height":       64,
                "fps":          100,
                "name":         "smoke_1_s"
                }
fire_1 = {
                "bitmap_path":  img_dir + 'fire_1.png',
                "width":        128,
                "height":       128,
                "fps":          100,
                "name":         "fire_1"
                }

bomb = {
                "bitmap_path":  img_dir + 'bomb.png',
                "width":        128,
                "height":       128,
                "fps":          100,
                "name":         "bomb"
                }

#list of all effects(dicts)
all_effects = [explosion_1, explosion_2, explosion_3,
               explosion_4, explosion_5, explosion_6,
               smoke_1, smoke_1_s, fire_1, bomb]
