import ssl, signal, select, os
import BaseHTTPServer
from server import Server
from handler import Handler
from SocketServer import _eintr_retry

class PLAIN:
	# xtra lazy namespace
	DISABLED = 0
	MIRROR   = 1
	REDIRECT = 2
	CUSTOM   = 3
	values = (0,1,2,3)

class SSLServer(Server):
	def __init__(self,
			listen_secure,
			handler,
			cert_path,
			key_path,
			plain_mode    = 0,
			listen_plain  = None,
			handler_plain = None
	):

		# figure out if we need to expose an http fallback
		try:
			if plain_mode in PLAIN.values:
				self.plain_mode = plain_mode
			else:
				self.plain_mode = getattr(PLAIN, str(plain_mode).upper())
		except:
			raise Exception("unrecognized mode '{0}'".format(repr(plain_mode)))

		Server.__init__(self, listen_secure, handler)
		#print listen_secure
		#print self.socket
		# the magic that allows simple https connections
		self.socket = ssl.wrap_socket(
			self.socket,
			certfile=cert_path,
			keyfile=key_path,
			server_side=True
		)

		# e.g. if any https is running
		if self.plain_mode:
			if listen_plain is None:
				raise Exception("need to specify `listen_plain` arg when running dual http+https")

			# CUSTOM plain mode requires a seperate, explicit handler
			if self.plain_mode == PLAIN.CUSTOM:
					if handler_plain is None:
						raise Exception("need to specify `handler_plain` when a separate handler is desired for http")

			# use the same handler for http and https
			elif self.plain_mode == PLAIN.MIRROR:
					handler_plain = handler

			# redirect all http requests to http asap
			elif self.plain_mode == PLAIN.REDIRECT:
					handler_plain = SSLRedirectHandler

			else:
					raise Exception("shouldn't be able to get this far without a valid plain_mode???")

			self.plain_server = Server(listen_plain, handler_plain)
		else:
			self.plain_server = None

	def serve_forever(self, poll_interval=0.5):
		# make sure every process knows the https parent pid
		secure_pid = os.getpid()
		plain_pid = os.fork() if self.plain_mode else None
		# when using simultaneous plain http, fork and run that part on the child.
		# os.fork() warns about ssl and multiprocessing. I think we're okay tho,
		# since only the parent does any ssl and its right on the socket???

		# plain (child) part:
		if plain_pid == 0:
			# TODO: catch signals from / poll for pid of parent?
			try:
				self.plain_server.serve_forever(poll_interval)
			finally:
				# could probably investigate the nature of our pid more closely,
				# however pidfiles are too tryhard atm
				if secure_pid == os.getppid():
					os.kill(secure_pid, signal.SIGTERM)


		# secure (parent) part:
		else:
			# might get away w/ lazy style? if more sophisticated management is desired
			# can override SocketServer.py copypastastyle
			try:
				Server.serve_forever(self, poll_interval)
			finally:
				# again, might want to think at least two seconds about our cleanup...
				# None == no fork even happened.
				if plain_pid is not None:
					os.kill(plain_pid, signal.SIGTERM)


from router import route
from reply import Reply
import json
class SSLRedirectHandler(Handler):
	@route('GET', '.*', -1)
	def redirect(self):
		# methinks this is probably a vuln right here :I
		location = "https://{host}{path}".format(host = self.headers['host'], path = self.path)
		return Reply.text(308, '', headers=dict(location=location))



