import gb.options.parser.stream
from gb.state import StateMachine
from gb.options.parser.state.format import FindFormat

def find_format(raw_data):
	stream = gb.options.parser.stream.Stream(raw_data)
	return StateMachine(FindFormat()).run(stream)

def parse(raw_data, InitState = None):
	# strip out the comments... do it the lazy way for now
	raw_data = '\n'.join(l for l in raw_data.split('\n') if not l.strip().startswith('#'))

	stream = gb.options.parser.stream.Stream(raw_data)

	InitState = InitState if InitState else find_format(raw_data)

	if InitState is not None:
		return StateMachine(InitState()).run(stream)
	else:
		raise Exception("couldn't figure out the format of this file")

