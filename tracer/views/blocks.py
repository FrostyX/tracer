from . import View
import sys

print_ = sys.stdout.write


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
					print block["title"]
				print_(block["content"])

				if self.next(index):
					print ""

	def next(self, index):
		"""Return True if there is any nonempty block after given index"""
		for block in self.args.blocks[index+1:]:
			if block["content"]:
				return True
		return False
