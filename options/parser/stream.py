class Stream(object):
	def __init__(self, raw_data):
		self.raw_data = raw_data
		self.i = 0

	@property
	def last(self):
		if self.i >= len(self.raw_data):
			raise IndexError("end of stream reached!")
		return self.raw_data[self.i]

	def pop(self):
		c = self.last
		self.i += 1
		return c

	@property
	def index(self):
		return self.i
