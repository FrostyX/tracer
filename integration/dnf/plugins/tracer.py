#-*- coding: utf-8 -*-
# tracer.py
# Calls tracer after every successful transaction.
# Also supplies the 'tracer' command.
#
# Copyright (C) 2014 Jakub Kadlčík
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

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
		out = p.communicate()[0]
		_print_output(out)


class TracerCommand(dnf.cli.Command):
	"""DNF tracer plugin"""
	aliases = ['tracer']
	activate_sack = True

	def run(self, args):
		"Called after running `dnf tracer ...`"
		args = ['tracer'] + args
		p = subprocess.Popen(args, stdout=subprocess.PIPE)
		out = p.communicate()[0]
		_print_output(out)


def _print_output(out):
	print 'You should restart:'
	if len(out) == 0:
		print "  Nothing needs to be restarted"
		return

	# Last value is blank line
	for line in out.split('\n')[:-1]:
		print "  " + line
