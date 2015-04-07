class NoOptions(object):
	"""Placeholder object for uncofigured objects/classes"""
	def get(self, value, default=None):
		"""If an options object hasn't been loaded, default values will still work.
		"""
		return default

	def __getattr__(self, name):
		raise AttributeError('Attemtped to access options but none have been loaded!')

	def __getitem__(self, name):
		raise AttributeError('Attemtped to access options but none have been loaded!')

	def __bool__(self):
		return False

	def __nonzero__(self):
		return False


class Optionable(object):
	"""Options may be assigned to an object, a class, or globally (to every
	Optionalbe), but this can never be done to the class/superclass of an
	object or class that has already had options registerered to it.

	at the same time, any object or class that has options registered to it may
	not register a different options instance.
	"""
	# cause an error to be raised when accessing options before loaded.
	Opts = NoOptions()
	subclass_registered_options = False

	def register_options(self, options):
		if self.Opts or self.__class__.Opts or Optionable.Opts:
			raise ValueError('%s already has already loaded options!'\
			                 % (repr(self),))
		if self.__class__.Opts:
			raise ValueError('%s already has already loaded options!'\
			                  % (repr(cls),))
		if Optionable.Opts:
			raise ValueError('%s already has already loaded a options!'\
			                  % (repr(Optionable),))
		self.Opts = options
		
		self.__class__.mark_subclass_registered_options(repr(self))

	@classmethod
	def mark_subclass_registered_options(cls, obj):
		if cls.subclass_registered_options:
			return
		cls.subclass_registered_options = obj
		for b in cls.__bases__:
			if issubclass(b, Optionable):
				b.mark_subclass_registered_options(obj)

	@classmethod
	def register_options_class(cls, options):
		if cls is Optionable:
			raise TypeError('to register options for all Optionable,' +\
			                'use `Optionable.register_options_global(<Options instance>)`')
		if cls.Opts:
			raise ValueError('%s already has already loaded options!'\
			                  % (repr(cls),))
		if Optionable.Opts:
			raise ValueError('%s already has already loaded options!'\
			                  % (repr(Optionable),))
		if cls.subclass_registered_options:
			raise ValueError(('cannot register options for class %s ' +\
			                  'after %s has already registered!') %\
			                 (repr(cls), cls.subclass_registered_options))

		cls.Opts = options
		cls.mark_subclass_registered_options(repr(cls))

	@staticmethod
	def register_option_global(options):
		if Optionable.Opts:
			raise ValueError('%s already has already loaded options!'\
			                  % (repr(Optionable),))

		if Optionable.subclass_registered_options:
			raise ValueError(('cannot register options for all Optionables '+\
			                  'after  %s has already registered!') %\
			                 (Optionable.class_registered_to_all,))

		Optionable.Opts = options
