import gb.options.parser.stream
from gb.state import StateMachine
from gb.options.parser.state.format import FindFormat

def find_format(raw_data):
	stream = gb.options.parser.stream.Stream(raw_data)
	return StateMachine(FindFormat()).run(stream)

def parse(raw_data, InitState = None):
	stream = gb.options.parser.stream.Stream(raw_data)

	InitState = InitState if InitState else find_format(raw_data)

	if InitState is not None:
		return StateMachine(InitState()).run(stream)
	else:
		raise Exception("couldn't figure out the format of this file")

