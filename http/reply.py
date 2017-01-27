import json
import magic
class Reply(object):
	def __init__(self, code, body, headers={}):
		self.code = code
		self.body = body
		self.headers = headers

	def __iter__(self):
		return (self.code, self.body, self.headers).__iter__()

	@classmethod
	def text(cls, code, body, content_type="text/plain", headers={}):
		"""any plaintext reply should eventualy use this method"""
		
		headers['content-type'] = content_type
		# does this need to be a thing py3 or can it stay VV
		headers['content-length'] = len(body.encode('utf-8'))
		return cls(code, body, headers)

	@classmethod
	def json(cls, code, data, headers={}, encoder=None):
		"""accepts a json-serializable data object"""
		body = json.dumps(data)
		return cls.text(code, body, "application/json; charset=utf-8", headers)

	@classmethod
	def filename(cls, filename, headers={}):
		"""plop in a filename to send its contents as an http reply
		TODO: should be able to pass a code for Reply.filename(self):
		"""
		try:
			with open(filename, 'rb') as f:
				body = f.read()
		except OSError:
			return cls.text('400: "{0}" not found'.format(filename))

		headers['content-type'] = cls.mime_type(filename)
		headers['content-length'] = len(body)
		return cls(200, body, headers)

	@staticmethod
	def mime_type(filename):
		"""returns the mime type for a given filename
		not sure why i needed to specify these three types? might look later.
		"""
		if filename.endswith('.css'):
			return "text/css"

		if filename.endswith('.js'):
			return "text/javascript"

		if filename.endswith('.html'):
			return "text/html"

		return magic.from_file(filename, mime=True)
