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

        self.form = 1 #practice
        self.rigor = 1 #precision
        self.spunk = 1 #perseverance
        self.knowledge = 1

        self.cash = 0
        self.bag = []

    def set_board(self, board):
        """Attach the board"""

        self.board = board

    def move(self, number):
        """Moves toward number specified (using board logic)"""

        if 1 > number or number > 100:
            return "You crazy man... philosophical... seriously."

        else:
            # origin = str(self.curr_tile)
            self.dest_tile = {'x': (number - 1) % 10, 'y': (number - 1) // 10}
            cont = True
            while self.curr_tile != self.dest_tile and cont:
                cont = self.board.step(self)
            self.dest_tile = self.curr_tile #if move breaks early by event, player will start where interrupted

    def use(self, string):
        return self.name + " uses {}.".format(string)

    def jump(self, string):
        return self.name + " jumped over {}!".format(string)

    def search(self, string):
        list = ["nothing at all", "a hat", "some underwear", "cash", "a badge of honor"]
        return self.name + " searches... and finds " + random.choice(list) + "!"

    def open(self, string):
        return self.name + " opens the " + string + '!'

    def say(self, string):
        return self.name + " says '" + string + "'."

    # def ask(self, string):
    #     return self.name + " asks '" + string + "?'"

    def __copy__(self):
        """Returns copy of hero state (need to figure out pythonic copy process)"""

        if self is not None:
            aCopy = Hero(self.name)
            aCopy.curr_tile = copy.deepcopy(self.curr_tile)
            aCopy.dest_tile = copy.deepcopy(self.dest_tile)
            return aCopy

    def __str__(self):
        return str(self.curr_tile) + " " + str(self.dest_tile)