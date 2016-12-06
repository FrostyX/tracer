#-*- coding: utf-8 -*-
# helper.py
# Defines HelperController
#
# Copyright (C) 2016 Jakub Kadlcik
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

from psutil import AccessDenied

from tracer.resources.system import System
from tracer.resources.memory import dump_memory
from tracer.views.helper import HelperView
from tracer.resources.lang import _
from tracer.resources.tracer import Tracer
from tracer.resources.applications import Applications
from tracer.resources.rules import Rules


class HelperController(object):

	args = None
	packages = None

	def __init__(self, args, packages=None):
		self.args = args
		self.packages = packages

	def render(self):
		for app_name in self.args.helper:
			self.print_helper(Applications.find(app_name), self.args)
			if app_name != self.args.helper[-1]:
				print("")

	def print_helper(self, app, args):
		if app.instances:
			manager = System.package_manager()
			package = manager.provided_by(app)
			if package:
				package.load_info(System.package_manager())

			tr = Tracer(System.package_manager(), Rules, Applications)
			tr.now = self.args.now
			if self.packages:
				tr.specified_packages = self.packages

			try: affected_by = tr.trace_application(app)
			except AccessDenied: affected_by = _("You don't have enough permissions")
			affects = self._affects(app, affected_by)

			view = HelperView()
			view.assign("args", args)
			view.assign("processes", app.instances)
			view.assign("application", app)
			view.assign("package", package)
			view.assign("affected_by", affected_by)
			view.assign("affects", affects)
			view.render()
		else:
			print(_("Application called {0} is not running").format(app.name))

	def _affects(self, app, affected_by):
		if not affected_by:
			return None

		last = affected_by[-1].name()
		if last == app.name:
			return None

		if last not in [p.parent().name() for p in app.instances]:
			return None

		return last
