from __future__ import print_function
from __future__ import unicode_literals

from . import View
import sys


class BlocksView(View):

	"""
	Assign ``blocks`` with this list

	[
		{
			"title": "...",
			"content": "some text",
		},
		...
	]
	"""

	def render(self):
		for index, block in enumerate(self.args.blocks):
			if block["content"]:
				if "title" in block:
					self.print(block["title"])
				self.print(block["content"], end="")

				if self.next(index):
					self.print("")

	def next(self, index):
		"""Return True if there is any nonempty block after given index"""
		for block in self.args.blocks[index+1:]:
			if block["content"]:
				return True
		return False

	def has_content(self):
		"""Return True if at least one block's content is not empty"""
		return self.next(-1)
