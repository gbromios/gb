from gb.options.parser.state.base import ParserState

import gb.options.parser.state.object

class Init(ParserState):
	def __init__(self, stream, input_type = dict):
		super(Init, self).__init__(stream)
		self.input_type = input_type

	def run(self):
		if self.input_type is dict:
			return gb.options.parser.state.object.ReadObject(self.stream, top_level = True)

		else:
			return None
