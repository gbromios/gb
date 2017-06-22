from parser import parse

data = open('test.conf').read()

#print parse(data)

class A(object):
	m = [
		("a", A.a),
	]

	def a(self):
		return 3
