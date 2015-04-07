import parser
import os.path

class Options(object):
	_config_dir = None

	def __init__(self, data):
		self._options = data

	@classmethod
	def from_env(cls, env):
		if cls._config_dir is None:
			raise ValueError('config dir not set, no idea where to look :(')
		if not os.path.isdir(cls._config_dir):
			raise ValueError('config dir is set to a non-directory path!')
		filename = env + '.conf'
		path = os.path.join(cls._config_dir, filename)
		options = cls.from_path(path)

		if 'env' not in options._options:
			raise ValueError("'env' value not set!")
		if options._options['env'] != env:
			raise ValueError(
				"'env' has bad value '%s'; should be '%s'"
				% options._options['env'], env
			)
		return options

	@classmethod
	def from_path(cls, path):
		try:
			config_file = open(path, 'r')
		except Exception as e:
			raise IOError("can't open '%s':%s" % (path, e))

		options = cls.from_file(config_file)
		config_file.close()
		return options

	@classmethod
	def from_file(cls, config_file):
		return cls.from_string(config_file.read())

	@classmethod
	def from_string(cls, config_string):
		return cls(parser.parse(config_string))

	def __getattr__(self, attr):
		if attr in self._options:
			return self._options[attr]
		else:
			raise AttributeError('no option key "%s"' % attr)

	def __getitem__(self, key):
		return self._options[key]

	def __setitem__(self, key, value):
		raise TypeError('option values may not be set after parsing!')

	def has(self, key):
		return key in self._options

	def is_set(self, key):
		return self.has(key)

	def get(self, key, default=None):
		return self._options.get(key, default)
