from gb.options import Options, Optionable
from gb.options.test import relations_path
import os

class Able(Optionable):
	pass

class Risible(Able):
	pass

class Sinkable(Able):
	pass

a = Able()
b = Able()

q = Risible()
r = Risible()

s = Sinkable()
t = Sinkable()

o = Options.from_path(relations_path)

o._dump()

Optionable.register_options_global(o.register_globally)
# after a global registration, every optional has the stuff


