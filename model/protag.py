__author__ = 'jessebostic'

class Hero:

    def __init__(self, name):
        self.name = name

    def move(self, number):
        return self.name + " moved to tile " + str(number) + "!"

    def jump(self):
        return self.name + " jumped!"

    def search(self):
        return self.name + " searches... and finds nothing!"