import Tkinter
import tkFont

__author__ = 'jessebostic'

class StatDisplay(Tkinter.Canvas):

    def __init__(self, root, herometer):
        Tkinter.Canvas.__init__(self, root)
        self.herometer = herometer
        self.frame = None
        self.update(self.herometer.get_stats())

    def update(self, stats):
        self.frame = Tkinter.Frame(self)

        font1 = tkFont.Font()
        count = 0
        for stat in stats:
            count += 1
            if count == 1:
                font2 = tkFont.Font(underline=True)
                text = Tkinter.Label(self.frame, text=stat[0], font=font2)
            else:
                text = Tkinter.Label(self.frame, text=stat[0], font=font1)
            text.grid(row=count, column=0, sticky='NWSE')
            value = Tkinter.Label(self.frame, text=stat[1], font=font1)
            value.grid(row=count, column=1, ipadx=30, sticky='NWSE')

        self.frame.place(relx=.55, rely=.02, relheight=1, relwidth=1)

        self.pack()

