#-*- coding: utf-8 -*-
# dpkg.py
# Module to work with dpkg based package managers
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

from ipackageManager import IPackageManager
from resources.package import Package
import subprocess
import time
import os

class Dpkg(IPackageManager):

	@property
	def dpkg_log(self): return '/var/log/dpkg.log'

	def packages_newer_than(self, unix_time):
		"""
		Returns list of packages which were modified between unix_time and present
		Requires root permissions.
		"""
		newer = []
		log = open(self.dpkg_log, 'r')
		for line in log:
			line = line.split(" ")

			if line[2] != "upgrade":
				continue

			# There actually should be %e instead of %d
			modified = time.mktime(time.strptime(line[0] + " " + line[1], "%Y-%m-%d %H:%M:%S"))
			if modified >= unix_time:
				pkg_name = line[3].split(":")[0]
				newer.append(Package(pkg_name, modified))
		return newer

	def package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		files = []
		FNULL = open(os.devnull, 'w')
		p = subprocess.Popen(['dpkg-query', '-L', pkg_name], stdout=subprocess.PIPE, stderr=FNULL)
		out, err = p.communicate()
		for file in out.split('\n')[:-1]:
			if os.path.isfile(file):
				files.append(file)
		return files
