from gb.http import *

sample_foos = dict(
	first = "baaaaah",
	my_cool_foo = "a custom high quality foo",
	bwaaah = "hank"
)

class FHandler(Handler):
	@route('GET', '^/foo/list$', priority=10)
	def get_foo_list(self):
		return Reply.text(200, repr(sample_foos))

	@route('GET', '^/foo/\w{3,20}$', 5)
	def get_foo_id(self):
		# we know the regex we matched has two "segments" (dirs???)
		# so we know that the '/' separated path has two items and p[1] is okay
		foo_id = self.split_path[1]

		try:
			return Reply.text(200, sample_foos[foo_id])

		except KeyError:
			return Reply.text(
			404,
			"404, can't find foo with id '{0}'".format(foo_id)
			)

	@route('GET', '.*', -1)
	def get_catchall(self):
		return Reply.text(404, "this Fooniverse hath no {0}".format(self.path))

	# just an example POST route illustrating request data access. the changes to
	# sample_foos won't actually be persistent, you'd need a db for that.
	@route('POST', '^/foo/?')
	def post_foo(self):
		if len(sample_foos) > 10:
			return Reply.text(400, "Maximum Foos reached")

		try:
			foo_key = self.request_data['key']
			foo_val = self.request_data['value']

			if foo_key in sample_foos and len(sample_foos[foo_key]) >= len(foo_val):
				raise ValueError

			old_foo = sample_foos.get(foo_key)
			sample_foos[foo_key] = foo_val
			if old_foo is not None:
				return Reply(200, '"{0}" : "{1}" => "{2}" (embiggened by {3})'.format(
					foo_key,
					old_foo,
					foo_val,
					len(foo_val) - len(old_foo)
				))
			else:
				return Reply(200, '{0} '.format(
					sample_foos
				))

		except KeyError:
			return Reply.text(400, "must supply foo params `key` and `value`")
		except ValueError:
			return Reply.text(400, "can only embiggen existing foos, never shrink")

class BHandler(Handler):
	@route('GET', '.*', -1)
	def get_catchall(self):
		return Reply.text(200, "AINT ME GOT NO {0}".format(self.path))



if __name__ == '__main__':
	Server(('0.0.0.0',2799), FHandler).serve_forever()
