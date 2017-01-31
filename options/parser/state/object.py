from gb.options.parser.state.base import ParserState
from gb.options.parser.error import InvalidValueError, UnmatchedCharError, StreamEOF
import gb.options.parser.state.value

from gb.options.parser.token import *

# TODO: may need some way to keep track of whether a given object has been terminating with commas or newlines?
# actually for now, just require commas.... bloobloobloo
class ReadObject(ParserState):
	data_type = dict
	def run(self, stream):
		c = stream.last
		if WHITESPACE(c) or KVP_END(c):
			# ignore whitespace... and commas for now...?
			stream.pop()
			return self

		elif OBJECT_END(c):
			# done reading this object
			stream.pop()
			return None

		elif IDENTIFIER_START(c):
			# no pop
			return ReadKeyU()

		elif Q(c):
			stream.pop()
			return ReadKeyU()

		elif QQ(c):
			stream.pop()
			return ReadKeyU()

		else:
			raise UnmatchedCharError(c, [WHITESPACE, OBJECT_END, IDENTIFIER_START, Q, QQ])

	def resume(self, data):
		# TODO hmm might just want to make this a list of kvp, let someone else
		# deal with duplicates?
		self.data[data.key] = data.value
		return True

class ReadObjectTop(ReadObject):
	data_type = dict
	def run(self, stream):
		c = stream.last
		if WHITESPACE(c) or KVP_END(c):
			stream.pop()
			return self

		elif EOF(c):
			return None

		elif IDENTIFIER_START(c):
			return ReadKeyU()

		elif Q(c):
			stream.pop()
			return ReadKeyU()

		elif QQ(c):
			stream.pop()
			return ReadKeyU()

		else:
			raise UnmatchedCharError(c, [WHITESPACE, OBJECT_END, IDENTIFIER_START, Q, QQ])

	def resume(self, data):
		self.data[data.key] = data.value
		return True

class KVP(object):
	def __init__(self):
		self.key = ''
		self.value = None

class ReadKey(ParserState):
	data_type = KVP
	def resume(self, data):
		self.data.value = data
		return False

class ReadKeyU(ReadKey):
	def run(self, stream):
		c = stream.last
		# we can only get here from IDENTIFIER_START, so we can just check IDENTIFIER
		if IDENTIFIER(c):
			self.data.key += stream.pop()
			return self

		elif WHITESPACE(c) or KVP_SEP(c):
			if self.data.key:
				return ReadKVPSep()
			else:
				raise InvalidValueError('invalid key: empty identifier!')

		else:
			raise UnmatchedCharError(c, [IDENTIFIER, WHITESPACE, KVP_SEP])


class ReadKeyQ(ReadKey):
	def run(self, stream):
		c = stream.last
		if IDENTIFIER(c):
			# if no key has been found yet, make sure initial char is valid
			if not self.data.key and not IDENTIFIER_START(c):
				raise InvalidValueError('Identifier can only start [_a-zA-Z]')
			self.data.key += stream.pop()
			return self

		# key ends with a single quote
		elif Q(c):
			stream.pop()

		else:
			raise UnmatchedCharError(c, [Q, IDENTIFIER])


class ReadKeyQQ(ReadKey):
	def run(self, stream):
		c = stream.last
		if IDENTIFIER(c):
			# if no key has been found yet, make sure initial char is valid
			if not self.data.key and not IDENTIFIER_START(c):
				raise InvalidValueError('Identifier can only start [_a-zA-Z]')
			self.data.key += stream.pop()
			return self

		# key ends with a single quote
		elif QQ(c):
			stream.pop()

		else:
			raise UnmatchedCharError(c, [QQ, IDENTIFIER])


class ReadKVPSep(ParserState):
	_data_set = False # unnecessary if value cant be None, but idk about that
	def run(self, stream):
		c = stream.last
		# if our data is set, we're looking for A) a comma or B) the end of our object
		if self._data_set:
			if WHITESPACE(c):
				stream.pop()
				return self

			elif KVP_END(c):
				stream.pop()
				return None

			elif OBJ_END(c):
				return None

			else:
				raise UnmatchedCharError(c, [WHITESPACE, KVP_END, OBJ_END])

		else:
			if WHITESPACE(c):
				stream.pop()
				return self

			elif KVP_SEP(c):
				stream.pop()
				return gb.options.parser.state.value.ReadValue()

			else:
				raise UnmatchedCharError(c, [WHITESPACE, KVP_SEP])
