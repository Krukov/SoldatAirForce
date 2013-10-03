#!/usr/bin/python
#-*- coding: utf-8 -*-

from unit_param import *

## ( unit param, length, wight, direction, start speed)
## units - spitfire, mig3, fw190, ta152, p51d, la5, hawker, yak1, he162, arado, shilka, strela, c3000


class mist(object):
    Easy = {
            'player': (100, 200, 'right', None),
            'enemy': ((ta152, 5700, 100, 'left', None),),
            'friends': (),
            'target': 'destroy all'
            }

    Medium = {
            'player': (100, 300, 'right', None),
            'enemy': ((shilka, 6330, 1000, 'left', 1), (fw190, 6700, 300, 'left', None),
                       (spitfire, 6500, 500, 'left', None)),
            'friends': ((mig3, 300, 100, 'right', None),),
            'target': 'destroy all'
            }

    Hard = {
            'player': (300, 100, 'right', None),
            'enemy': ((shilka, 6700, 1100, 'left', 1), (p51d, 6700, 300, 'left', None),
                      (p51d, 6700, 100, 'left', None), (spitfire, 6500, 200, 'left', None)),
            'friends': ((mig3, 200, 200, 'right', None), (arado, 100, 500, 'right', None),
                       (strela, 3000, 1300, 'right', None)),
            'target': 'Save Arado'
            }


class normans(object):
    Easy = {
            'player': (100, 200, 'right', None),
            'enemy': ((spitfire, 5700, 100, 'left', None), (hawker, 5700, 300, 'left', None)),
            'friends': ((yak1, 100, 100, 'right', None),),
            'target': 'destroy all'
            }

    Medium = {
            'player': (100, 300, 'right', None),
            'enemy': ((strela, 3500, 1500, 'left', 1),
                    (fw190, 5750, 1000, 'left', None), (c3000, 5550, 1650, 'left', 1)),
            'friends': ((he162, 500, 100, 'right', None),),
            'target': ''
            }

    Hard = {
            'player': (100, 300, 'right', None),
            'enemy': ((arado, 5700, 300, 'left', None), (p51d, 5600, 100, 'left', None),
                    (p51d, 5600, 200, 'left', None), (hawker, 5400, 1000, 'left', None),
                    (hawker, 5200, 1000, 'left', None)),
            'friends': ((shilka, 3100, 1300, 'right', 0),
                    (strela, 2050, 1500, 'right', 0), (fw190, 100, 500, 'right', None))
            }
