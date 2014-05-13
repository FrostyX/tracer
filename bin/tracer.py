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
from resources.lang import _
from resources.tracer import Tracer
from resources.args_parser import args
from resources.package import Package
from resources.exceptions import UnsupportedDistribution
from resources.applications import Applications
import resources.memory as Memory
import resources.system as System


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

		print "\n" + _("prompt_help")
		answer = raw_input("--> ")
		try:
			if answer == "q": return
			elif int(answer) <= 0 or int(answer) > i: raise IndexError
			print_helper(without_session[int(answer) - 1].name)

		except (SyntaxError, IndexError, ValueError):
			print _("wrong_app_number")

		raw_input(_("press_enter"))

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
		print "\n" + _("note_unlisted_apps")
		if session_count > 0:
			print _("requiring_session").format(session_count)

		if static_count > 0:
			print _("requiring_reboot").format(static_count)

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

		how_to_restart = _("not_known_restart")
		if app["type"] == Applications.TYPES["DAEMON"]:
			init = System.init_system()
			if init == "systemd": how_to_restart = "systemctl restart {0}".format(app["name"])
			elif init == "init": how_to_restart = "/etc/init.d/{0} restart".format(app["name"])

		print _("helper").format(
			app_name = app_name,
			pkg_name = package.name,
			type = app["type"].capitalize(),
			pkg_description = package.description,
			user = process.username,
			time = started_str,
			pid = process.pid,
			how_to_restart = how_to_restart,
		)

	except AttributeError:
		print _("app_not_running").format(app_name)



if __name__ == '__main__':
	if args.helper:
		print_helper(args.helper[0])
		sys.exit()

	if os.getuid() != 0:
		print _("root_only")
		sys.exit();

	main()
