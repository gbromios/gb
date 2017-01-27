#!/usr/bin/python

from gb.http import *
import server

cert_path='/root/secret-whispers/themoonischill.x509.crt'
key_path='/root/secret-whispers/themoonischill.key'

SSLServer(
	('0.0.0.0',443),
	server.FHandler,
	cert_path,
	key_path,
	plain_mode    = 'redirect',
	listen_plain  = ('0.0.0.0', 80)

).serve_forever()
