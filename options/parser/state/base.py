import gb.state

class ParserState(gb.state.State):
	def __init__(self, stream):
		super(ParserState, self).__init__()
		self.stream = stream

	# TODO have grand plans to make this whole thing as data driven as possible
	# but right now hard coding what I need is probably more sane... there's still
	# some easy wins here... maybe.

	def _run(self, c):
		raise NotImplemented

	def run(self):
		# pretty much every parser state wants to know what the next char is
		# if we hit eof: just end like crazy? probably parse will fail but whatever
		try:
			c = self.stream.last
		except IndexError:
			return None

		return self._run(c)

	def resume(self, data):
		'''default is to blindly pass the data up. be careful..'''
		self.data = data
		return False

class ParserError(Exception):
	'''raise when u cant parse huehue'''

class UnmatchedCharError(ParserError):
	def __init__(self, char, expected):
		message = 'character "{0} matches no valid tokens.'.format(char)
		if expected:
			message += ' expected: {0}'.format(expected)
		super(UnmatchedCharError, self).__init__(message)
