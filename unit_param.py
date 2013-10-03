#!/usr/bin/python
#-*- coding: utf-8 -*-

# list 'player' contains airplanes that gamer can choose to play

from bin import *

img_dir = os.path.join(u'bin', 'image') + os.sep
fast_missle =   {"type":              Missle,  # *
                 "bitmap_path_wf":    img_dir + 'missle.png',  # *
                 "bitmap_path":       img_dir + 'missle_fire.png',
                 "name":              "fast_missle",
                 "mass":              0.2,
                 "speed":             0,
                 "assel":             0.1,
                 "maneuver_ability":  2,
                 "damage":            30,  # *
                 "time_to_live":      200,
                 "time_to_reload":    100,  # *
                 "detected_radius":   1000,
                 "detected_type":     Airplane,
                 "effect":            "explosion_3",
                 "effect2":           "smoke_1_s"
                 }

medium_missle = {"type":              Missle,  # *
                 "bitmap_path_wf":    img_dir + 'missle_2.png',  # *
                 "bitmap_path":       img_dir + 'missle_2_fire.png',
                 "name":              "medium_missle",
                 "mass":              0,
                 "speed":             0,
                 "assel":             0.05,
                 "maneuver_ability":  1,
                 "damage":            80,  # *
                 "time_to_live":      250,
                 "time_to_reload":    200,  # *
                 "detected_radius":   500,
                 "detected_type":     Airplane,
                 "effect":            "explosion_3",
                 "effect2":           "smoke_1_s"
                 }

power_missle =  {"type":              Missle,  # *
                 "bitmap_path_wf":    img_dir + 'missle_2.png',  # *
                 "bitmap_path":       img_dir + 'missle_2_fire.png',
                 "name":              "power_missle",
                 "mass":              0.05,
                 "speed":             0,
                 "assel":             0.01,
                 "maneuver_ability":  0.5,
                 "damage":            120,  # *
                 "time_to_live":      1000,
                 "time_to_reload":    1000,  # *
                 "detected_radius":   2000,
                 "detected_type":     Airplane,
                 "effect":            "explosion_3",
                 "effect2":           "smoke_1_s"
                 }

snag         = {"type":               Snag,  # *
                "bitmap_path":        img_dir + 'snag.png',
                "mass":               3,
                "maneuver_ability":   0,
                "damage":             0,  # *
                "time_to_reload":     50,  # *
                "time_to_live":       100,
                 "effect":             "fire_1"
                }

bomb         = {"type":               Bomb,  # *
                "bitmap_path":        img_dir + 'bomb.png',
                "name":               "Bomb",
                "mass":               0.5,
                "maneuver_ability":   0,
                "damage":             50,  # *
                "time_to_reload":     50,  # *
                "time_to_live":       3000,
                "effect":             "bomb"
                }

fast_cannon   = {"type":              Cannon,  # *
                "bitmap_path":        img_dir + 'cannon2.png',
                "name":               "fast_cannon",
                "mass":               0,
                "maneuver_ability":   0,
                "speed":              50,
                "damage":             1.5,  # *
                "time_to_reload":     10,  # *
                "time_to_live":       70,
                "effect":             "fire_1"
                }

medium_cannon= {"type":               Cannon,  # *
                "bitmap_path":        img_dir + 'cannon1.png',
                "name":               "medium_cannon",
                "mass":               0,
                "maneuver_ability":   0,
                "speed":              30,
                "damage":             10,  # *
                "time_to_reload":     25,  # *
                "time_to_live":       70,
                "effect":             "fire_1"
                }

power_cannon= {"type":                Cannon,  # *
                "bitmap_path":        img_dir + 'cannon3.png',
                "name":               "power_cannon",
                "mass":               1,
                "maneuver_ability":   0,
                "speed":              15,
                "damage":             40,  # *
                "time_to_reload":     60,  # *
                "time_to_live":       400,
                "effect":             "explosion_5"
                }

spitfire      = {"type":              Airplane,  # *
                 "name":              "Spitfire",  # * for meny show
                 "bitmap_path":       img_dir + 'spitfire.png',  # *
                 "max_speed":         10,  # *
                 "mass":              5,  # * must be less then max_speed
                 "maneuver_ability":  2,  # *
                 "health":            100,  # *
                 "main_weapon":       fast_cannon,  # *
                 "sec_weapon":        fast_missle,  # *
                 "snag":              snag,
                 "detected_radius":   1000,
                 "effect":            "explosion_3"
                 }

fw190         = {"type":              Airplane,  # *
                 "name":              "FW190",  # * for meny show
                 "bitmap_path":       img_dir + 'fw190.png',  # *
                 "max_speed":         7,  # *
                 "mass":              3,  # * must be less then max_speed
                 "maneuver_ability":  1.5,  # *
                 "health":            120,  # *
                 "main_weapon":       fast_cannon,  # *
                 "sec_weapon":        medium_missle,  # *
                 "snag":              snag,
                 "detected_radius":   800,
                 "effect":            "explosion_3"
                 }

la5           = {"type":              Airplane,  # *
                 "name":              "La-5",  # * for meny show
                 "bitmap_path":       img_dir + 'la5.png',  # *
                 "max_speed":         6,  # *
                 "mass":              3,  # * must be less then max_speed
                 "maneuver_ability":  1,  # *
                 "health":            100,  # *
                 "main_weapon":       fast_cannon,  # *
                 "sec_weapon":        medium_missle,  # *
                 "snag":              snag,
                 "detected_radius":   1000,
                 "effect":            "explosion_3"
                 }

mig3          = {"type":              Airplane,  # *
                 "name":              "MIG-3",  # * for meny show
                 "bitmap_path":       img_dir + 'mig3.png',  # *
                 "max_speed":         11,  # *
                 "mass":              5,  # * must be less then max_speed
                 "maneuver_ability":  3,  # *
                 "health":            90,  # *
                 "main_weapon":       fast_cannon,  # *
                 "sec_weapon":        fast_missle,  # *
                 "snag":              snag,
                 "detected_radius":   800,
                 "effect":            "explosion_3"
                 }

ta152         = {"type":              Airplane,  # *
                 "name":              "TA-152",  # * for meny show
                 "bitmap_path":       img_dir + 'ta152.png',  # *
                 "max_speed":         7,  # *
                 "mass":              3,  # * must be less then max_speed
                 "maneuver_ability":  2,  # *
                 "health":            100,  # *
                 "main_weapon":       medium_cannon,  # *
                 "sec_weapon":        medium_missle,  # *
                 "snag":              snag,
                 "detected_radius":   1200,
                 "effect":            "explosion_3"
                 }

he162         = {"type":              Airplane,  # *
                 "name":              "He162",  # * for meny show
                 "bitmap_path":       img_dir + 'he162.png',  # *
                 "max_speed":         7,  # *
                 "mass":              3,  # * must be less then max_speed
                 "maneuver_ability":  1.2,  # *
                 "health":            600,  # *
                 "main_weapon":       power_cannon,  # *
                 "sec_weapon":        power_missle,  # *
                 "snag":              snag,
                 "detected_radius":   500,
                 "effect":            "explosion_3"
                 }

p51d         =  {"type":              Airplane,  # *
                 "name":              "P51d",  # * for meny show
                 "bitmap_path":       img_dir + 'p51d.png',  # *
                 "max_speed":         8,  # *
                 "mass":              3.5,  # * must be less then max_speed
                 "maneuver_ability":  2,  # *
                 "health":            110,  # *
                 "main_weapon":       medium_cannon,  # *
                 "sec_weapon":        medium_missle,  # *
                 "snag":              snag,
                 "detected_radius":   1000,
                 "effect":            "explosion_3"
                 }

hawker       =  {"type":              Airplane,  # *
                 "name":              "Hawker",  # * for meny show
                 "bitmap_path":       img_dir + 'hawker.png',  # *
                 "max_speed":         9,  # *
                 "mass":              4,  # * must be less then max_speed
                 "maneuver_ability":  2,  # *
                 "health":            90,  # *
                 "main_weapon":       medium_cannon,  # *
                 "sec_weapon":        fast_missle,  # *
                 "snag":              snag,
                 "detected_radius":   1000,
                 "effect":            "explosion_3"
                 }

yak1         =  {"type":              Airplane,  # *
                 "name":              "YAK-1",  # * for meny show
                 "bitmap_path":       img_dir + 'yak1.png',  # *
                 "max_speed":         9,  # *
                 "mass":              4,  # * must be less then max_speed
                 "maneuver_ability":  1.7,  # *
                 "health":            100,  # *
                 "main_weapon":       medium_cannon,  # *
                 "sec_weapon":        medium_missle,  # *
                 "snag":              snag,
                 "detected_radius":   1000,
                 "effect":            "explosion_3"
                 }

arado        =  {"type":              Airplane,  # *
                 "name":              "Arado",  # * for meny show
                 "bitmap_path":       img_dir + 'arado.png',  # *
                 "max_speed":         5,  # *
                 "mass":              2.5,  # * must be less then max_speed
                 "maneuver_ability":  0,  # *
                 "health":            1000,  # *
                 "main_weapon":       power_cannon,  # *
                 "sec_weapon":        bomb,  # *
                 "snag":              snag,
                 "detected_radius":   1000,
                 "effect":            "explosion_3"
                 }

shilka        = {"type":              Airdefence,  # *
                 "name":              "Shilka",  # * for meny show
                 "bitmap_path":       img_dir + 'towergun.png',  # *
                 "base":              img_dir + 'base.png',
                 "mass":              7,  # *
                 "maneuver_ability":  0.5,  # *
                 "health":            40,  # *
                 "main_weapon":       fast_cannon,  # *
                 "sec_weapon":        fast_missle,  # *
                 "snag":              snag,
                 "detected_radius":   3000,
                 "effect":            "explosion_3"
                 }

strela        = {"type":              Airdefence,  # *
                 "name":              "Strela",  # * for meny show
                 "bitmap_path":       img_dir + 'towergun.png',  # *
                 "base":              img_dir + 'base.png',
                 "mass":              7,  # *
                 "maneuver_ability":  1,  # *
                 "health":            70,  # *
                 "main_weapon":       power_cannon,  # *
                 "sec_weapon":        fast_missle,  # *
                 "snag":              snag,
                 "detected_radius":   2000,
                 "effect":            "explosion_3"
                 }

c3000         = {"type":              Airdefence,  # *
                 "name":              "C3000",  # * for meny show
                 "bitmap_path":       img_dir + 'towergun.png',  # *
                 "base":              img_dir + 'base.png',
                 "mass":              7,  # *
                 "maneuver_ability":  1,  # *
                 "health":            70,  # *
                 "main_weapon":       power_missle,  # *
                 "sec_weapon":        power_missle,  # *
                 "snag":              snag,
                 "detected_radius":   1000,
                 "effect":            "explosion_3"
                 }

player = [la5, spitfire, mig3, fw190, ta152, p51d, hawker, yak1, he162]
