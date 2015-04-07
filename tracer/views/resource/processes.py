from __future__ import unicode_literals

from .. import View


class ProcessesView(View):
	def render(self):
		line = "{0:<10}{1:<20}{2:<20}{3:<10}"
		print(line.format("PID", "Time running", "User", "Process"))
		print(100 * "-")
		for process in self.args.processes.sorted("create_time"):
			print(line.format(process.pid, process.str_started_ago, process.username(), process.name()))
