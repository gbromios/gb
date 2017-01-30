import gb.state
import gb.options.parser.stream
import gb.options.parser.state.init

def parse(raw_data):
	stream = gb.options.parser.stream.Stream(raw_data)
	init = gb.options.parser.state.init.Init(stream)
	machine = gb.state.StateMachine(init)

	machine.run()

	return machine.final_state.data
