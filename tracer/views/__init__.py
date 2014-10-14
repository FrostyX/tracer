class Arguments(object):
	pass


class View(object):
	args = Arguments()

	def assign(self, key, value):
		self.args.__dict__[key] = value

	def get(self, key):
		return self.args.__dict__[key]