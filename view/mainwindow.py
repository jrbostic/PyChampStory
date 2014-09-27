from Tkinter import *
import tkMessageBox, tkFont, time
from validator import *
from control.herometer import Herometer
import gamemap


class MainWindow():

    def __init__(self, name):

        self.root = Tk()
        self.root.attributes("-zoomed", True)
        self.root.title("PyChamp Story - The Adventures of " + name)

        self.hero = Hero(name)
        self.herometer = Herometer(self.hero)

        # create components
        self.dobutton = Button(self.root, text="Do", \
                               command=lambda: self.do_action(None))
        self.dobutton['state'] = 'disabled'
        self.exitbutton = Button(self.root, text="Exit", \
                                 command=self.exit_action, bg='red', fg='white')
        self.entrybox = InputField(self.root, self.herometer)
        self.gameboard = gamemap.GameMap(self.root)
        self.profile = Canvas(self.root, bg='green')  #placeholder

        #arrange components
        self.dobutton.place(bordermode=OUTSIDE, relx=.60, rely=.88, \
                            relheight=.1, relwidth=.26)
        self.exitbutton.place(bordermode=OUTSIDE, relx=.88, rely=.88, \
                              relheight=.1, relwidth=.1)
        self.entrybox.entry.place(bordermode=OUTSIDE, relx=.02, \
                                  rely=.88, relheight=.1, relwidth=.59)
        self.gameboard.gamemap.place(bordermode=OUTSIDE, relx=.3, rely=.05, \
                                     relheight=.75, relwidth=.68)
        self.profile.place(bordermode=OUTSIDE, relx=.02, rely=.02, \
                           relheight=.20, relwidth=.26)

        self.entrybox.entry.focus_set()
        self.dobutton.bind('<Return>', self.do_action)

        self.update_gui()
        self.root.mainloop()

    def do_action(self, event):

        tkMessageBox.showinfo("Do Button Action", "This is the where execution happens.")

    def exit_action(self):

        answer = tkMessageBox.askyesno('Really Quit?', 'Are you sure you want to quit?')
        if answer:
            exit()

    def update_gui(self):

        if self.entrybox.is_executable and self.dobutton['state'] == 'disabled':
            self.dobutton['state'] = 'active'
            self.dobutton.focus_set()
        elif not self.entrybox.is_executable:
            self.dobutton['state'] = 'disabled'

        font = tkFont.Font(family="Times", size=-self.entrybox.entry.winfo_height() + 15)
        self.entrybox.entry['font'] = font
        self.dobutton['font'] = font
        self.exitbutton['font'] = font

        if self.gameboard.gamemap.winfo_width() > 9 < self.gameboard.gamemap.winfo_height():
            self.gameboard.updateMap(self.gameboard.gamemap.winfo_height(), \
                                     self.gameboard.gamemap.winfo_width())

        self.root.after(1, self.update_gui)
