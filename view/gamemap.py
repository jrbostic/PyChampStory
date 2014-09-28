from Tkinter import *


class GameMap:

    def __init__(self, root, herometer):

        self.gamemap = Canvas(root)
        self.herometer = herometer

        self.the_coupler = herometer.get_board_coupler()
        self.the_coupler.attach_listener(self._update_map)

    def _update_map(self, type=None, data=None):

        if type=='mapupdate':
            self.updateMap(herox=data[0], heroy=data[1])
            self.gamemap.update_idletasks()

    def updateMap(self, herox=0, heroy=0):

        #event is fired by observable board... can use this field upon adding observers

        height = self.gamemap.winfo_height()
        width = self.gamemap.winfo_width()

        self.gamemap.delete('all')
        widthslice = (width - 3) // 10  # 10x10 grid
        heightslice = (height - 3) // 10
        boardwidth = widthslice * 10 + 2  # for flush borders
        boardheight = heightslice * 10 + 1

        for x in xrange(1, width, widthslice):
            y = 0
            self.gamemap.create_line(x, y, x, boardheight, fill="blue")

        for y in xrange(1, height, heightslice):
            x = 0
            self.gamemap.create_line(x, y, boardwidth, y, fill="blue")

        hero_pos = self.herometer.get_hero_position()

        if herox == 0 and heroy == 0:
            herox = hero_pos['x']*widthslice
            heroy = hero_pos['y']*heightslice

        else:
            herox *= widthslice
            heroy *= heightslice

        self.gamemap.create_oval(herox+4, heroy+4, herox+widthslice//3, heroy+heightslice-3,
                                 fill="green", outline="light green")

        count = 0
        for y in xrange(1, height-heightslice, heightslice):
            for x in xrange(1, width-widthslice, widthslice):
                count += 1
                self.gamemap.create_text(x+widthslice//10+3, y+heightslice//10+2, text=str(count), fill="red")
