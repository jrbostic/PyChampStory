import time
import threading
import random

__author__ = 'jessebostic'

class Hero:

    def __init__(self, name):
        self.name = name
        self.curr_tile = {'x': 0, 'y': 0}
        self.dest_tile = self.curr_tile

    def _set_board(self, board):
        self.board = board

    def move(self, number):

        if 1 > number or number > 100:
            return "You crazy man... philosophical... seriously."
        else:
            origin = str(self.curr_tile)
            self.dest_tile = {'x': (number-1)%10, 'y': (number-1)//10}
            while self.curr_tile != self.dest_tile:
                self.board.step()
            return self.name + " moved to tile at " + str(self.dest_tile) + " from tile at " + origin + "!"

    def jump(self):
        return self.name + " jumped!"

    def search(self):
        return self.name + " searches... and finds " + self._search() + "!"

    def breakdance(self):
        return self.name + " busts a sweet move!"

    def open(self):
        return "There's nothing for " + self.name + ' to open!'

    def say(self, string):
        return self.name + " says '" + string + "'."

    def _search(self):

        list = ["nothing at all", "a hat", "some underwear", "cash", "a badge of honor"]
        return random.choice(list)
