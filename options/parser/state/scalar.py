from gb.options.parser.state.base import ParserState, ParserError, UnmatchedCharError

from gb.options.parser.token import *

class ReadScalar(ParserState):
	# only reads first char, then delegates
	def _run(self, c):
		# will never be whitespace afaict?
		# single quote, double quote, or OTHER

		if Q(c):
			self.stream.burn()
			return ReadScalarQ(self.stream)

		elif QQ(c):
			self.stream.burn()
			return ReadScalarQQ(self.stream)

		else:
			return ReadScalarUQ(self.stream)

class ReadScalarQ(ParserState):
	data_type = str
	def _run(self, c):
		if Q(c):
			self.stream.burn()
			return None

		elif ESCAPE(c):
			# for now, just accept the next char, no matter what it is.
			self.stream.burn()
			self.data += self.stream.burn()
			return self

		else:
			self.data += self.stream.burn()
			return self

	def resume(self, data):
		raise ParserError('scalars should never start other states!')

class ReadScalarQQ(ParserState):
	data_type = str
	def _run(self, c):
		if QQ(c):
			self.stream.burn()
			return None

		elif ESCAPE(c):
			self.stream.burn()
			self.data += self.stream.burn()
			return self

		else:
			self.data += self.stream.burn()
			return self


	def resume(self, data):
		raise ParserError('scalars should never start other states!')

class ReadScalarUQ(ParserState):
	data_type = str
	def _run(self, c):
		if ESCAPE(c):
			# for now, just accept the next char, no matter what it is.
			self.stream.burn()
			self.data += self.stream.burn()

		# unescaped whitespace or comma will end an unquoted scalar
		elif WHITESPACE(c):
			print 'end scalar_u'
			return None

		# p much anything else if fair game
		elif SCALAR(c):
			self.data += self.stream.burn()
			return self

		else:
			# could result in a hard to diagnose syntax error, but thems the breaks
			return None

	def resume(self, data):
		raise ParserError('scalars should never start other states!')

