import string, re
from odict import ODict

KEY_CHARS = '_' + string.ascii_letters + string.digits
COMMENT_CHAR = '#'
KVP_SEPR = '='

# using any of the following characters as part of a literal value
# requires either single or double quotes:
#    []{},\s\t\n
#    space, tab, newline

# ending single/double quote can be backslash-escaped
# (TODO: strip out escaping-backslashes... heh)

def is_whitespace(c):
	return c in '\t\n, '

class Input(object):
	def __init__(self, data):
		# clean data
		data += '' if data.endswith('\0') else '\0'

		self.data = data
		self.index = 0

	def char(self, quoted=False):
		# burn un-quoted comments:
		if self.index == len(self.data):
			raise IndexError
		if not quoted and self.data[self.index] == COMMENT_CHAR:
			while True:
				self.index += 1
				# don't eat the null EOF if the comment fell there
				if self.data[self.index] == '\0':
					return

				elif self.data[self.index] == '\n':
					self.index += 1
					return '\n'

		else:
			c = self.data[self.index]
			self.index += 1
			return c

	def rollback(self):
		# roll back the index. for some reason i find this simpler
		# than looking ahead?
		self.index = max(0, self.index - 1)

	def burn_comment(self):
		# how can u burn a comment w/ no comment??
		# also, don't call this from within quoted stuff.
		assert(self.data[self.index] == COMMENT_CHAR)

class TDict(object):
	def __init__(self, i, body=False):
		self.data = ODict()

		while True:
			# escape or continue?
			while True:
				nc = i.char()
				if is_whitespace(nc):
					#print('waspay', nc)
					continue # look for non-whitespace
				elif nc == ('}' if not body else '\0'):
					#print('bai', nc)
					return
				else:
					###print('kay', nc)
					i.rollback()
					break
			#print("wat")

			# key
			k = TKey(i).data
			#print(k)
			if k in self.data:
				raise TypeError('{0} already present: keys must be unqiue!')

			# eat the '=' sign
			while True:
				nc = i.char()
				if is_whitespace(nc):
					continue
				elif nc == KVP_SEPR:
					break
				else:
					raise ValueError('expected "=" KVP separator')

			self.data[k] = TValue(i).data
			#print (self.data)

class TKey(object):
	def __init__(self, i):
		self.data = ''

		while True:
			nc = i.char()
			if not self.data: # no key characters yet found
				if is_whitespace(nc):
					continue # look for non-whitespace

				elif nc in '_0123456789':
					raise ValueError('key cannot start with _ or 0-9')

				elif nc in string.ascii_letters:
					self.data += nc

				else:
					raise ValueError('invalid key character "{0}"'.format(nc))

			else: # after the beginning of the key has been found
				if is_whitespace(nc):
					return # whitesepace signals the end of a key

				elif nc == KVP_SEPR: # if we got a no-space-equals, roll input back one
					i.rollback()
					return

				elif nc in KEY_CHARS:
					self.data += nc

				else:
					raise ValueError('invalid key character "{0}"'.format(nc))


class TList(object):
	def __init__(self, i):
		self.data = []
		while True:
			# escape or continue?
			while True:
				nc = i.char()
				if is_whitespace(nc):
					continue # look for non-whitespace
				elif nc == ']':
					return
				else:
					i.rollback()
					self.data.append(TValue(i).data)


class TLiteralSingle(object):
	def __init__(self, i):
		self.data = ''
		while True:
			nc = i.char(quoted=True)
			if nc == '\'':
				if re.search(".*[^\\\\](\\\\\\\\)*$", self.data):
					return
				else:
					if self.data.endswith('\\'):
						self.data = self.data[:-1] + nc
			elif nc == '\0':
				i.rollback()
				return
			else:
				self.data += nc


class TLiteralDouble(object):
	def __init__(self, i):
		self.data = ''
		while True:
			nc = i.char(quoted=True)
			if nc == '"':
				if re.search(".*[^\\\\](\\\\\\\\)*$", self.data):
					return
				else:
					if self.data.endswith('\\'):
						self.data = self.data[:-1] + nc
			elif nc == "\0":
				i.rollback()
				return
			else:
				self.data += nc


class TLiteralBare(object):
	def __init__(self, i):
		self.data = ''
		while True:
			nc = i.char()
			# have to be a bit picky about separators in bare literals!
			if nc in '\0]}':
				i.rollback()
				return

			elif is_whitespace(nc):
				return

			else:
				self.data += nc


class TValue(object):
	def __init__(self, i):
		while True:
			nc = i.char()
			if is_whitespace(nc):
				continue

			else:
				if nc == '{': # goes to }
					cls = TDict

				elif nc == '[': # goes to ]
					cls = TList

				elif nc == '"': # goes to unescaped "
					cls = TLiteralDouble

				elif nc == '\'': # goes to unescaped '
					cls = TLiteralSingle

				else: # goes to whitespace!
					cls = TLiteralBare
					i.rollback()

				self.data = cls(i).data
				#print('bare',self.data)
				break


def parse(raw_data):
	return TDict(Input(raw_data), body=True).data
