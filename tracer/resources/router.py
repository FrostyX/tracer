#-*- coding: utf-8 -*-
# router.py
# Router chooses the right controller and its method and calls it
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
from tracer.version import __version__
from tracer.resources.lang import _
# WARNING: There are local imports in dispatch method


class Router:

	args = None
	packages = None

	def __init__(self, args, packages):
		self.args = args
		self.packages = packages

	def dispatch(self):
		if self.args.helper:
			from tracer.controllers.helper import HelperController
			controller = HelperController(self.args, self.packages)
			controller.render()

		elif self.args.version:
			print(__version__)

		elif self.args.resource:
			from tracer.controllers.resource import ResourceController
			controller = ResourceController(self.args)
			controller.render()

		else:
			from tracer.controllers.default import DefaultController
			controller = DefaultController(self.args, self.packages)
			if self.args.helpers:
				controller.render_helpers()
			elif self.args.interactive:
				controller.render_interactive()
			else:
				controller.render()
