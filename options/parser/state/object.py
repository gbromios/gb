from gb.options.parser.state.base import ParserState, ParserError, UnmatchedCharError
import gb.options.parser.state.value

from gb.options.parser.token import *

# TODO: may need some way to keep track of whether a given object has been terminating with commas or newlines?
# actually for now, just require commas.... bloobloobloo
class ReadObject(ParserState):
	data_type = dict

	def __init__(self, stream, top_level = False):
		super(ReadObject, self).__init__(stream)
		# are we looking for } or an eof? for now, probably doesn matter heh
		self.top_level = top_level

	def run(self):
		try:
			c = self.stream.peek()
		except IndexError:
			if self.top_level:
				return None
			else:
				raise

		if WHITESPACE(c) or KVP_END(c):
			# ignore whitespace... and commas for now...?
			self.stream.burn()
			return self

		elif not self.top_level and OBJECT_END(c):
			# done reading this object
			self.stream.burn()
			return None

		elif IDENTIFIER_START(c):
			# no burn
			return ReadKeyU(self.stream)

		elif Q(c):
			self.stream.burn()
			return ReadKeyU(self.stream)

		elif QQ(c):
			self.stream.burn()
			return ReadKeyU(self.stream)

		else:
			raise UnmatchedCharError(c, [WHITESPACE, OBJECT_END, IDENTIFIER_START, Q, QQ])

	def resume(self, data):
		# TODO hmm might just want to make this a list of kvp, let someone else
		# deal with duplicates?
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
	def _run(self, c):
		# we can only get here from IDENTIFIER_START, so we can just check IDENTIFIER
		if IDENTIFIER(c):
			self.data.key += self.stream.burn()
			return self

		elif WHITESPACE(c) or KVP_SEP(c):
			if self.data.key:
				return ReadKVPSep(self.stream)
			else:
				raise ParserError('invalid key: empty identifier!')

		else:
			raise UnmatchedCharError(c, [IDENTIFIER, WHITESPACE, KVP_SEP])


class ReadKeyQ(ReadKey):
	def _run(self, c):
		if IDENTIFIER(c):
			# if no key has been found yet, make sure initial char is valid
			if not self.data.key and not IDENTIFIER_START(c):
				raise ParserError('Identifier can only start [_a-zA-Z]')
			self.data.key += self.stream.burn()
			return self

		# key ends with a single quote
		elif Q(c):
			self.stream.burn()

		else:
			raise UnmatchedCharError(c, [Q, IDENTIFIER])


class ReadKeyQQ(ReadKey):
	def _run(self, c):
		if IDENTIFIER(c):
			# if no key has been found yet, make sure initial char is valid
			if not self.data.key and not IDENTIFIER_START(c):
				raise ParserError('Identifier can only start [_a-zA-Z]')
			self.data.key += self.stream.burn()
			return self

		# key ends with a single quote
		elif QQ(c):
			self.stream.burn()

		else:
			raise UnmatchedCharError(c, [QQ, IDENTIFIER])


class ReadKVPSep(ParserState):
	_data_set = False # unnecessary if value cant be None, but idk about that
	def _run(self, c):
		# if our data is set, we're looking for A) a comma or B) the end of our object
		if self._data_set:
			if WHITESPACE(c):
				self.stream.burn()
				return self

			elif KVP_END(c):
				self.stream.burn()
				return None

			elif OBJ_END(c):
				return None

			else:
				raise UnmatchedCharError(c, [WHITESPACE, KVP_END, OBJ_END])

		else:
			if WHITESPACE(c):
				self.stream.burn()
				return self

			elif KVP_SEP(c):
				self.stream.burn()
				return gb.options.parser.state.value.ReadValue(self.stream)

			else:
				raise UnmatchedCharError(c, [WHITESPACE, KVP_SEP])
