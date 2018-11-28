#-*- coding: utf-8 -*-
# dnf.py
# Module to work with DNF package manager class
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

import os.path

from tracer.resources.system import System
if System.distribution() in ["fedora", "mageia"]:

	import subprocess
	from tracer.packageManagers.rpm import Rpm

	class Dnf(Rpm):

		def __init__(self, **kwargs):
			super(Dnf, self).__init__(**kwargs)
			if os.path.exists('/var/lib/dnf/history.sqlite'):
				self.opts['modern_swdb'] = True

		@property
		def history_path(self):
			if self.opts.get('modern_swdb'):
				return '/var/lib/dnf/history.sqlite'
			return '/var/lib/dnf/history/'

		def package_files(self, pkg_name):
			if self._is_installed(pkg_name):
				return super(Dnf, self).package_files(pkg_name)

			if "erased" not in self.opts or not self.opts["erased"]:
				return []

			process = subprocess.Popen(["dnf", "repoquery", "-q", "-l", pkg_name], stdout=subprocess.PIPE)
			out = process.communicate()[0]
			return out.decode().split("\n")
