from control import *
from model import *
from view import *

__author__ = 'jessebostic'

class Coupler:

    def __init__(self, board):
        self.board = board
        self.listeners = []

    def attach_listener(self, my_callback):
        self.listeners.append(my_callback)

    def listen_up(self, type=None, data=None):
        for obs in self.listeners:
            obs(type=type, data=data)
