from Tkinter import *

class GameMap:

	def __init__(self, root):
	
		self.gamemap = Canvas(root)
	
	def updateMap(self, height, width):

		self.gamemap.delete('all')
		widthslice = (width-3)//10  #10x10 grid
		heightslice = (height-3)//10
		boardwidth = widthslice*10+2  # for flush borders
		boardheight = heightslice*10+1

		for x in xrange(1, width, widthslice):
			y = 0
			self.gamemap.create_line(x, y, x, boardheight, fill="blue")

		for y in xrange(1, height, heightslice):
			x = 0
			self.gamemap.create_line(x, y, boardwidth, y, fill="blue")
