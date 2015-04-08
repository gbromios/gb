import BaseHTTPServer
import SocketServer
from handler import Handler

class Server(SocketServer.ForkingMixIn, BaseHTTPServer.HTTPServer):
	""" basic threaded http server """
	def __init__(self, server_address, handler):
		BaseHTTPServer.HTTPServer.__init__(self, server_address, handler)
		if not issubclass(handler, Handler):
			raise TypeError('gb.http.Server requires gb.http.Handler for its handler.')

		handler._decorate_routes()
