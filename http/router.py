from reply import Reply
import json
import re
import traceback

class route(object):
	"""Handler instance methods are decordated with @route
	all of these should return a gb.http.Reply
	and everything else will work itself out :3

	looks like this:

	@route('GET', regex='/foo/list', priority=10)
	def get_foo_list(self):
		return gb.http.Reply.text(200, "foo a, foo b, etc") # or whatever

	@route('GET', '/foo/\w{3,20}', 5)
	def get_foo_by_id(self):
		# get foo/ followed by 3-20 word characters to get a specific foo
		# or maybe a 404 if not given a legit foo_id
		...

	@route('GET', '.*', -1)
	def get_all(self):
		# catchall:, return an index page or something

	and so on.
	"""
	def __init__(self, http_method, regex, priority=0):
		"""
			http_method: e.g. "GET", "POST"

			regex: re to check against incoming request paths. note that a regex
				only matches, and thus triggers a dispatch to its method, the
				expression is automatically padded with ^ and $, such that the
				entire path must match. including extras doesnt hurt but it's
				not necessary
			
			priority (int): incoming request paths are matched against routes in
				descending order of priority. default priority is 0, and -1 is a
				good choice for catchalls, i.e. ".*"
		"""
		#self._route = (http_method, re.compile('^{0}$'.format(regex)), priority)

		self._http_method = http_method
		self._regex = re.compile('^{0}$'.format(regex))
		self._priority = priority

	def __call__(self, f):
		def wrapped_f(*args):
			return f(*args)
		#wrapped_f._route = self._route

		# this might be hairy???
		wrapped_f._http_method = self._http_method
		wrapped_f._regex = self._regex
		wrapped_f._priority = self._priority

		return wrapped_f

class Router(object):
	def __init__(self, routes=[]):
		# sort the routes in descending order by priority:
		# higher priorities will be matched first. useful for catchall methods
		self.routes = sorted(
			routes,
			key=lambda m: getattr(m, '_priority', 0),
			reverse=True
		)

	def verbose(self):
		return '\n'.join([
				('{0}: {1}'.format(m._priority, m._regex)) for m in self.routes
			]) or "(no routes)"

	def __call__(self, path):
		""" path - request path whose route we're looking for.
		attempt to match each route in descending order of priority against the 
		actual request path. if the route matches, the request is dispatched to
		the accompanying method, an instance method of the current gb.http.Handler

		return the method name! that's the important thing, it's how we'll call
		"""
		for m in self.routes:
			# path is a hit!
			if m._regex.match(path):
				return m
		return None

