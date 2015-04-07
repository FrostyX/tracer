from __future__ import unicode_literals

from .. import View


class RulesView(View):
	def render(self):
		line = "{0:<40}{1:<10}"
		print(line.format("Rule", "Action"))
		print(55 * "-")
		for rule in self.args.rules:
			print(line.format(rule.name, rule.action))
