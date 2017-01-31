from gb.options.parser.state.base import ParserState, ParserError, UnmatchedCharError

from gb.options.parser.token import *

import re

FLOAT_RE = re.compile('^[\\d]*\\.[\\d]+$')
INT_RE   = re.compile('^[\\d]+$')

class ReadScalar(ParserState):
	# only reads first char, then delegates
	def run(self):
		c = self.stream.last
		# will never be whitespace afaict?
		# single quote, double quote, or OTHER

		if Q(c):
			self.stream.pop()
			return ReadScalarQ(self.stream)

		elif QQ(c):
			self.stream.pop()
			return ReadScalarQQ(self.stream)

		else:
			return ReadScalarUQ(self.stream)

class ReadScalarQ(ParserState):
	data_type = str
	def run(self):
		c = self.stream.last
		if Q(c):
			self.stream.pop()
			return None

		elif ESCAPE(c):
			# for now, just accept the next char, no matter what it is.
			self.stream.pop()
			self.data += self.stream.pop()
			return self

		else:
			self.data += self.stream.pop()
			return self

	def resume(self, data):
		raise ParserError('scalars should never start other states!')

class ReadScalarQQ(ParserState):
	data_type = str
	def run(self):
		c = self.stream.last
		if QQ(c):
			self.stream.pop()
			return None

		elif ESCAPE(c):
			self.stream.pop()
			self.data += self.stream.pop()
			return self

		else:
			self.data += self.stream.pop()
			return self


	def resume(self, data):
		raise ParserError('scalars should never start other states!')

class ReadScalarUQ(ParserState):
	data_type = str
	def run(self):
		c = self.stream.last
		if ESCAPE(c):
			# for now, just accept the next char, no matter what it is.
			self.stream.pop()
			self.data += self.stream.pop()

		# unescaped whitespace or comma will end an unquoted scalar
		elif WHITESPACE(c):
			self.parse_type()
			return None

		# p much anything else if fair game
		elif SCALAR(c):
			self.data += self.stream.pop()
			return self

		else:
			# could result in a hard to diagnose syntax error, but thems the breaks
			self.parse_type()
			return None

	def parse_type(self):
		# unquoted scalars can be ints or floats or strings or null!
		data = self.data
		if data == 'null' or data == 'None':
			self.data = None

		elif FLOAT_RE.match(data):
			self.data = float(data)

		elif INT_RE.match(data):
			self.data = int(data)


	def resume(self, data):
		raise ParserError('scalars should never start other states!')

