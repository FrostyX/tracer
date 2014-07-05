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
	def message(self): return _("unsupported_distro")

	def __init__(self, distro):
		OSError.__init__(self, self.message.format(distro, __version__))


# @TODO Figure out why this import can't be above UnsupportedDistribution class
from tracer.resources.system import distribution

class PathNotFound(OSError):

	@property
	def message(self): return _("path_not_found")

	def __init__(self, name):
		OSError.__init__(self, self.message.format(name, distribution()))
