"""
Contains the Herometer control structure, a varied source of communication
between the board views and models.  Also holds the regex data structure which
is used to validate user input.
"""

from model.protag import Hero
from model.board import Board
import inspect
import re

__author__ = 'Jesse Bostic'


class Herometer:
    """Class providing functionality to format data and mutate
    state of models via activities originating in view.
    """

    def __init__(self, hero_name):
        """Creates hero and board objects, couples them, and builds regex call tables.

        :param hero_name: name of hero
        """

        # couple hero and board so they can mediate their own crap.
        self.hero = Hero(hero_name)
        self.board = Board(self.hero)
        self.hero.set_board(self.board)

        # build up data structures for display and validation
        self._build_ability_table(Hero)
        self.calls = self._build_calls_table()

    def _build_ability_table(self, the_class):
        """Builds up a dictionary of method to params

        :param the_class: the name of class to build table from
        :return: None
        """

        method_list = inspect.getmembers(the_class, predicate=inspect.ismethod)

        usable_methods = [meth[0] for meth in method_list if meth[0][0] is not '_']
        method_params = [inspect.getargspec(getattr(the_class, meth))[0][1:] for meth in usable_methods]
        complete_table = {usable_methods[i]: method_params[i] for i in xrange(len(usable_methods))}

        self.abilities = complete_table

    def _build_calls_table(self):
        """Builds up internal data structure to validate user input against.
        First index is string, after that regex for variable comparisons.

        :return: the regex data structure used to validate
        """

        regex_key = []
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

            regex_key.append(method_matcher)

        return regex_key

    def validate_input(self, the_input):
        """Validates user input and returns whether a fully matching call exists.

        :param the_input: the string to test
        :return: True for full match, False for partial, None for no match
        """

        matches = [False, False, False]

        # partial sequential and regex match
        for call in self.calls:
            matches[0] = matches[0] or the_input == call[0][0:len(the_input)]

        for partialRegex in self.calls:
            for list_of_regex in partialRegex[1]:
                matches[0] = matches[0] or list_of_regex.match(the_input) is not None

        # full regex match -bad naming convention
        for fullRegex in self.calls:
            for list_of_regex in fullRegex[2]:
                matches[1] = matches[1] or list_of_regex.match(the_input) is not None

        if matches[1]:
            return True
        elif matches[0]:
            return False
        else:
            return None

    @staticmethod
    def execute_method(self, text):
        """Executes user-issued command.

        :param text: the validated command to execute
        :return anything returned by text code (usually console output for action)
        """

        result = ''
        if text is not None:
            exec "result = self.hero." + text
        return result

    def get_hero_position(self):
        """Get hero x and y board location (the tile occupied).
        Kind of strange to have this here... should probably be routing
        this through the coupler.

        :return dict containing x and y locations (keys: 'x', 'y')
        """

        return self.hero.curr_tile

    def get_available_methods(self):
        """Provides formatted list of available methods for display.

        :return list of method call string reps
        """

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
        """Gets reference to job queue 'coupler'.

        :return coupler for adding jobs to event loop
        """

        return self.board.coupler

    def get_stats(self):
        """Returns a set of hero stats to display in game window.

        :return:list of tuples [(stat_name, stat_value), ...]
        """

        h = self.hero
        stats = [('KNOWLEDGE', h.knowledge), ('', ''), ('FORM', h.form), ('RIGOR', h.rigor),
                 ('SPUNK', h.spunk), ('', ''), ('CASH', "$"+str(h.cash))]
        return stats

    def add_to_bag(self, the_item):
        """Pushes passed item into hero bag.

        :param the_item: item to add to back
        :return: None
        """
        self.hero.bag.append(the_item)
