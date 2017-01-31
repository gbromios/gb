from gb.options.parser.state.base import ParserState, ParserError, UnmatchedCharError
import gb.options.parser.state.value

from gb.options.parser.token import *

class ReadList(ParserState):
	data_type = list
	def _run(self, c):
		if WHITESPACE(c) or LIST_SEP(c):
			self.stream.pop()
			return self

		elif LIST_END(c):
			self.stream.pop()
			self.data = tuple(self.data)
			return None

		else:
			return gb.options.parser.state.value.ReadValue(self.stream)

	def resume(self, data):
		self.data.append(data)
		return True
