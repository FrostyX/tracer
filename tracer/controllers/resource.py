#-*- coding: utf-8 -*-
# resource.py
# Defines ResourceController
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


from __future__ import absolute_import

import os
import psutil
from datetime import datetime
from tracer.resources.processes import Processes
from tracer.resources.system import System
from tracer.resources.rules import Rules
from tracer.resources.applications import Applications
from tracer.version import __version__

from tracer.views.resource.processes import ProcessesView
from tracer.views.resource.packages import PackagesView
from tracer.views.resource.rules import RulesView
from tracer.views.resource.applications import ApplicationsView
from tracer.views.resource.system import SystemView


class ResourceController(object):

	args = None

	def __init__(self, args):
		self.args = args

	def render(self):
		r = self.args.resource[0]
		if   r == 'processes':    self.render_processes()
		elif r == 'packages':     self.render_packages()
		elif r == 'rules':        self.render_rules()
		elif r == 'applications': self.render_applications()
		elif r == 'system':       self.render_system()

	def render_processes(self):
		view = ProcessesView()
		view.assign('processes', Processes.all())
		view.render()

	def render_packages(self):
		timestamp = self.args.timestamp[0] if self.args.timestamp[0] else System.boot_time()
		manager = System.package_manager()
		packages = manager.packages_newer_than(timestamp)

		view = PackagesView()
		view.assign('packages', packages)
		view.assign('boot_time', System.boot_time())
		view.render()

	def render_rules(self):
		view = RulesView()
		view.assign('rules', Rules.all())
		view.render()

	def render_applications(self):
		view = ApplicationsView()
		view.assign('applications', Applications.all())
		view.render()

	def render_system(self):
		uptime = datetime.now() - datetime.fromtimestamp(System.boot_time())
		uptime = str(uptime).split('.')[0]

		try:
			users = set([user.name for user in psutil.get_users()])
		except AttributeError:
			users = set([user.name for user in psutil.users()])
		package_managers = System.package_manager().names()

		view = SystemView()
		view.assign('python', System.python_version())
		view.assign('distribution', System.distribution())
		view.assign('package_managers', package_managers)
		view.assign('init', System.init_system())
		view.assign('uptime', uptime)
		view.assign('user', System.user())
		view.assign('users', users)
		view.assign('version', __version__)
		view.assign('rules_count', len(Rules.all()))
		view.assign('applications_count', len(Applications.all()))
		view.render()
