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
import textwrap
from resources.tracer import Tracer
from resources.args_parser import args
from resources.package import Package
from resources.exceptions import UnsupportedDistribution
from resources.applications import Applications
import resources.memory as Memory


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

		processes = tracer.trace_running()
		if not processes: return
		if args.interactive: _print_all_interactive(processes)
		else: _print_all(processes)

	except UnsupportedDistribution as ex:
		print ex

def _print_all(processes):
	without_static = _exclude_type(processes, Applications.TYPES["STATIC"])
	without_session = _exclude_type(without_static, Applications.TYPES["SESSION"])
	for process in without_session:
		print process.name

	static_count = len(processes)-len(without_static)
	session_count = len(without_static)-len(without_session)
	_print_note_for_hidden(session_count, static_count)

def _print_all_interactive(processes):
	processes = list(processes) # Cause Set is not ordered
	without_static = _exclude_type(processes, Applications.TYPES["STATIC"])
	without_session = _exclude_type(without_static, Applications.TYPES["SESSION"])
	static_count = len(processes)-len(without_static)
	session_count = len(without_static)-len(without_session)
	while True:
		i = 1
		l = len(str(len(without_session))) # Number of digits in processes length
		for process in without_session:
			n = "[{0}]".format(i).ljust(l + 2)
			print "{} {}".format(n, process.name)
			i += 1
		_print_note_for_hidden(session_count, static_count)

		print "\nPress application number for help or 'q' to quit"
		answer = raw_input("--> ")
		try:
			if answer == "q": return
			elif int(answer) <= 0 or int(answer) > i: raise IndexError
			print_helper(without_session[int(answer) - 1].name)

		except (SyntaxError, IndexError, ValueError):
			print "Wrong application number"

		raw_input("-- Press enter to get list of applications --")

def _exclude_type(processes, app_type):
	"""app_type -- see Applications.TYPES"""
	without = []
	for process in processes:
		app = Applications.find(process.name)
		if app["type"] != app_type:
			without.append(process)
	return without

def _print_note_for_hidden(session_count, static_count):
	if not args.quiet and (session_count > 0 or static_count > 0):
		print "\nPlease note that there are:"
		if session_count > 0:
			print "  - {0} processes requiring restarting your session (i.e. Logging out & Logging in again)".format(session_count)

		if static_count > 0:
			print "  - {0} processes requiring reboot".format(static_count)

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

		print textwrap.dedent("""\
			* {app_name}
			    Package:     {pkg_name}
			    Description: {pkg_description}
			    Type:        {type}
			    State:       {app_name} has been started by {user} {time} ago. PID - {pid}

			    How to restart:
					 {how_to_restart}
		""".format(
				app_name = app_name,
				pkg_name = package.name,
				type = app["type"].capitalize(),
				pkg_description = package.description,
				user = process.username,
				time = started_str,
				pid = process.pid,
				how_to_restart = "Sorry, It's not known",
			))

	except AttributeError:
		print "Application called %s is not running" % app_name




if __name__ == '__main__':
	if args.helper:
		print_helper(args.helper[0])
		sys.exit()

	if os.getuid() != 0:
		print "Only root can use this application"
		sys.exit();

	main()
