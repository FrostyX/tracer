# license

import dnf
import subprocess

class Tracer(dnf.Plugin):
	"""DNF plugin for `tracer` command"""
	name = 'tracer'

	def __init__(self, base, cli):
		self.base = base
		self.cli = cli
		if self.cli is not None:
			self.cli.register_command(TracerCommand)

	def transaction(self):
		"""
		Call after successful transaction
		Warning, this code uses undocummented parts. See https://bugzilla.redhat.com/show_bug.cgi?id=1067156
		"""
		items = []
		for transaction_item in self.base.transaction:
			item = transaction_item.installed.name if transaction_item.installed else transaction_item.erased.name
			items.append(item)

		args = ['tracer', '-n'] + items
		p = subprocess.Popen(args, stdout=subprocess.PIPE)
		out, err = p.communicate()

		print 'Calling tracer'
		print out


class TracerCommand(dnf.cli.Command):
	"""DNF tracer plugin"""
	aliases = ['tracer']
	activate_sack = True

	def run(self, args):
		"Call after running `dnf tracer ...`"
		for arg in args:
			print arg
