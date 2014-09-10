#!/usr/bin/python
#-*- coding: utf-8 -*-
# helper.py
# Defines HelperController
#
# Copyright (C) 2013 Jakub Kadlčík
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

import time
import datetime
from psutil import AccessDenied

import tracer.resources.memory as Memory
from tracer.views.helper import HelperView
from tracer.resources.lang import _
from tracer.resources.tracer import Tracer
from tracer.resources.applications import Applications


class HelperController(object):

	args = None

	def __init__(self, args):
		self.args = args

	def render(self):
		self.print_helper(self.args.helper[0], self.args)

	def print_helper(self, app_name, args):
		process = Memory.process_by_name(app_name)
		if process:
			tr = Tracer()
			package = tr.package_info(app_name)
			app = Applications.find(app_name)

			now = datetime.datetime.fromtimestamp(time.time())
			started = datetime.datetime.fromtimestamp(process.create_time)
			started = now - started

			started_str = ""
			if started.days > 0:
				started_str = str(started.days) + " days"
			elif started.seconds >= 60 * 60:
				started_str = str(started.seconds / (60 * 60)) + " hours"
			elif started.seconds >= 60:
				started_str = str(started.seconds / 60) + " minutes"
			elif started.seconds >= 0:
				started_str = str(started.seconds) + " seconds"

			try: affected_by = tr.who_affected(app_name) if args.verbose else None
			except AccessDenied: affected_by = _("affected_by_forbidden")

			view = HelperView()
			view.assign("args", args)
			view.assign("process", process)
			view.assign("application", app)
			view.assign("package", package)
			view.assign("time", started_str)
			view.assign("affected_by", affected_by)
			view.render()
		else:
			print _("app_not_running").format(app_name)
