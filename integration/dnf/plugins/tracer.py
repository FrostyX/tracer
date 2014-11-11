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

from __future__ import absolute_import
import sys
sys.path.pop(0) # To avoid filename conflict

import time
import dnf.cli
import subprocess
from tracer.resources.lang import _


class Tracer(dnf.Plugin):
	"""DNF plugin for `tracer` command"""
	name = 'tracer'

	def __init__(self, base, cli):
		self.timestamp = time.time()
		self.base = base
		self.cli = cli
		if self.cli is not None:
			self.cli.register_command(TracerCommand)

	def transaction(self):
		"""
		Call after successful transaction
		See https://rpm-software-management.github.io/dnf/api_transaction.html
		"""
		installed = set([package.name for package in self.base.transaction.install_set])
		erased = set([package.name for package in self.base.transaction.remove_set])

		# Don't run tracer when uninstalling it
		if "tracer" in erased - installed:
			return

		args = ['tracer', '-n'] + list(installed | erased)
		p = subprocess.Popen(args, stdout=subprocess.PIPE)
		out = p.communicate()[0]
		_print_output(out)

		if len(out) != 0:
			print "\n" + _("for_more_informations")
			print "    sudo tracer -iat " + str(self.timestamp)


class TracerCommand(dnf.cli.Command):
	"""DNF tracer plugin"""
	aliases = ['tracer']
	activate_sack = True

	def run(self, args):
		"""Called after running `dnf tracer ...`"""
		args = ['tracer'] + args
		p = subprocess.Popen(args, stdout=subprocess.PIPE)
		out = p.communicate()[0]
		_print_output(out)


def _print_output(out):
	if len(out) == 0:
		print _("you_should_restart")
		print "  " + _("nothing_to_restart")
		return

	# Last value is blank line
	for line in out.split('\n')[:-1]:
		print line
