import tkMessageBox
import tkFont
import time

from validator import *
from control.herometer import Herometer
import gamemap
import statdisplay


class MainWindow():
    def __init__(self, name):
        """Conducts setup of the main window"""

        self.root = Tk()
        self.root.attributes("-zoomed", True)
        #self.root.resizable(0,0)
        self.root.title("PyChamp Story - The Adventures of " + name)
        self.root['bg'] = '#656565'

        self.herometer = Herometer(name)
        self.coupler = self.herometer.get_board_coupler()

        self._create_components()
        self._arrange_components()

        self._update_abilitybox()
        self.entrybox.entry.focus_set()
        self.dobutton['state'] = 'disabled'
        self.dobutton.bind('<Return>', self.do_action)

        self.timer = time.time()-.75

        self.update_gui()
        self.root.mainloop()

    def _create_components(self):
        """Creates the components (no placement)"""

        self.dobutton = Button(self.root, text="Do",
                               command=lambda: self.do_action(None))
        self.exitbutton = Button(self.root, text="Exit",
                                 command=self.exit_action, bg='red', fg='white')
        self.entrybox = InputField(self.root, self.herometer)
        self.gameboard = gamemap.GameMap(self.root, self.herometer, self)
        self.gameboard.gamemap.config(highlightbackground='#656565')
        self.profile = statdisplay.StatDisplay(self.root, self.herometer)  # placeholder

        self.var = StringVar()
        self.abilitybox = Label(self.root, textvariable=self.var, relief=GROOVE,
                                anchor=NW, justify=LEFT, padx=15, pady=15, fg='white', bg='black', bd='2')

        self.var2 = StringVar()
        self.outputbox = Label(self.root, textvariable=self.var2, relief=SUNKEN,
                               anchor=SW, justify=LEFT, wraplength=355, fg='white', bg='black', bd='2')


    def _arrange_components(self):
        """Arrange layout of components"""

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
        """Simple update for hero ability box"""

        abilitybox_text = ''
        for meth in self.herometer.get_available_methods():
            abilitybox_text += meth + "\n"
        self.var.set(abilitybox_text)

    def _update_outputbox(self, text):
        """Simple update for output box"""

        if text is None:
            text = ''
        if text != '':
            self.var2.set(self.var2.get() + '\n' + text)

    def do_action(self, event):
        """Executes do action of DO button"""

        entered_text = self.entrybox.entry.get()
        output_text = self.herometer.execute_method(entered_text)
        self._update_outputbox(output_text)
        self.entrybox.entry.delete(0, END)
        self.entrybox.entry.focus_set()


    def exit_action(self):
        """Facilitates program termination"""

        answer = tkMessageBox.askyesno('Really Quit?', 'Are you sure you want to quit?')
        if answer:
            exit()

    def update_gui(self):
        """Main event loop"""

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

        if time.time() - self.timer > 1:
            self._check_jobs()
            self.timer = time.time()

        self.root.after(60, self.update_gui)  # lower number for faster gui response

    def _check_jobs(self):
        """Interprets next job queue item and routes update"""

        job = self.coupler.get_a_job()
        if job is not None:

            for component in job.keys():

                if component == 'board':
                    hero = job['hero']
                    if hero is not None:
                        self.gameboard.updateMap(herox=hero.curr_tile['x'], heroy=hero.curr_tile['y'], tiles=job['board'])

                elif component == 'message':
                    self._update_outputbox(job[component])

                elif component == 'item_display':
                    self.profile.items_update()
            #       self.profile.place(bordermode=OUTSIDE, relx=.02, rely=.02,
            #                relheight=.20, relwidth=.26)
