from gb.options.parser.error import StreamEOF

class Stream(object):
	def __init__(self, raw_data):
		self._raw_data = raw_data
		self.i = 0

	@property
	def last(self):
		if self.i >= len(self._raw_data):
			return '\x03' # EOF

		return self._raw_data[self.i]

	def pop(self):
		if self.i >= len(self._raw_data):
			raise StreamEOF

		c = self.last
		self.i += 1
		return c

	def reset(self):
		self.i = 0

	@property
	def index(self):
		return self.i
