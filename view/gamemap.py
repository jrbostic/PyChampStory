from Tkinter import *


class GameMap:
    """Handles game board view (probably should inherit from Canvas"""

    def __init__(self, root, herometer):
        """Sets up canvas and herometer reference"""

        self.gamemap = Canvas(root)
        self.gamemap['bg'] = "black" #'#228b22'
        self.gamemap['bd'] = 0
        self.gamemap['relief'] = 'solid'

        self.herometer = herometer


    def updateMap(self, herox=0, heroy=0, tiles=None):
        """Updates the game map for view"""

        height = self.gamemap.winfo_height()
        width = self.gamemap.winfo_width()

        self.gamemap.delete('all')
        widthslice = (width - 3) // 10  # 10x10 grid
        heightslice = (height - 3) // 10
        boardwidth = widthslice * 10 + 2  # for flush borders
        boardheight = heightslice * 10 + 1

        if tiles is not None:
            self._render_tiles(tiles, widthslice, heightslice)

        for x in xrange(2, width, widthslice):
            y = 0
            self.gamemap.create_line(x, y, x, boardheight, fill="black", width=2)

        for y in xrange(2, height, heightslice):
            x = 0
            self.gamemap.create_line(x, y, boardwidth, y, fill="black", width=2)

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
                                         fill="white")

    def _render_tiles(self, tiles, wslice, hslice):
        """Handles rendering of each tile on the board based on state"""

        for row in tiles:
            for atile in row:
                if atile.visited is True:
                    basex = wslice*atile.x
                    basey = hslice*atile.y
                    self.gamemap.create_rectangle(basex, basey, basex+wslice, basey+hslice, fill=atile.bg)

