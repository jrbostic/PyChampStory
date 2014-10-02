from Tkinter import *


class GameMap:
    def __init__(self, root, herometer):

        self.gamemap = Canvas(root)
        self.gamemap['bg'] = '#228b22'
        self.gamemap['bd'] = 0
        self.gamemap['relief'] = 'solid'

        self.herometer = herometer


    def updateMap(self, herox=0, heroy=0):

        height = self.gamemap.winfo_height()
        width = self.gamemap.winfo_width()

        self.gamemap.delete('all')
        widthslice = (width - 3) // 10  # 10x10 grid
        heightslice = (height - 3) // 10
        boardwidth = widthslice * 10 + 2  # for flush borders
        boardheight = heightslice * 10 + 1

        for x in xrange(2, width, widthslice):
            y = 0
            self.gamemap.create_line(x, y, x, boardheight, fill="black", width=2)

        for y in xrange(2, height, heightslice):
            x = 0
            self.gamemap.create_line(x, y, boardwidth, y, fill="black", width=2)

        hero_pos = self.herometer.get_hero_position()

        if herox == 0 and heroy == 0:
            herox = hero_pos['x'] * widthslice
            heroy = hero_pos['y'] * heightslice

        else:
            herox *= widthslice
            heroy *= heightslice

        self.gamemap.create_oval(herox + widthslice // 4, heroy + heightslice // 3, herox + widthslice // 4 + 20,
                                 heroy + heightslice // 3 + 20,
                                 fill="green", outline="black")

        count = 0
        for y in xrange(1, height - heightslice, heightslice):
            for x in xrange(1, width - widthslice, widthslice):
                count += 1
                self.gamemap.create_text(x + widthslice // 10 + 3, y + heightslice // 10 + 4, text=str(count),
                                         fill="blue")
