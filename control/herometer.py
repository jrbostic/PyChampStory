from model.protag import Hero
from model.board import Board
import inspect
import re

__author__ = 'Jesse Bostic'


class Herometer:
    """All functionality to format data and move Hero state info to view"""

    def __init__(self, hero_name):

        # couple hero and board so they can mediate their own crap.
        self.hero = Hero(hero_name)
        self.board = Board(self.hero)
        self.hero._set_board(self.board)  # in this instance, I'm deeming this okay

        self.abilities = self._build_ability_table(inspect.getmembers
                                                   (Hero, predicate=inspect.ismethod))
        self.calls = self._build_calls_table()


    def _build_ability_table(self, methodList):
        """Builds up a dictionary of method to params"""

        usable_methods = [meth[0] for meth in methodList if meth[0][0] is not '_']
        method_params = [inspect.getargspec(getattr(Hero, meth))[0][1:] for meth in usable_methods]
        complete_table = {usable_methods[i]: method_params[i] for i in xrange(len(usable_methods))}
        return complete_table

    def _build_calls_table(self):
        """First index is string, after that regex for variable comparisons"""

        regexKey = []
        for meth in self.abilities.keys():
            aMethod = []
            aMethod.append(meth + '(')
            aMethod.append(re.compile(r'^' + meth + r'[\s]*$'))
            aMethod.append(re.compile(r'^' + meth + r'[\s]*\($'))
            if len(self.abilities[meth]):
                for param in self.abilities[meth]:
                    if param == 'number':
                        aMethod.append(re.compile(r'^' + meth + r'[\s]*\([\s]*$'))
                        aMethod.append(re.compile(r'^' + meth + r'[\s]*\([\s]*[0-9]+$'))
                        aMethod.append(re.compile(r'^' + meth + r'[\s]*\([\s]*[0-9]+[\s]*$'))
                        aMethod.append(re.compile(r'^' + meth + r'[\s]*\([\s]*[0-9]+[\s]*\)$'))
                    elif param == 'string':
                        aMethod.append(re.compile(r'^' + meth + r'\([\s]*["]?$'))
                        aMethod.append(re.compile(r'^' + meth + r'\([\s]*["][\w\s]*$'))
                        aMethod.append(re.compile(r'^' + meth + r'\([\s]*["][\w\s]*["]?$'))
                        aMethod.append(re.compile(r'^' + meth + r'\([\s]*["][\w\s]*["][\s]*$'))
                        aMethod.append(re.compile(r'^' + meth + r'\([\s]*["][\w\s]*["][\s]*\)$'))
            else:
                aMethod.append(re.compile(r'^' + meth + r'[\s]*\([\s]*$'))
                aMethod.append(re.compile(r'^' + meth + r'[\s]*\([\s]*\)$'))
            regexKey.append(aMethod)
        return regexKey

    def validate_input(self, theInput):
        """Return True for full match, False for partial, None for no match"""

        #somewhat superfluous structure to hold match state
        matches = []

        #partial string match
        match0 = False
        for call in self.calls:
            test_string = ''
            for char in theInput:
                test_string = call[0][0:len(test_string) + 1]
                match0 = match0 or test_string == theInput

        #partial regex match
        match1 = False
        for partialRegex in self.calls:
            for i in xrange(1, len(partialRegex)-1):
                match1 = match1 or partialRegex[i].match(theInput)

        matches.append(match0 or match1)

        #full regex match
        match2 = False
        for fullRegex in self.calls:
            match2 = match2 or fullRegex[-1].match(theInput)

        matches.append(match2)

        if matches[1]:
            return True
        elif matches[0]:
            return False
        else:
            return None

    def execute_method(self, text):

        result = ''
        if text is not None:
            exec "result = self.hero." + text
        return result

    def get_hero_position(self):

        return self.hero.curr_tile

    def get_available_methods(self):

        method_list = []
        for meth in self.abilities:
            method_str = meth + '( '

            #determine how to display parameter in display string
            if (len(self.abilities[meth]) > 0) and self.abilities[meth][0]=='number':
                method_str += '#' #self.abilities[meth][0]
            if (len(self.abilities[meth]) > 0) and self.abilities[meth][0]=='string':
                method_str += '~' #self.abilities[meth][0]

            method_str += ' )'
            method_list.append(method_str)

        return method_list

    def get_board_coupler(self):

        return self.board.the_coupler
