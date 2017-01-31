from gb.options.parser.state.base import ParserState

from gb.options.parser.error import *
from gb.options.parser.token import *

import re

FLOAT_RE = re.compile('^[\\d]*\\.[\\d]+$')
INT_RE   = re.compile('^[\\d]+$')

class ReadScalar(ParserState):
	# only reads first char, then delegates
	def run(self, stream):
		c = stream.last
		# will never be whitespace afaict?
		# single quote, double quote, or OTHER

		if Q(c):
			stream.pop()
			return ReadScalarQ()

		elif QQ(c):
			stream.pop()
			return ReadScalarQQ()

		else:
			return ReadScalarUQ()

class ReadScalarQ(ParserState):
	data_type = str
	def run(self, stream):
		c = stream.last
		if NEWLINE(c):
			# mostly because it theoretically makes parsing comments hard
			raise IllegalNewline

		elif EOF(c):
			raise IllegalEOF

		elif Q(c):
			stream.pop()
			return None

		elif ESCAPE(c):
			# for now, just accept the next char, no matter what it is.
			stream.pop()
			self.data += stream.pop()
			return self

		else:
			self.data += stream.pop()
			return self

	def resume(self, data):
		raise StateTransitionError('scalars should never start other states!')

class ReadScalarQQ(ParserState):
	data_type = str
	def run(self, stream):
		c = stream.last
		if NEWLINE(c):
			raise IllegalNewline

		elif EOF(c):
			raise IllegalEOF

		elif QQ(c):
			stream.pop()
			return None

		elif ESCAPE(c):
			stream.pop()
			self.data += stream.pop()
			return self

		else:
			self.data += stream.pop()
			return self


	def resume(self, data):
		raise StateTransitionError('scalars should never start other states!')

class ReadScalarUQ(ParserState):
	data_type = str
	def run(self, stream):
		c = stream.last

		if EOF(c):
			self.parse_type()
			return None

		if ESCAPE(c):
			# for now, just accept the next char, no matter what it is.
			stream.pop()
			self.data += stream.pop()

		# unescaped whitespace or comma will end an unquoted scalar
		elif WHITESPACE(c):
			self.parse_type()
			return None

		# p much anything else if fair game
		elif SCALAR(c):
			self.data += stream.pop()
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
		raise StateTransitionError('scalars should never start other states!')

