"""
Contains the model for board object.
"""

import random
from eventgen import EventGenerator
from control.thethievesbounty import Coupler
from protag import Hero


class Board:
    """Class for creating board to handle tile state and board events"""

    def __init__(self, hero):
        """Initialize at level 0, setup layout and coupler"""

        self.coupler = Coupler()

        self.level = 0
        self.layout = self._construct_layout()

        #adds delay to discovery coloring of tile (and sets up necessary tile state)
        self.coupler.add_job({'message': "Welcome to the Realm of PyChamp!",
                              'board': self._copy_layout(), 'hero': hero})
        self.layout[0][0].visited = True
        self.coupler.add_job({'message': "Your adventure begins...",
                              'board': self._copy_layout(), 'hero': Hero('Default')})

    def _construct_layout(self, ref=None):
        """Create layout, a multidimensional array, 10 x 10
        Optionally acts as a copy constructor for tile state.

        :param ref: tile array to copy
        :return multidimensional board array
        """

        the_layout = []
        for i in xrange(10):
            the_layout.append([])
            for n in xrange(10):
                if ref is not None:
                    the_layout[i].append(ref.layout[n][i].copy())
                else:
                    the_layout[i].append(self.Tile(n, i, self.level))

        the_layout[0][0].event = None  # first tile has no event

        return the_layout

    def step(self, hero):
        """Handles a single hero step on board.

        :param hero: hero object to step
        :return False if event is encountered, True otherwise
        """

        # current and destination tiles
        currx = hero.curr_tile['x']
        curry = hero.curr_tile['y']
        destx = hero.dest_tile['x']
        desty = hero.dest_tile['y']

        # super basic routing algorithm
        if currx < destx:
            hero.curr_tile['x'] += 1
        elif curry < desty:
            hero.curr_tile['y'] += 1
        elif currx > destx:
            hero.curr_tile['x'] -= 1
        elif curry > desty:
            hero.curr_tile['y'] -= 1

        # convert x and y values to numbers (1-100)
        last_tile_num = curry * 10 + currx + 1
        currx = hero.curr_tile['x']
        curry = hero.curr_tile['y']
        curr_tile_num = curry * 10 + currx + 1

        self.layout[curry][currx].visited = True

        # constructs console output and queues up job
        console_message = hero.name + " moved from tile " + str(last_tile_num) + " to tile " + str(curr_tile_num)
        self.coupler.add_job({'message': console_message, 'board': self._copy_layout(), 'hero': hero.__copy__()})

        self.layout[curry][currx].first_time = False

        # returns whether event was not encountered on this step
        return self.layout[hero.curr_tile['y']][hero.curr_tile['x']].event is None

    def _copy_layout(self):
        """Copies layout of board for Coupler input

        :return copy of board tiles
        """

        return self._construct_layout(ref=self)

    def __iter__(self):
        """Iteration of a board is simply its tiles in order."""

        for row in self.layout:
            for tile in row:
                yield str(tile)

    def __str__(self):
        """String representation of layout

        :return simple string rep of board
        """

        the_string = ''
        for tile in self:
            the_string += tile + ", "
        return the_string

    class Tile:
        """Class for constructing board tiles."""

        # lazy weighted colors base on freq... temporary... demonstration value
        LEVEL_COLORS = ['#102510', '#102510', '#102510', '#102510', '#102510', '#232110', '#101022']
        EVENT_GEN = EventGenerator()

        def __init__(self, x, y, level):
            """Sets up coordinates, whether visited, terrain color, and random events

            :param x: x location of tile
            :param y: y location of tile
            :param level: level of current board (important for future progression)
            :return: a new tile with all features
            """

            self.x = x
            self.y = y
            self.first_time = True
            self.visited = False
            self.bg = random.choice(self.LEVEL_COLORS)

            # approx 40 percent of tiles have events
            if random.random() < .4:
                self.event = self.EVENT_GEN.generate_event()
            else:
                self.event = None

        def copy(self):
            """Returns a complete copy of self.

            :return copy of this tile
            """

            new_tile = Board.Tile(self.x, self.y, 0)
            new_tile.first_time = self.first_time
            new_tile.visited = self.visited
            new_tile.bg = self.bg
            new_tile.event = self.event

            return new_tile

        def __str__(self):
            """String rep of some tile state.

            :return basic string rep of tile
            """

            return "Coord( " + str(self.x) + ', ' + str(self.y) + ' )' + "; Visited=" + str(self.visited)