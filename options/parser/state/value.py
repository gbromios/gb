from gb.options.parser.state.base import ParserState, ParserError, UnmatchedCharError
import gb.options.parser.state.object
import gb.options.parser.state.scalar
import gb.options.parser.state.list

from gb.options.parser.token import *

class ReadValue(ParserState):
	def _run(self, c):
		if WHITESPACE(c):
			self.stream.burn()
			return self

		elif OBJECT_START(c):
			self.stream.burn()
			return gb.options.parser.state.object.ReadObject(self.stream)

		elif LIST_START(c):
			self.stream.burn()
			return gb.options.parser.state.list.ReadList(self.stream)

		elif SCALAR(c): # anything but syntax tbh
			return gb.options.parser.state.scalar.ReadScalar(self.stream)

		else:
			raise UnmatchedCharError(c, [WHITESPACE, OBJECT_START, LIST_START, SCALAR])
