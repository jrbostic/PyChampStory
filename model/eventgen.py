from Tkinter import *
from itemgen import ItemGenerator

__author__ = 'jessebostic'

"""Returns randomized event"""


class EventGenerator:

    ITEM_GEN = ItemGenerator()

    def __init__(self):
        pass

    def generate_event(self):

        return self.GameEvent()


    class GameEvent():

        def __init__(self):

            self.item = EventGenerator.ITEM_GEN.generate_item()
            self.event_window = None

        def render_event(self, root, tilex, tiley):

            self.event_window = Toplevel(root)
            self.event_window.title("An Event")

            message = Message(self.event_window, text="An event has occurred at tile ("
                                                      + str(tilex) + ", " + str(tiley) + ")")
            message.pack()
            button = Button(self.event_window, text="Run Away", command=self.event_window.destroy)
            button.pack()

            x = root.winfo_rootx()
            y = root.winfo_rooty()
            geom = "+%d+%d" % (x + root.winfo_width()/2, y + root.winfo_height()/3)

            self.event_window.geometry(geom)
            self.event_window.grab_set()
            self.event_window.focus_set()
            button.focus_set()
            self.event_window.transient(root)
