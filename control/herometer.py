from model.protag import Hero
from model.board import Board
import inspect
import re

__author__ = 'Jesse Bostic'


class Herometer:
    """All functionality to format data and move Hero state info to view"""

    def __init__(self, hero_name):
        """Sets up interface to hero abilities data (so far)"""

        # couple hero and board so they can mediate their own crap.
        self.hero = Hero(hero_name)
        self.board = Board(self.hero)
        self.hero._set_board(self.board)  # in this instance, I'm deeming this okay

        self._build_ability_table(inspect.getmembers
                                                   (Hero, predicate=inspect.ismethod))
        self.calls = self._build_calls_table()

    def _build_ability_table(self, methodList):
        """Builds up a dictionary of method to params"""

        usable_methods = [meth[0] for meth in methodList if meth[0][0] is not '_']
        method_params = [inspect.getargspec(getattr(Hero, meth))[0][1:] for meth in usable_methods]
        complete_table = {usable_methods[i]: method_params[i] for i in xrange(len(usable_methods))}

        self.abilities = complete_table

    def _build_calls_table(self):
        """First index is string, after that regex for variable comparisons"""

        regexKey = []
        for meth in self.abilities.keys():

            method_matcher = [meth, [re.compile(r'^' + meth + r'\s*$'), re.compile(r'^' + meth + r'\s*\($')]]

            partial_re = None
            full_re = None

            if len(self.abilities[meth]):
                for param in self.abilities[meth]:

                    if param == 'number':
                        partial_re = [re.compile(r'^' + meth + r'\s*\(\s*$'),
                                      re.compile(r'^' + meth + r'\s*\(\s*[0-9]+$'),
                                      re.compile(r'^' + meth + r'\s*\(\s*[0-9]+\s*$'),
                                      re.compile(r'^' + meth + r'\s*\(\s*[0-9]+\s*\)$')]

                        full_re = [re.compile(r'^' + meth + r'\s*\(\s*[0-9]+\s*\)\s*$')]

                    elif param == 'string':
                        partial_re = [re.compile(r'^' + meth + r'\s*\(\s*"?$'),
                                      re.compile(r'^' + meth + r'\s*\(\s*"[\w\s]*$'),
                                      re.compile(r'^' + meth + r'\s*\(\s*"[\w\s]*"?$'),
                                      re.compile(r'^' + meth + r'\s*\(\s*"[\w\s]*"\s*$'),

                                      re.compile(r'^' + meth + r'\s*\(\s*[\']?$'),
                                      re.compile(r'^' + meth + r'\s*\(\s*[\'][\w\s]*$'),
                                      re.compile(r'^' + meth + r'\s*\(\s*[\'][\w\s]*[\']?$'),
                                      re.compile(r'^' + meth + r'\s*\(\s*[\'][\w\s]*[\']\s*$')]

                        full_re = [re.compile(r'^' + meth + r'\s*\(\s*"[\w\s]*"\s*\)$'),
                                   re.compile(r'^' + meth + r'\s*\(\s*"[\w\s]*"\s*\)\s*$'),

                                   re.compile(r'^' + meth + r'\s*\(\s*[\'][\w\s]*[\']\s*\)$'),
                                   re.compile(r'^' + meth + r'\s*\(\s*[\'][\w\s]*[\']\s*\)\s*$')]

            else:

                partial_re = [re.compile(r'^' + meth + r'\s*\(\s*$')]
                full_re = [re.compile(r'^' + meth + r'\s*\(\s*\)$'),
                           re.compile(r'^' + meth + r'\s*\(\s*\)\s*$')]

            method_matcher[1].extend(partial_re)
            method_matcher.append(full_re)

            regexKey.append(method_matcher)

        return regexKey

    def validate_input(self, theInput):
        """Return True for full match, False for partial, None for no match"""

        matches = [False, False, False]

        # partial sequential and regex match
        for call in self.calls:
            matches[0] = matches[0] or theInput == call[0][0:len(theInput)]

        for partialRegex in self.calls:
            for list_of_regex in partialRegex[1]:
                matches[0] = matches[0] or list_of_regex.match(theInput) is not None

        # full regex match -bad naming convention
        for fullRegex in self.calls:
            for list_of_regex in fullRegex[2]:
                matches[1] = matches[1] or list_of_regex.match(theInput) is not None

        if matches[1]:
            return True
        elif matches[0]:
            return False
        else:
            return None

    def execute_method(self, text):
        """Mediates execution of user-issued command"""

        result = ''
        if text is not None:
            exec "result = self.hero." + text
        return result

    def get_hero_position(self):
        """Returns current hero position"""

        return self.hero.curr_tile

    def get_available_methods(self):
        """Provides formatted list of available methods for display"""

        method_list = []
        for meth in self.abilities:
            method_str = meth + '( '

            # determine how to display parameter in display string
            if (len(self.abilities[meth]) > 0) and self.abilities[meth][0] == 'number':
                method_str += '#'  # self.abilities[meth][0]
            if (len(self.abilities[meth]) > 0) and self.abilities[meth][0] == 'string':
                method_str += '~'  # self.abilities[meth][0]

            method_str += ' )'
            method_list.append(method_str)

        return method_list

    def get_board_coupler(self):
        """Gets reference to coupler"""

        return self.board.coupler
