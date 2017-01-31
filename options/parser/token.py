import re

class Token(object):
	def __init__(self, pattern, comment):
		self.re = re.compile(pattern)
		self.comment = comment # TODO docstring?

	def __call__(self, char):
		if self.re.match(char):
			return True
		return False

class All(Token):
	def __init__(self):
		pass

	def __call__(self, char):
		return True

WHITESPACE = Token('\s', '"whitespace" space, tab, newline, etc. most stuff ignores this.')
NEWLINE = Token('\n', '"newline" i.e. "\\n et al"')
EOF = Token('\x03', 'EOF sent by stream reader')

SCALAR = Token('[^\[\]\{\},=]', '"scalar start" pretty much any non-whitespace character except {}[],=')

Q = Token('\'', 'a single quote')
QQ = Token('"', 'a double quote')
ESCAPE = Token('\\\\', '"escape char" i.e. "\\"')
#ESQ = Token('\\\'', 'escape char + Q')
#EDQ = Token('\\"', 'escape char + QQ')
OBJECT_START = Token('{', '"object start" i.e. "{"')
OBJECT_END = Token('}', '"object end" i.e. "}"')
KVP_SEP = Token('=', '"key-value-pair separator" i.e. "="')
KVP_END = Token(',', '"key-value-pair end" i.e. ","')

IDENTIFIER_START = Token('[_a-zA-Z]', '"identifier-start" valid python name starters i.e. "[_a-zA-Z]"')
IDENTIFIER = Token('[_a-zA-Z0-9]', '"identifier-character" valid postpositive characters for python names i.e. "[_a-zA-Z0-9]"')

LIST_START = Token('\[', '"list start" i.e. "["')
LIST_END = Token('\]', '"list end" i.e. "]"')
LIST_SEP = Token(',', '"list item separator" i.e. ","')

all = [
	'WHITESPACE',
	'NEWLINE',
	'SCALAR',
	'Q',
	'QQ',
	'ESCAPE',
	#'ESQ',
	#'EDQ',
	'OBJECT_START',
	'OBJECT_END',
	'KVP_SEP',
	'KVP_END',
	'IDENTIFIER_START',
	'IDENTIFIER',
	'LIST_START',
	'LIST_END',
	'LIST_SEP',
]
