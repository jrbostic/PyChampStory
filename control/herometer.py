from model.protag import Hero
import inspect
import re

__author__ = 'Jesse Bostic'


class Herometer:
    """All functionality to format data and move Hero state info to view"""

    def __init__(self, hero):

        self.hero = hero
        self.abilities = self._build_ability_table(inspect.getmembers \
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
            if len(self.abilities[meth]):
                for param in self.abilities[meth]:
                    if param == 'number':
                        aMethod.append(re.compile(r'^' + meth + r'\([0-9]+$'))
                        aMethod.append(re.compile(r'^' + meth + r'\([0-9]+\)$'))
            else:
                aMethod.append(re.compile(r'^' + meth + r'\([\s]*$'))
                aMethod.append(re.compile(r'^' + meth + r'\([\s]*\)$'))
            regexKey.append(aMethod)
        return regexKey

    def validate_input(self, theInput):
        """Return True for full match, False for partial, None for no match"""

        match0 = False
        for call in self.calls:
            test_string = ''
            for char in theInput:
                test_string = call[0][0:len(test_string) + 1]
                match0 = match0 or test_string == theInput

        match1 = False
        for partialRegex in self.calls:
            match1 = match1 or partialRegex[1].match(theInput)

        match2 = False
        for fullRegex in self.calls:
            match2 = match2 or fullRegex[2].match(theInput)

        if match2:
            return True
        elif match1 or match0:
            return False
        else:
            return None