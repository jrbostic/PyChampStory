from Tkinter import *
import re

class InputField():

	def __init__(self, root):
		vcmd = (root.register(self.OnValidate), \
			'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
		self.entry = Entry(root, validate="key", \
			validatecommand=vcmd)
		self.is_executable = False
		
	def OnValidate(self, d, i, P, s, S, v, V, W):
		
		print "DEBUG OUTPUT:"
		print "d='%s'" % d
		print "i='%s'" % i
		print "P='%s'" % P
		print "s='%s'" % s
		print "S='%s'" % S
		print "v='%s'" % v
		print "V='%s'" % V
		print "W='%s'" % W

		testval = re.compile(r'^walk\([0-9]+\)$')
		
		testval2 = False
		string = 'walk('
		string2 = ''
		for char in string:
			string2 = string[0:len(string2)+1]
			testval2 = testval2 or string2==P
		testval3 = re.compile(r'^walk\([0-9]+$')
		
		self.is_executable = False

		if testval.match(P):
			self.entry.config(fg='#5700FF')
			self.is_executable = True
		elif testval2 or testval3.search(P):
		    self.entry.config(fg='#038357')
		else:
			self.entry.config(fg='#FF0000')
			
		return True

