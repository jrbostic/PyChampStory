from Tkinter import *
import tkMessageBox, tkFont, time
from validator import *
from control.herometer import Herometer
import gamemap
import threading


class MainWindow():
    def __init__(self, name):

        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.root.title("PyChamp Story - The Adventures of " + name)
        self.root['bg'] = '#228b22'

        self.herometer = Herometer(name)
        self.herometer.get_board_coupler().attach_listener(self.notify_observers)

        self._create_components()
        self._arrange_components()

        self._update_abilitybox()
        self.entrybox.entry.focus_set()
        self.dobutton['state'] = 'disabled'
        self.dobutton.bind('<Return>', self.do_action)

        self.update_gui()
        self.gameboard.updateMap()
        self.root.mainloop()

    def _create_components(self):

        self.dobutton = Button(self.root, text="Do",
                               command=lambda: self.do_action(None))
        self.exitbutton = Button(self.root, text="Exit",
                                 command=self.exit_action, bg='red', fg='white')
        self.entrybox = InputField(self.root, self.herometer)
        self.gameboard = gamemap.GameMap(self.root, self.herometer)
        self.profile = Canvas(self.root, bg='green')  # placeholder

        self.var = StringVar()
        self.abilitybox = Label(self.root, textvariable=self.var, relief=RAISED,
                                anchor=NW, justify=LEFT, padx=15, pady=15)

        self.var2 = StringVar()
        self.outputbox = Label(self.root, textvariable=self.var2, relief=SUNKEN,
                               anchor=SW, justify=LEFT, wraplength=355)


    def _arrange_components(self):

        self.dobutton.place(bordermode=OUTSIDE, relx=.60, rely=.88,
                            relheight=.1, relwidth=.26)
        self.exitbutton.place(bordermode=OUTSIDE, relx=.88, rely=.88,
                              relheight=.1, relwidth=.1)
        self.entrybox.entry.place(bordermode=OUTSIDE, relx=.02,
                                  rely=.88, relheight=.1, relwidth=.59)
        self.gameboard.gamemap.place(bordermode=OUTSIDE, relx=.3, rely=.02,
                                     relheight=.75, relwidth=.68)
        self.profile.place(bordermode=OUTSIDE, relx=.02, rely=.02,
                           relheight=.20, relwidth=.26)
        self.abilitybox.place(bordermode=OUTSIDE, relx=.02, rely=.25,
                              relheight=.40, relwidth=.26)
        self.outputbox.place(bordermode=OUTSIDE, relx=.02, rely=.68,
                              relheight=.17, relwidth=.26)

    def _update_abilitybox(self):

        abilitybox_text = ''
        for meth in self.herometer.get_available_methods():
            abilitybox_text += meth + "\n"
        self.var.set(abilitybox_text)

    def _update_outputbox(self, text):
        if text is None:
            text = ''
        if text != '':
            self.var2.set(self.var2.get() + '\n' + text)

    def do_action(self, event):
        entered_text = self.entrybox.entry.get()
        output_text = self.herometer.execute_method(entered_text)
        self._update_outputbox(output_text)
        self.entrybox.entry.delete(0, END)
        self.entrybox.entry.focus_set()


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

        font = tkFont.Font(family="Times", size=-(self.entrybox.entry.winfo_height()-15))
        self.entrybox.entry['font'] = font
        self.dobutton['font'] = font
        self.exitbutton['font'] = font

        font2 = tkFont.Font(family="Times", size=-(self.abilitybox.winfo_height() /
                                                   (len(self.herometer.get_available_methods())+4)))
        self.abilitybox['font'] = font2
        self._update_abilitybox()

        if self.gameboard.gamemap.winfo_width() > 9 < self.gameboard.gamemap.winfo_height():
            self.gameboard.updateMap()

        self.root.after(10, self.update_gui)  # lower number for faster gui response


    def notify_observers(self, type=None, data=None):
        """routes observable's notify messages"""

        if type=='mapupdate':
            self.gameboard.updateMap(herox=data[0], heroy=data[1])
            self.gameboard.gamemap.update_idletasks()
        elif type=='consoleupdate':
            self._update_outputbox(data)