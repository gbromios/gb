from gb.http import *
import server

cert_path='/root/secret-whispers/themoonischill.x509.crt'
key_path='/root/secret-whispers/themoonischill.key'

SSLServer(('0.0.0.0',2799), server.FHandler, cert_path, key_path, plain_address=('0.0.0.0', 2798)).serve_forever()
