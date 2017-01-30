class Stream(object):
	def __init__(self, raw_data):
		self.raw_data = raw_data
		self.i = 0

	def peek(self, offset = 0):
		o = self.i + offset
		if o >= len(self.raw_data):
			raise IndexError("cannot peak past end of data!")

		return self.raw_data[o]

	def burn(self):
		if self.i >= len(self.raw_data):
			raise IndexError("end of stream reached!")
		c = self.raw_data[self.i]
		self.i += 1
		return c

	@property
	def index(self):
		return self.i
