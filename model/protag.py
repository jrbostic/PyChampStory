"""
Contains protagonist state and methods.  Perhaps would contain a
pet class in the future for instantiating a secondary object to
call methods from.
"""

import random
import copy

__author__ = 'jessebostic'


class Hero:
    """The PyChamp resides here (mostly methods for ability list parsing)"""

    def __init__(self, name):
        """Initialize name and coordinates"""

        self.name = name
        self.curr_tile = {'x': 0, 'y': 0}
        self.dest_tile = self.curr_tile

        self.board = None

        # hero stat values
        self.form = 1  # practice
        self.rigor = 1  # precision
        self.spunk = 1  # perseverance
        self.knowledge = 1

        self.cash = 0
        self.bag = []

    def _set_board(self, board):
        """Attach the board.

        :param board: the board to attach
        :return None
        """

        self.board = board

    def move(self, number):
        """Moves toward number specified (using board logic)

        :param number: the target tile
        :return console output string if out of range, None otherwise
        """

        if 1 > number or number > 100:
            return "You crazy man... philosophical... seriously."

        else:
            self.dest_tile = {'x': (number - 1) % 10, 'y': (number - 1) // 10}
            cont = True

            # step until event is encountered, then clear destination
            while self.curr_tile != self.dest_tile and cont:
                cont = self.board.step(self)
            self.dest_tile = self.curr_tile

    def use(self, string):
        """Stub for a use('item_name') type of functionality"""
        return self.name + " uses {}.".format(string)

    def jump(self, string):
        """Stub for a jump('obstacle') type of functionality"""
        return self.name + " jumped over {}!".format(string)

    def search(self, string):
        """Stub for a search() or search('contain') type of function"""
        a_list = ["nothing at all", "a hat", "some underwear", "cash", "a badge of honor"]
        return self.name + " searches... and finds " + random.choice(a_list) + "!"

    def open(self, string):
        """Stub for open('port') type of function"""
        return self.name + " opens the " + string + '!'

    def say(self, string):
        """Stub for a way to talk in game"""
        return self.name + " says '" + string + "'."

    # def ask(self, string):
    #     return self.name + " asks '" + string + "?'"

    def __copy__(self):
        """Returns copy of hero state (need to figure out pythonic copy process)

        :return copy of hero
        """

        if self is not None:
            aCopy = Hero(self.name)
            aCopy.curr_tile = copy.deepcopy(self.curr_tile)
            aCopy.dest_tile = copy.deepcopy(self.dest_tile)
            return aCopy

    def __str__(self):
        """Get hero string rep.

        :return: string rep of this hero object
        """
        return str(self.curr_tile) + " " + str(self.dest_tile)