#-*- coding: utf-8 -*-
# exceptions.py
# Tracer exceptions module
#
# Copyright (C) 2014 Jakub Kadlčík
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

from tracer.version import __version__
from tracer.resources.lang import _


class UnsupportedDistribution(OSError):

	@property
	def message(self):
		return _(
			"You are running unsupported linux distribution\n"
			"\n"
			"Please visit https://github.com/FrostyX/tracer/issues\n"
			"and create new issue called 'Unknown or unsupported linux distribution: {0} (v{1})' if there isn't such.\n"
			"\n"
			"Don't you have an GitHub account? Please report this issue on frostyx@email.cz")

	def __init__(self, distro):
		OSError.__init__(self, self.message.format(distro, __version__))


class LockedDatabase(OSError):

	@property
	def message(self):
		return _("Package database is locked by another process")

	def __init__(self):
		OSError.__init__(self, self.message)


class DatabasePermissions(OSError):

	@property
	def message(self):
		return _("You can't open package database due to insufficient permissions")

	def __init__(self):
		OSError.__init__(self, self.message)


class PathNotFound(OSError):

	@property
	def message(self):
		return _(
			"Problem occurred - neither one of {0} paths doesn't exist\n"
			"Please contact maintainer of tracer package in your distribution.")

	def __init__(self, name):
		OSError.__init__(self, self.message.format(name))
