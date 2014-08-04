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

# Enable importing modules from parent directory (tracer's root directory)
import os
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.sys.path.insert(0, parentdir)

import sys
import time
import datetime
from tracer.version import __version__
from tracer.resources.lang import _
from tracer.resources.tracer import Tracer
from tracer.resources.args_parser import args
from tracer.resources.package import Package
from tracer.resources.exceptions import UnsupportedDistribution, PathNotFound, LockedDatabase
from tracer.resources.applications import Applications
from tracer.resources.ProcessesList import ProcessesList
import tracer.resources.memory as Memory
import tracer.resources.system as System


def main(argv=sys.argv, stdin=[]):
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

		if not args.helpers: print _("you_should_restart")
		if args.interactive: _print_all_interactive(processes, args)
		else: _print_all(processes, args)

	except (UnsupportedDistribution, PathNotFound, LockedDatabase) as ex:
		print ex

def _user(user):
	if   user == '*':    return None
	elif user == None:   return os.getlogin()
	else: return user[0]

def _print_all(processes, args):
	filtered = processes.exclude_types([
		Applications.TYPES['STATIC'],
		Applications.TYPES['SESSION']
	]) if not args.all else processes

	for process in filtered:
		if args.helpers:
			print_helper(process.name)
		else:
			print "  " + process.name

	if not args.all: _print_note_for_hidden(
		len(processes),
		processes.count_type(Applications.TYPES['SESSION']),
		processes.count_type(Applications.TYPES['STATIC'])
	)

def _print_all_interactive(processes, args):
	filtered = processes.exclude_types([
		Applications.TYPES['STATIC'],
		Applications.TYPES['SESSION']
	]) if not args.all else processes

	while True:
		i = 1
		digits = len(str(len(filtered)))
		for process in filtered:
			n = "[{0}]".format(i).ljust(digits + 2)
			print "{} {}".format(n, process.name)
			i += 1

		if not args.all: _print_note_for_hidden(
			len(processes),
			processes.count_type(Applications.TYPES['SESSION']),
			processes.count_type(Applications.TYPES['STATIC'])
		)

		print "\n" + _("prompt_help")
		answer = raw_input("--> ")
		try:
			if answer == "q": return
			elif int(answer) <= 0 or int(answer) > i: raise IndexError
			print_helper(filtered[int(answer) - 1].name)

		except (SyntaxError, IndexError, ValueError):
			print _("wrong_app_number")

		raw_input(_("press_enter"))

def _print_note_for_hidden(total_count, session_count, static_count):
	if not args.quiet and (session_count > 0 or static_count > 0):
		if session_count + static_count != total_count:
			print ""

		print _("note_unlisted_apps")
		if session_count > 0:
			print _("requiring_session").format(session_count)

		if static_count > 0:
			print _("requiring_reboot").format(static_count)

def _affected_by_str(app_name):
	if args.verbose == 0:
		return ""

	tracer = Tracer()
	affected_by = tracer.who_affected(app_name)

	indent = "    "
	s = "\n" + indent + _("affected_by") + ":\n"
	for package in affected_by:
		s += 2 * indent + package + "\n"
	return s

def print_helper(app_name):
	try:
		tracer = Tracer()
		package = tracer.package_info(app_name)
		process = Memory.process_by_name(app_name)
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

		affected_by = _affected_by_str(app_name)
		how_to_restart = app['helper'] if app['helper'] else _("not_known_restart")

		print _("helper").format(
			app_name = app_name,
			pkg_name = package.name,
			type = app["type"].capitalize(),
			pkg_description = package.description,
			user = process.username,
			time = started_str,
			pid = process.pid,
			affected_by = affected_by,
			how_to_restart = how_to_restart,
		)

	except AttributeError:
		print _("app_not_running").format(app_name)



if __name__ == '__main__':
	if args.helper:
		print_helper(args.helper[0])
		sys.exit()

	if args.version:
		print __version__
		sys.exit()

	if os.getuid() != 0:
		print _("root_only")
		sys.exit();

	main()
