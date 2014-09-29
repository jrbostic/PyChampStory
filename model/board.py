import time
import threading
from eventgen import EventGenerator
from model.protag import *

from control.thethievesbounty import Coupler


class Board:

    def __init__(self, hero):
        self.hero = hero
        self.level = 0
        self.layout = self._construct_layout()

        self.the_coupler = Coupler(self)

    def _construct_layout(self):
        the_layout = []
        for i in xrange(10):
            the_layout.append([])
            for n in xrange(10):
                the_layout[i].append(self.Tile(i, n, self.level))
        return the_layout

    def step(self):
        currx = self.hero.curr_tile['x']
        curry = self.hero.curr_tile['y']
        destx = self.hero.dest_tile['x']
        desty = self.hero.dest_tile['y']

        if currx < destx:
            self.hero.curr_tile['x'] += 1
        elif curry < desty:
            self.hero.curr_tile['y'] += 1
        elif currx > destx:
            self.hero.curr_tile['x'] -= 1
        elif curry > desty:
            self.hero.curr_tile['y'] -= 1

        last_tile_num = curry*10+currx+1 #if currx+1<10 else (curry+1)*10+currx+1
        currx = self.hero.curr_tile['x'] ##reassign
        curry = self.hero.curr_tile['y']
        curr_tile_num = curry*10+currx+1 #if currx+1<10 else (curry+1)*10+currx+1

        console_message = self.hero.name + " moved from tile " + str(last_tile_num) + " to tile " + str(curr_tile_num)
        self.the_coupler.listen_up(type="consoleupdate", data=console_message)
        self.the_coupler.listen_up(type="mapupdate", data=(currx, curry))

        time.sleep(1)

    def __iter__(self):
        for row in self.layout:
            for tile in row:
                yield str(tile)

    class Tile:

        # color order shoudl be green, blue, purple, orange, yellow, red
        LEVEL_COLORS = [0xFFFFF1, 0xFFFFF2, 0xFFFFF3, 0xFFFFF4, 0xFFFFF5, 0xFFFFF6]
        EVENT_GEN = EventGenerator()

        def __init__(self, x, y, level):
            self.x = x
            self.y = y
            self.bg = self.LEVEL_COLORS[level]
            self.event = self.EVENT_GEN.generate_event()

        def __str__(self):
            return "Coord( " + str(self.x) + ', ' + str(self.y) + ' )' + "; Color=" + str(self.bg)