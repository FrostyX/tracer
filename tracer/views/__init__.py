from __future__ import print_function
from __future__ import unicode_literals

from sys import __stdout__, version_info


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

	def print(self, text, end=None):
		if version_info.major == 2:
			text = text.encode("utf8")

		print(text, end=end, file=self.out)
