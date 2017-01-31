from gb.options.parser.state.base import ParserState

import gb.options.parser.state.object
import gb.options.parser.state.scalar
import gb.options.parser.state.list

from gb.options.parser.token import *

class ReadValue(ParserState):
	def run(self, stream):
		c = stream.last
		if WHITESPACE(c):
			stream.pop()
			return self

		elif OBJECT_START(c):
			stream.pop()
			return gb.options.parser.state.object.ReadObject()

		elif LIST_START(c):
			stream.pop()
			return gb.options.parser.state.list.ReadList()

		elif SCALAR(c): # anything but syntax tbh
			return gb.options.parser.state.scalar.ReadScalar()

		else:
			raise UnmatchedCharError(c, [WHITESPACE, OBJECT_START, LIST_START, SCALAR])
