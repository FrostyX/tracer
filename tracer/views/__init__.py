from sys import __stdout__


class Arguments(object):
	pass


class View(object):
	args = Arguments()
	out = None

	def __init__(self, out=__stdout__):
		self.out = out

	def assign(self, key, value):
		self.args.__dict__[key] = value

	def get(self, key):
		return self.args.__dict__[key]