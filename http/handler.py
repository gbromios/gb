from router import Router
from reply import Reply
import BaseHTTPServer # kill in 3!
import inspect
import json
import socket
import urlparse

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
	# set these in subclasses.
	routers = {}

	def __init__(self, request, client_addr, server):
		# i wish:
		# super(Handler, self).__init__(request, client_addr, server)
		self._request_data = None
		self._split_path = None
		BaseHTTPServer.BaseHTTPRequestHandler.__init__(
			self, request, client_addr, server
		)

	@classmethod
	def _decorate_routes(cls):
		"""sets up all the @route methods so they can be used to match requests
		and send replies

		need a way to have this called automatically. I would flex with the
		metaclass, or BaseHTTPServer, but the fuss isn't worth it. these are all
		old-style classes and I'd rather make any real improvements as a part of
		porting this functionaility to http.server in python 3

		Just call it manually when ya start the server.
		"""
		found_routes = {}
		# list of all @route methods:
		for n, m in inspect.getmembers(cls, predicate=inspect.ismethod):
			# method which has a route and needs to be registered:
			if hasattr(m, '_http_method'):
				hm = m._http_method
				r = m._regex
				p = m._priority

				#print n, hm, r, p, m.__name__

				if hm not in found_routes:
						found_routes[hm] = []
				found_routes[hm].append(m)


		# once all the methods have been found and sorted by http method,
		# initialize their respective Routers, where they are sorted by priority
		cls.routers = {
			hm:Router(rlist)
			for hm, rlist in found_routes.items()
		}

		# ends up looking like:
		# { 'GET': <Router instance>, 'POST': <Router instance>, ... }
		# the Router instance sorts the routes internally, and selects from
		# among them when handling a request.

	def handle_one_request(self):
		"""Handle a single HTTP request."""
		try:
			self.raw_requestline = self.rfile.readline(65537)
			if len(self.raw_requestline) > 65536:
				self.requestline = ''
				self.request_version = ''
				self.command = ''
				self.send_error(414)
				return
			if not self.raw_requestline:
				self.close_connection = 1
				return
			if not self.parse_request():
				# An error code has been sent, just exit
				return

			# gb.http.Handler overrides
			#

			if self.command not in self.routers:
				self.send_error(400, "Unsupported method '{0}'".format(self.command))
				return

			# here is the dispatch: the router is selected based on the http
			# method (e.g. GET, POST, PUT); then based on the path segment of
			# the url, the router matches each route in desc. order of priority
			# and is guaranteed to get a gb.http.Reply in return, which we know
			# how to send

			method = self.routers[self.command](self.path_no_qs)
			if method is None:
				self.send_error(404, "no route matched '{0}'".format(self.command))
				return

			reply =  method(self) #getattr(self, name)()

			# heh, this could be cleaned up but unfortunately im lazy but also
			# appreciate fresh looking address bars at least in dev
			if self.headers.getheader('Origin'):
				reply.headers['Access-Control-Allow-Origin'] = self.headers.getheader('Origin')
			self.send_http_reply(reply)

			# end custom part
			#

			self.wfile.flush() #actually send the response if not already done.
		except socket.timeout, e:
			#a read or a write timed out.  Discard this connection
			self.log_error("Request timed out: %r", e)
			self.close_connection = 1
			return

	@property
	def request_data(self):
		if self._request_data is None:
			self._request_data = self._parse_request()
		return self._request_data

	@property
	def raw_data(self):
		# sorta like request_type, if no body is evident, assume that its a query
		# string, since it'll still work if there's neither.
		if self.request_length:
			return self.rfile.read(self.request_length)
		else:
			return urlparse.urlparse(self.path).query or ''

	@property
	def request_type(self):
		# if there's a given content-type, that's that, but absent a content-type,
		# just assume there's an empty body, and any data will be urlencoded. this
		# fails gracefully if there's neither, less finicky than more exact methods
		return self.headers.getheader('content-type') or 'application/x-www-form-urlencoded'

	@property
	def request_length(self):
		# same as request_type, see above
		try:
			return int(self.headers.getheader('content-length'))

		except TypeError, ValueError:
			return 0

	def _parse_request(self):
		"""return a dict of postdata"""
		# fairly lazy/imprecise, but works perfectly for the current need
		if 'application/x-www-form-urlencoded' in self.request_type:
			return self._query_string_to_dict(self.raw_data)

		elif 'application/json' in self.request_type:
			return json.loads(self.raw_data)

		else:
			raise ValueError("406: bad content-type {0}".format(content_type))

	@property
	def split_path(self):
		return self.path_no_qs.strip('/').split('/')

	@property
	def path_no_qs(self):
		return urlparse.urlparse(self.path).path.rstrip('/')

	@property
	def query(self):
		return urlparse.urlparse(self.path).query

	@staticmethod
	def _query_string_to_dict(qs):
		return dict([
				Handler._qs_pair_to_py(k,v)
				for k,v in urlparse.parse_qs(qs).items()
			])

	@staticmethod
	def _qs_pair_to_py(k, v):
		if k.endswith('[]'):
			return (
				k.rstrip('[]'), (
					[Handler._qs_arg_to_py(arg) for arg in v]
				)
			)

		else:
			return k, Handler._qs_arg_to_py(v[0])

	@staticmethod
	def _qs_arg_to_py(v):
		# the complexity of this can be increased if necessary
		# but I doubt it will need that much thought.
		# as of now, it's either an int or a string.
		try:
			return int(v)
		except:
			return str(v)

	def send_http_reply(self, http_reply):
		""" sends response code, http headers and body back to client
			Accepts: gb.http.Reply http_reply
			Returns: None
		"""
		if not isinstance(http_reply, Reply):
			raise TypeError("expected  Reply instance, not %s" % type(http_reply))
		self.send_response(http_reply.code)
		for h,v in http_reply.headers.items():
			self.send_header(h, v)
		self.end_headers()
		self.wfile.write(http_reply.body)
