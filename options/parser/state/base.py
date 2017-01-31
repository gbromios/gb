import gb.state

class ParserState(gb.state.State):
	def __init__(self):
		super(ParserState, self).__init__()

	def resume(self, data):
		'''default is to blindly pass the data up. be careful..'''
		self.data = data
		return False
