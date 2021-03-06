"""
Holds entry widget for validating user input and selecting color.
"""

from Tkinter import *

__author__ = "jesse bostic"

class InputField():
    """Takes and processes user input (should probably inherit from Entry class)"""

    def __init__(self, root, herometer):
        """Sets up entry box and validation command.

        :param root: the root widget
        :param herometer: reference to herometer
        """

        # See: http://stackoverflow.com/questions/4140437/python-tkinter-interactively-validating-entry-widget-content
        vcmd = (root.register(self.on_validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry = Entry(root, validate="key",
                           validatecommand=vcmd)

        self.is_executable = False
        self.herometer = herometer

    def on_validate(self, d, i, P, s, S, v, V, W):
        """Validates textbox input and determining color text box contents

        :param P: user input string
        """

        # Keep this for future modification (very interesting)
        # print "DEBUG OUTPUT:"
        # print "d='%s'" % d
        # print "i='%s'" % i
        # print "P='%s'" % P
        # print "s='%s'" % s
        # print "S='%s'" % S
        # print "v='%s'" % v
        # print "V='%s'" % V
        # print "W='%s'" % W

        is_complete = self.herometer.validate_input(P.lstrip())

        self.is_executable = False

        if is_complete is None:
            self.entry.config(fg='#FF0000')
        elif is_complete is False:
            self.entry.config(fg='#038357')
        else:
            self.entry.config(fg='#5700FF')
            self.is_executable = True

        return True

