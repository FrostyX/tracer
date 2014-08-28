#!/usr/bin/python
#-*- coding: utf-8 -*-
# tracer.py
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
import datetime
from psutil import AccessDenied
from tracer.version import __version__
from tracer.resources.lang import _
from tracer.resources.tracer import Tracer
from tracer.resources.args_parser import parser
from tracer.resources.package import Package
from tracer.resources.exceptions import UnsupportedDistribution, PathNotFound, LockedDatabase
from tracer.resources.applications import Applications
from tracer.resources.ProcessesList import ProcessesList
import tracer.resources.memory as Memory
import tracer.resources.system as System

import tracer.templates.default
import tracer.templates.helper
import tracer.templates.interactive
import tracer.templates.note_for_hidden


def run():
	args = parser.parse_args()

	if args.helper:
		print_helper(args.helper[0], args)
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

		if args.helpers: _print_helpers(processes, args)
		elif args.interactive: _print_all_interactive(processes, args)
		else: _print_all(processes, args)

	except (UnsupportedDistribution, PathNotFound, LockedDatabase) as ex:
		print ex


def _user(user):
	if   user == '*':    return None
	elif not user:       return os.getlogin()
	else: return user[0]


def _processes(processes, args):
	return processes.exclude_types([
		Applications.TYPES['STATIC'],
		Applications.TYPES['SESSION']
	]) if not args.all else processes


def _print_all(processes, args):
	filtered = _processes(processes, args)

	tracer.templates.default.render(
		processes = filtered,
		args = args,
		total_count = len(processes),
		session_count = processes.count_type(Applications.TYPES['SESSION']),
		static_count = processes.count_type(Applications.TYPES['STATIC'])
	)


def _print_helpers(processes, args):
	for process in _processes(processes, args):
		print_helper(process.name, args)
		print ""

	tracer.templates.note_for_hidden.render(
		args = args,
		total_count = len(processes),
		session_count = processes.count_type(Applications.TYPES['SESSION']),
		static_count = processes.count_type(Applications.TYPES['STATIC'])
	)


def _print_all_interactive(processes, args):
	filtered = _processes(processes, args)

	while True:
		tracer.templates.interactive.render(
			processes = filtered,
			args = args,
			total_count = len(processes),
			session_count = processes.count_type(Applications.TYPES['SESSION']),
			static_count = processes.count_type(Applications.TYPES['STATIC'])
		)

		answer = raw_input("--> ")
		try:
			if answer == "q": return
			elif int(answer) <= 0 or int(answer) > len(filtered): raise IndexError
			print_helper(filtered[int(answer) - 1].name, args)

		except (SyntaxError, IndexError, ValueError):
			print _("wrong_app_number")

		raw_input("\n" + _("press_enter"))


def print_helper(app_name, args):
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

		how_to_restart = app.helper if app.helper else _("not_known_restart")

		try: affected_by = tr.who_affected(app_name) if args.verbose else None
		except AccessDenied: affected_by = _("affected_by_forbidden")

		tracer.templates.helper.render(
			args = args,
			process = process,
			application = app,
			package = package,
			time = started_str,
			affected_by = affected_by,
			how_to_restart = how_to_restart
		)
	else:
		print _("app_not_running").format(app_name)
