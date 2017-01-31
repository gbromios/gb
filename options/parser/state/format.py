from gb.options.parser.state.base import ParserState
from gb.options.parser.token import *
import gb.options.parser.state.object
import gb.options.parser.state.list
import gb.options.parser.state.value


class FindFormat(ParserState):
	def run(self, stream):
		c = stream.last
		if EOF(c):
			self.data = EmptyFile
			return None # empty string basically

		if WHITESPACE(c):
			stream.pop()
			return self

		# hitting { or [ tells us right away, orthodox object/list
		if OBJECT_START(c) or LIST_START(c):
			self.data = gb.options.parser.state.value.ReadValue
			return None

		# must be a identifer, list item, or lone scalar but we wont know until
		# we can look at the second item
		if Q(c):
			stream.pop()
			return FmtQuoted(Q)

		if QQ(c):
			stream.pop()
			return FmtQuoted(QQ)

		if SCALAR(c):
			return FmtUnquoted()

		else:
			return None # error

class FmtQuoted(ParserState):
	def __init__(self, quote_char):
		super(FmtQuoted, self).__init__()
		self.quote_char = quote_char

	def run(self, stream):
		c = stream.last
		if EOF(c):
			return None # empty string basically

		elif ESCAPE(c):
			stream.pop()
			stream.pop()
			return self

		elif self.quote_char(c):
			stream.pop()
			return FmtSecondItem()

		# could make second item know that this cannot be a KVP but overkill atm
		# so just accept any char
		else:
			stream.pop()
			return self

class FmtUnquoted(ParserState):
	def run(self, stream):
		c = stream.last
		if EOF(c) or WHITESPACE(c):
			# could just be None, but let SecondItem handle it
			return FmtSecondItem()

		elif ESCAPE(c):
			stream.pop()
			stream.pop()
			return self

		elif SCALAR(c):
			stream.pop()
			return self

		elif LIST_SEP(c):
			self.data = gb.options.parser.state.list.ReadListTop
			return None

		elif KVP_SEP(c):
			self.data = gb.options.parser.state.object.ReadObjectTop
			return None

		else:
			return None # error

class FmtSecondItem(ParserState):
	def run(self, stream):
		c = stream.last

		if EOF(c):
			self.data = LoneScalar
			return None

		elif WHITESPACE(c):
			stream.pop()
			return self

		elif OBJECT_END(c) or LIST_END(c):
			# these mean a broken file
			return None

		elif KVP_SEP(c):
			# technically possible to get here w/out a strictly valid identifer.
			# not too worried because parsing will fail even if we try
			self.data = gb.options.parser.state.object.ReadObjectTop
			return None

		else:
			# anything else should be the start of a list item, though if there's
			# flaws w/ this class its probably because of that assumption
			self.data = gb.options.parser.state.list.ReadListTop
			return None

# hue...
class EmptyFile(ParserState):
	def run(self, stream):
		#self.data = {} ???? i think i prefer this. but none works too.
		return None # i.e. a state that ends with data = None

class LoneScalar(ParserState):
	def run(self, stream):
		self.data = stream._raw_data.strip()
		if self.data[0] in "'\"":
			self.data = self.data[1:-1]
		return None
