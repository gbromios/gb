class ParserError(Exception):
	'''raise when u cant parse huehue'''

class StreamEOF(ParserError):
	'''raised when the stream hits its end'''

class InvalidValueError(ParserError):
	'''token matched, but the value was no good'''

class StateTransitionError(ParserError):
	'''tried to move to an invalid state'''

class UnmatchedCharError(ParserError):
	def __init__(self, char, expected):
		message = 'character "{0} matches no valid tokens.'.format(char)
		if expected:
			message += ' expected: {0}'.format(expected)
		super(UnmatchedCharError, self).__init__(message)
