import Tkinter
import tkFont

__author__ = 'jessebostic'

class StatDisplay(Tkinter.Canvas):

    def __init__(self, root, herometer):
        Tkinter.Canvas.__init__(self, root)
        self.herometer = herometer
        self.frame = Tkinter.Frame(self)

        bag_display_frame1 = Tkinter.Frame(self)
        bag_display_frame2 = Tkinter.Frame(bag_display_frame1)
        scrollbar = Tkinter.Scrollbar(bag_display_frame2, orient=Tkinter.VERTICAL)
        self.bag_display = Tkinter.Listbox(bag_display_frame1, yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.bag_display.yview)

        self.frame.place(relx=.55, rely=.02, relheight=1, relwidth=1)
        bag_display_frame1.place(relx=.02, rely=.05, relheight=.9, relwidth=.5)
        bag_display_frame2.pack(side=Tkinter.RIGHT, fill=Tkinter.BOTH, expand=1)
        self.bag_display.pack(fill=Tkinter.X, expand=1)
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.BOTH, expand=1)

        self.pack()
        self.stats_update()

    def stats_update(self):

        self.delete('all')

        font1 = tkFont.Font()
        count = 0
        for stat in self.herometer.get_stats():
            count += 1
            if count == 1:
                font2 = tkFont.Font(underline=True)
                text = Tkinter.Label(self.frame, text=stat[0], font=font2)
            else:
                text = Tkinter.Label(self.frame, text=stat[0], font=font1)
            text.grid(row=count, column=0, sticky='NWSE')
            value = Tkinter.Label(self.frame, text=stat[1], font=font1)
            value.grid(row=count, column=1, ipadx=30, sticky='NWSE')


    def items_update(self):
        self.bag_display.delete(0, Tkinter.END)
        for item in self.herometer.hero.bag:
            self.bag_display.insert(0, item.name)