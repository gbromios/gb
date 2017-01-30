from gb.state import State, StateMachine

import random

LETTERS = 'ABCD'

class Foo(State):
	'assemble a small string of ABDs'
	data_type = str
	def run(self):
		if len(self.data) < 10:
			print 'Foo -- get new letters from Bar'
			return Bar()

		else:
			print 'Foo -- done running'
			return None

	def resume(self, data):
		print 'Foo -- resume: "{0}" + "{1}"'.format(self.data, data)
		self.data += data

class Bar(State):
	'return 1-3 A, B or D characters, but never C!'
	def run(self):
		l = random.choice(LETTERS)

		if l == 'C':
			print 'Bar -- got C, try again...'
			return self

		else:
			self.data = l * random.randint(1,3)
			print 'Bar -- finishing with "{0}"'.format(self.data)
			return None

def test():
	machine = StateMachine(Foo())
	machine.run()
	print 'State Machine Finished with "{0}"'.format(machine.final_state.data)

if __name__ == '__main__':
	test()
