class StateMachine(object):
	def __init__(self, initial_state):
		self.states = [initial_state]
		self.final_state = None # set this when finished.
		self.started = False

	@property
	def current_state(self):
		if self.states:
			return self.states[-1]
		else:
			return None

	@current_state.setter
	def current_state(self, state):
		self.states.append(state)

	def pop_state(self):
		if self.states:
			return self.states.pop(-1)
		else:
			raise IndexError("no states to pop!")

	def run(self):
		# could make this async with minimal work
		self.started = True
		x = 0
		while True:
			x += 1
			next_state = self.current_state.run()

			if next_state is None:
				# return to the prior state
				last_state = self.pop_state()
				while True:
					if self.current_state is None:
						# out of states, we did it
						self.final_state = last_state
						return

					else:
						# resume == True, continue running states as normal
						if self.current_state.resume(last_state.data):
							break
						# resume == False, pop this state and resume the last one
						else:
							last_state = self.pop_state()

			elif next_state is self.current_state:
				pass

			elif isinstance(next_state, State):
				self.current_state = next_state


class State(object):
	# set per class if you want self.data to start out with an empty object
	data_type = None
	def __init__(self):
		if self.data_type is not None:
			self.data = self.data_type()
		else:
			self.data = None

	def run(self):
		raise NotImplemented

		# do some stuff, then return one of the following:
		if "all done with this state":
			return None

		elif "keep going on this state":
			return self

		elif "move to a new state":
			return State()

	def resume(self, data):
		# get the data that has been returned to us and do whatever we need to do.
		# return False == do nothing but pass my data to the next guy
		# return True  == resume running states as normal.
		return False
