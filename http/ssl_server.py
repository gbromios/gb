import ssl, signal, select, os
import BaseHTTPServer
from server import Server
from handler import Handler
from SocketServer import _eintr_retry

class SSLServer(Server):
	def __init__(self, server_address, handler, cert_path, key_path, plain_address=None, redirect_plain=True, plain_handler=None):
		print server_address
		Server.__init__(self, server_address, handler)
		print self.socket
		self.socket = ssl.wrap_socket(
			self.socket,
			certfile=cert_path,
			keyfile=key_path,
			server_side=True
		)

		# optionally provide a way to redirect HTTP connections
		self.plain_pid = None
		self.plain_server = None
		if plain_address:
			self.plain_server = Server(
				plain_address,
				handler if plain_handler else handler
			)

	def serve_forever(self, poll_interval=0.5):
		if self.plain_server:
			# plain server forks its own http server
			self.plain_pid = os.fork()
			if self.plain_pid == 0:
				self.plain_server.serve_forever(poll_interval)
				# should be enough unless calling code is catching exits?
				raise SystemExit
		print dir(self)
		self._BaseServer__is_shut_down.clear()
		try:
			while not self._BaseServer__shutdown_request:
				r, w, e = _eintr_retry(select.select, [self], [], [], poll_interval)
				if self in r:
					self._handle_request_noblock()
		finally:
			# kill http child if it exists 
			if self.plain_pid:
				os.kill(self.plain_pid, signal.SIGTERM)
				self._BaseServer__shutdown_request = False
				self._BaseServer__is_shut_down.set()

class SSLRedirectHandler(Handler):
	pass
