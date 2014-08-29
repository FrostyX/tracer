#!/usr/bin/python
#-*- coding: utf-8 -*-
# main.py
# Tracer finds outdated running applications in your system
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

import os
import sys
import time
from tracer.version import __version__
from tracer.resources.lang import _
from tracer.resources.tracer import Tracer
from tracer.resources.args_parser import parser
from tracer.resources.package import Package
from tracer.resources.exceptions import UnsupportedDistribution, PathNotFound, LockedDatabase
from tracer.resources.ProcessesList import ProcessesList

from tracer.controllers.default import DefaultController
from tracer.controllers.helper import HelperController


def run():
	args = parser.parse_args()

	if args.helper:
		controller = HelperController()
		controller.render(args)
		sys.exit()

	if args.version:
		print __version__
		sys.exit()

	if os.getuid() != 0:
		print _("root_only")
		sys.exit()

	_main(args)


def _main(args):
	# If there is something on stdin (that means piped into tracer)
	stdin_packages = []
	if not sys.stdin.isatty():
		stdin_packages = sys.stdin.readline().split()

	# All input packages enchanced by actual time (as modified time)
	packages = []
	for package in args.packages + stdin_packages:
		packages.append(Package(package, time.time() if args.now else None))

	try:
		tracer = Tracer()
		tracer.specified_packages = packages
		tracer.now = args.now

		processes = ProcessesList(tracer.trace_running(_user(args.user)))
		if not processes: return

		if args.helpers:
			controller = DefaultController()
			controller.render_helpers(processes, args)
		elif args.interactive:
			controller = DefaultController()
			controller.render_interactive(processes, args)
		else:
			controller = DefaultController()
			controller.render(processes, args)

	except (UnsupportedDistribution, PathNotFound, LockedDatabase) as ex:
		print ex


def _user(user):
	if   user == '*':    return None
	elif not user:       return os.getlogin()
	else: return user[0]
