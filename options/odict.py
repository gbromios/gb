class ODict(dict):
	"""option dict, you can access foo['bar']['baz'] like foo.bar.baz; oooh"""
	def __init__(self, *args, **kwargs):
		dict.__init__(self, *args, **kwargs)
		for (k, v) in self.items():
			self[k] = (
				ODict._handle_list(v) if isinstance(v, list)
				else ODict(v) if isinstance(v, dict)
				else v
			)

	@staticmethod
	def _handle_list(l):
		return [
			ODict._handle_list(i) if isinstance(i, list)
			else ODict(i) if isinstance(i, dict)
			else i
			for i in l
		]

	def __getattr__(self, attr):
		if attr in self:
			return self[attr]
		else:
			raise AttributeError("'%s' not found" % attr)
