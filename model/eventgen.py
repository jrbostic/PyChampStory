from Tkinter import *
from itemgen import ItemGenerator
import random

__author__ = 'jessebostic'

"""Returns randomized event"""


class EventGenerator:
    ITEM_GEN = ItemGenerator()

    def __init__(self):
        pass

    def generate_event(self):

        return self.GameEvent()


    class GameEvent():

        TYPES = ['gift', 'input', 'options']

        # dict of game type to list of event tuple
        # { type : [(console message, win title, win text, [(component type, text, command), ... ], accomplished)]
        DETAIL_DICT = {
            'gift': [("Gift Event Occurred", "Discovered an Item!", "You found {}!",
                      [('button', "Take It", True), ('button', "Leave It", False)], False)],
            'input': [("Input Event Occurred", "Type Command", "A barrel is coming for you...",
                       [('validator', "Entry TEXT", None),('button', "Do", None),('button', "Run Away", None)], False)],
            'options': [("Options Event Occurred", "Select an Option", "Which of these is a string?", [('button', "5", False),
                                                                                                       ('button', "4.53", False),
                                                                                                       ('button', "False", False),
                                                                                                       ('button', "'hello'", True)], False)]}



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
                    w = Button(frame, text=widget[1], command=lambda booly=widget[2]: self.eval_success(herometer, booly))
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

