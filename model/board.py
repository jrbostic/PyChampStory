
import copy

from eventgen import EventGenerator
from control.thethievesbounty import Coupler


class Board:
    def __init__(self, hero):
        #self.hero = hero
        self.level = 0
        self.layout = self._construct_layout()

        self.coupler = Coupler()

    def _construct_layout(self):
        the_layout = []
        for i in xrange(10):
            the_layout.append([])
            for n in xrange(10):
                the_layout[i].append(self.Tile(i, n, self.level))
        return the_layout

    def step(self, hero):
        currx = hero.curr_tile['x']
        curry = hero.curr_tile['y']
        destx = hero.dest_tile['x']
        desty = hero.dest_tile['y']

        if currx < destx:
            hero.curr_tile['x'] += 1
        elif curry < desty:
            hero.curr_tile['y'] += 1
        elif currx > destx:
            hero.curr_tile['x'] -= 1
        elif curry > desty:
            hero.curr_tile['y'] -= 1

        last_tile_num = curry * 10 + currx + 1
        currx = hero.curr_tile['x']  # #reassign
        curry = hero.curr_tile['y']
        curr_tile_num = curry * 10 + currx + 1

        console_message = hero.name + " moved from tile " + str(last_tile_num) + " to tile " + str(curr_tile_num)
        self.coupler.add_job({'message': console_message, 'board': self.layout, 'hero': hero.__copy__()})

        return True #this will allow interuption of a move by event once implemented

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
            self.visited = False
            self.bg = self.LEVEL_COLORS[level]
            self.event = self.EVENT_GEN.generate_event()

        def __str__(self):
            return "Coord( " + str(self.x) + ', ' + str(self.y) + ' )' + "; Color=" + str(self.bg)