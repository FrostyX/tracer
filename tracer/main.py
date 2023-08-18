#-*- coding: utf-8 -*-
# main.py
# Tracer finds outdated running applications in your system
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

from __future__ import print_function

import os
import sys
import time
from tracer.resources.router import Router
from tracer.resources.args_parser import parser
from tracer.resources.package import Package
from tracer.resources.exceptions import (
	TracerError,
	UnsupportedDistribution,
	PathNotFound,
	LockedDatabase,
	DatabasePermissions,
)
from tracer.resources.lang import _


def run():
	args = parser.parse_args()

	# If there is something on stdin (that means piped into tracer)
	stdin_packages = []
	if not sys.stdin.isatty() and "SSH_CONNECTION" not in os.environ:
		stdin_packages = sys.stdin.readline().split()

	# All input packages enchanced by actual time (as modified time)
	packages = []
	for package in args.packages + args.pkgs + stdin_packages:
		packages.append(Package(package, time.time() if args.now else None))

	try:
		router = Router(args, packages)
		return router.dispatch()

	except (UnsupportedDistribution, PathNotFound, LockedDatabase) as ex:
		ex.print()
		exit(1)
	except DatabasePermissions as ex:
		ex.print()
		print(_("You will probably need to run tracer as root"))
		exit(1)
	except TracerError as ex:
		ex.print()
		exit(1)
	except (KeyboardInterrupt, EOFError):
		print("")
