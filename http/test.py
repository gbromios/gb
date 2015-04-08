from gb.http import *

class Foo(object):
	sample_foos = dict(
		first = "baaaaah",
		my_cool_foo = "a custom high quality foo",
		bwaaah = 5677
	)

	class NoFoo4U(KeyError):
		"""NO FOO 4 U!!!"""

	@classmethod
	def all(cls):
		return repr(cls.sample_foos)

	@classmethod
	def from_id(cls, fid):
		try:
			return cls.sample_foos[fid]
		except KeyError:
			raise cls.NoFoo4U



class FHandler(Handler):
	@route('GET', '^/foo/list$', priority=10)
	def get_foo_list(self):
		return Reply.text(200, Foo.all())

	@route('GET', '^/foo/\w{3,20}$', 5)
	def get_foo_id(self):
		# we know the regex we matched has two "segments" (dirs???)
		# so we know that the '/' separated path has two items and p[1] is okay
		foo_id = self.split_path[1]

		try:
			return Reply.text(200, str(Foo.from_id(foo_id)))

		except Foo.NoFoo4U:
			return Reply.text(
			404,
			"404, can't find foo with id '{0}'".format(foo_id)
			)

	@route('GET', '.*', -1)
	def get_catchall(self):
		return Reply.text(400, "wat is {0}".format(self.path))

Server(('0.0.0.0',2799), FHandler).serve_forever()
