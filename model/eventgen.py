"""
Contains support for selecting random events from a set of known events.

In retrospect, the intended design was not implemented, rendering the inner class unnecessary.
This should be corrected at some point.
"""

from Tkinter import *
from itemgen import ItemGenerator
import random

__author__ = 'jessebostic'


class EventGenerator:
    """Class for creating a generator object that can serve events."""

    # an item generator to attach random items into event
    ITEM_GEN = ItemGenerator()

    def __init__(self):
        """Not much of an object..."""
        pass

    def generate_event(self):
        """Generates a new game event.

        :return randomly selected event
        """
        return self.GameEvent()


    class GameEvent():

        TYPES = ['gift', 'input', 'options']

        # dict of game type to list of event tuple... should probably be in a db
        # { type : [(console message, win title, win text, [(component type, text, command), ... ], accomplished)]
        DETAIL_DICT = {
            'gift': [("Found something!", "Discovered an Item!", "You found a {}!",
                      [('button', "Take It", True), ('button', "Leave It", False)], False),
                     ("Found something!", "Discovered an Item!",
                      "You tripped over something in the ground which appears to be a {}!",
                      [('button', "Dig It Out", True), ('button', "Leave It Buried", False)], False),
                     ("Offered something!", "Offered an Item!",
                      "You meet a strange old man with gnarly toenails... he offers you a {}!",
                      [('button', "'Thank you!'", True), ('button', "'No thanks, weirdo...'", False)], False),
                     ("Offered something!", "Offered an Item!", "A young girl pops out of nowhere and offers you a {}!",
                      [('button', "'Just what I wanted!'", True), ('button', "'Get lost kid.'", False)], False),
                     ("Offered something!", "Offered an Item!",
                      "A strange light appears in front of you... a shape begins to appear... it's a {}!",
                      [('button', "Take It (so as not to anger the gods)", True),
                       ('button', "'That light is annoying...'", False)], False)],
            'input': [("Whoa!  Think fast!", "Type Command", "A barrel is coming for you...",
                       [('validator', "Entry TEXT", None),('button', "Do", None),('button', "Run Away", None)], False),
                      ("Whoa!  Think fast!", "Type Command", "A tree branch falls, blocking your path!",
                       [('validator', "Entry TEXT", None),('button', "Do", None),
                        ('button', "Walk Around", None)], False),
                      ("Yikes!", "Type Command",
                       "Some kind of crazy looking alien mutant animal stands in front of you licking its lips!",
                       [('validator', "Entry TEXT", None),('button', "Do", None),
                        ('button', "'I\'m getting out of here!'", None)], False),
                      ("CAAAAAWWW!", "Type Command",
                       "A large bird flies directly overhead and apparently begins using the bathroom.",
                       [('validator', "Entry TEXT", None),('button', "Do", None),
                        ('button', "'Oh well... I don't mind.'", None)], False),
                      ("Dance off!", "Type Command",
                       "An ill break dancer wants to do a head on break dance battle against you.",
                       [('validator', "Entry TEXT", None),('button', "Do", None),
                        ('button', "'I don't dance...'", None)], False),
                      ("A treasure revealed!", "Type Command", "A young boy tells you of a treasure on tile "
                       + str(random.randint(1, 100)),
                       [('validator', "Entry TEXT", None),('button', "Do", None),
                        ('button', "Yea right...", None)], False)],
            'options': [("Super Quiz!", "Select an Option", "Which of these is a string?",
                         [('button', "5", False), ('button', "4.53", False), ('button', "False", False),
                          ('button', "'hello'", True)], False),
                        ("Test Time!", "Select an Option", "Which is not a boolean value?",
                         [('button', "True", False), ('button', "False", True), ('button', "None", False)], False),
                        ("Super Quiz!", "Select an Option",
                         "Given list THE_LIST=[3, 6, 9], what is the value of THE_LIST[0]",
                         [('button', "3", True), ('button', "6", False),('button', "9", False),
                          ('button', "'BOOP'", False)], False),
                        ("Super Quiz!", "Select an Option", "Given dict THE_DICT={'pig':'pink', 'dog':'brown', "
                                                            "'cat':'purple'}, what is the value of THE_DICT['dog']",
                         [('button', "'pink'", False), ('button', "'brown'", True), ('button', "'puple'", False),
                          ('button', "'kangaroo'", False)], False),
                        ("Test Time!", "Select an Option", "This game is awesome!  \nTrue or False?",
                         [('button', "True", True),('button',"False", False)], False),
                        ("Test Time!", "Select an Option", "A list is a type of number.  \nTrue or False?",
                         [('button', "True", False),('button', "False", True)], False),
                        ("Test Time!", "Select an Option", "An int is a type of number.  \nTrue or False?",
                         [('button', "True", True),('button', "False", False)], False),
                        ("Test Time!", "Select an Option", "A float is a type of number.  \nTrue or False?",
                         [('button', "True", True),('button', "False", False)], False),
                        ("Test Time!", "Select an Option", "An int is a type of string.  \nTrue or False?",
                         [('button', "True", False),('button', "False", True)], False),
                        ("Test Time!", "Select an Option", "The maker of this game must be rich!  \nTrue or False?",
                         [('button', "True", False),('button', "False", True)], False),
                        ("Test Time!", "Select an Option", "This game needs thousands of hours of work still.  "
                                                           "\nTrue or False?",
                         [('button', "True", True), ('button', "False", False)], False)]}



        def __init__(self):

            self.event_window = None  # this is basically private

            self.event_type = None  # will allow for diff types of games

            self.event_item = None

            self.event_message = None  # for output box in main window
            self.event_title = None  # for toplevel window title
            self.event_text = None  # the challenge description

            self.event_widgets = None

            self.accomplished = False

            self.generate()

        def generate(self):

            self.event_type = random.choice(self.TYPES)
            self.event_item = EventGenerator.ITEM_GEN.generate_item()

            event_details = random.choice(self.DETAIL_DICT[self.event_type])
            #if event_details is not None:
            self.event_message = event_details[0]
            self.event_title = event_details[1]
            self.event_text = event_details[2]

            self.event_widgets = event_details[3]

            self.accomplished = event_details[4]

        def eval_success(self, herometer, success):
            self.accomplished = success
            if success:
                herometer.add_to_bag(self.event_item)
                herometer.board.coupler.add_job({"item_display": "just fire it"})
            self.event_window.destroy()


        def render_event(self, root, herometer, tilex, tiley):

            self.event_window = Toplevel(root)
            self.event_window.title(self.event_title)

            # put message into the window
            if self.event_type == 'gift':
                self.event_text = self.event_text.format(self.event_item.name)
            message = Message(self.event_window, text=self.event_text, width=200)

            # bottom panel of buttons (options basically)
            frame = Frame(self.event_window)
            b_count = 0
            for widget in self.event_widgets:
                b_count += 1
                w = None
                if widget[0] == 'button':
                    w = Button(frame, text=widget[1],
                               command=lambda booly=widget[2]: self.eval_success(herometer, booly))
                    w.grid(row=0, column=b_count, sticky=NW+SE)
                elif widget[0] == 'validator':
                    import view.validator
                    w = view.validator.InputField(frame, herometer)#Entry(frame, text=widget[1])
                    w.entry.grid(row=0, column=b_count, sticky=NW+SE)

            message.pack(expand=1)
            frame.pack(anchor=CENTER)

            #set size and location
            x = root.winfo_rootx()
            y = root.winfo_rooty()
            geom = "%dx%d%+d%+d" % (root.winfo_width() / 2, root.winfo_height() / 2,
                                    x + root.winfo_width() / 4, y + root.winfo_height() / 4)

            # makes event win appear, in focus, remaining at front
            self.event_window.geometry(geom)
            self.event_window.grab_set()
            self.event_window.focus_set()
            self.event_window.transient(root)

