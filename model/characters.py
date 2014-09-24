from Tkinter import *
import ttk

class Robot:

	def __init__(self, parent, lx, ly):
		self.lx = lx
		self.ly = ly
		self.rx = lx+10
		self.ry = ly+10
		self.line = parent.create_oval(self.lx, self.ly, \
			self.rx, self.ry, fill="black")
