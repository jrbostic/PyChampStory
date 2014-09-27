from control.dialoger import *
from view.mainwindow import MainWindow
from os import listdir
from os.path import *

debug = computer_talk("DEBUG: Skip to game?", question=True, yesno=True, delay=0)
if debug:
    MainWindow('GOD')
    exit()

computer_talk(r"""
      ____                                             ____    
     / / /____ _____ _____ _____ _____ _____ _____ ____\ \ \   
    / / /_____|_____|_____|_____|_____|_____|_____|_____\ \ \  
   / / /|_____|_____|_____|_____|_____|_____|_____|_____|\ \ \ 
  /_/_/                                                   \_\_\
                                                               
   _ _   ____         ____ _                                _ _ 
  | | | |  _ \ _   _ / ___| |__   __ _ _ __ ___  _ __      | | |
  | | | | |_) | | | | |   | '_ \ / _` | '_ ` _ \| '_ \     | | |
  | | | |  __/| |_| | |___| | | | (_| | | | | | | |_) |    | | |
  | | | |_|    \__, |\____|_| |_|\__,_|_| |_| |_| .__/     | | |
  |_|_|        |___/                            |_|        |_|_|
  __ __        ____  _                      __             ____
 / / \ \      / ___|| |_ ___  _ __ _   _   / /____ _____  / / /
| |   | |     \___ \| __/ _ \| '__| | | | / /_____|_____|/ / / 
| |_ _| |      ___) | || (_) | |  | |_| | \ \_____|_____/ / /  
| (_|_) |     |____/ \__\___/|_|   \__, |  \_\         /_/_/   
 \_\ /_/                           |___/                       
    _    
   ( )   
    \|   
         
""", delay=.001)

computer_talk('\t\t\tLoading...', delay=.9)
computer_talk('\nHello!')
computer_talk('I am your computer.')
computer_talk('You can call me HAL...')

savedgame = computer_talk('You seem familiar... have we met before?', question=True, yesno=True)
if savedgame:
    computer_talk('NO SAVED GAMES (OR FUNCTIONALITY FOR THAT MATTER)')
else:
    computer_talk('Oh, it must just be your kind face.')

name = ''
verified = False
while not verified:
    name = computer_talk("What's your name?", question=True)
    verified = computer_talk("So, your name is " + name.title() \
                             + "?", question=True, yesno=True)
computer_talk("Nice to meet you, " + name.title() + "!")

tutor = computer_talk("Hey, would you like a brief tutorial on programming?", \
                      question=True, yesno=True)
if tutor:
    tutpath = "tutorials/"
    tutlist = [tutorial for tutorial in listdir(tutpath) \
               if isfile(join(tutpath, tutorial)) and \
               tutorial[-3:] == '.py' and tutorial[:-3] != '__init__']
    tutlist.sort()

    alldone = False  # valid option selected

    while not alldone:
        count = 0
        for tut in tutlist:
            count += 1
            print('\t' + str(count) + ". " + tut[:-3].title())
        print('')
        choice = computer_talk("Select a tutorial (0 to exit):", question=True)

        intchoice = -1  # holds the user entered value for list access
        badvalue = False

        try:
            intchoice = int(choice)
        except ValueError:
            intchoice = -1
            badvalue = True

        if intchoice == 0 and not badvalue:
            alldone = True  # exit tutorial
        elif 0 < intchoice <= len(tutlist):
            execfile(join(tutpath, tutlist[intchoice - 1]))
        else:
            computer_talk("Select either valid tutorial or exit.")

play = computer_talk("Would you like to play a GAME?", question=True, \
                     yesno=True)

if play == False:
    computer_talk("Fine, be that way...")
    exit()

computer_talk("Great!  This will be so much fun!")
computer_talk("Hold on while I try to find the GAME...")
computer_talk("..... ", delay=.75)
computer_talk("Darn!  Where is that GAME?!")
computer_talk("Hmmm... maybe you can help.")

validated = False
while not validated:
    computer_talk("TYPE THIS: Game():")
    command = str(raw_input('>>> ')).strip()
    if command == "Game()":
        validated = True
    elif command == "game()" or command == "game":
        computer_talk("Close, but you need an uppercase 'G'.  Try again.")
    elif command == "Game":
        computer_talk("Almost, but don't forget parentheses '()'.  Try again.")
    else:
        computer_talk("Try again...")

MainWindow(name)



