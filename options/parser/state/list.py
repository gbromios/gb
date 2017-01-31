from gb.options.parser.state.base import ParserState

import gb.options.parser.state.value

from gb.options.parser.token import *

class ReadList(ParserState):
	data_type = list
	def run(self, stream):
		c = stream.last
		if WHITESPACE(c) or LIST_SEP(c):
			stream.pop()
			return self

		elif LIST_END(c):
			stream.pop()
			self.data = tuple(self.data)
			return None

		else:
			return gb.options.parser.state.value.ReadValue()

	def resume(self, data):
		self.data.append(data)
		return True

class ReadListTop(ParserState):
	data_type = list
	def run(self, stream):
		c = stream.last
		if WHITESPACE(c) or LIST_SEP(c):
			stream.pop()
			return self

		elif EOF(c):
			self.data = tuple(self.data)
			return None

		else:
			return gb.options.parser.state.value.ReadValue()

	def resume(self, data):
		self.data.append(data)
		return True


