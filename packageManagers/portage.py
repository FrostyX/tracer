#-*- coding: utf-8 -*-
# portage.py
# Module to work with portage package manager class
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
import resources.memory as Memory
import subprocess
import time
import os

class Portage(IPackageManager):

	def packages_newer_than(self, unix_time):
		"""
		Returns list of packages which were modified between unix_time and present
		Requires root permissions.
		"""
		newer = []
		p = subprocess.Popen(['qlop', '-lC'], stdout=subprocess.PIPE)
		packages, err = p.communicate()
		for package in packages.split('\n')[:-1]:
			package = package.split(" >>> ")

			# There actually should be %e instead of %d
			modified = time.mktime(time.strptime(package[0], "%a %b %d %H:%M:%S %Y"))
			if modified >= unix_time:
				pkg_name = package[1] # Package name with version, let's cut it off
				pkg_name = self._pkg_name_without_version(pkg_name)
				newer.append(Package(pkg_name, modified))

		return newer

	def package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		FNULL = open(os.devnull, 'w')
		p = subprocess.Popen(['equery', '-q', 'f', pkg_name], stdout=subprocess.PIPE, stderr=FNULL)
		files, err = p.communicate()
		return files.split('\n')[:-1]

	def package_info(self, app_name):
		"""Returns package object with all attributes"""
		name = self.provided_by(app_name)

		p = subprocess.Popen(['eix', '-e', name], stdout=subprocess.PIPE)
		out, err = p.communicate()
		out = out.split('\n')
		description = out[4].split("Description:")[1].strip()

		package = Package(name)
		package.description = description
		return package

	def provided_by(self, app_name):
		"""Returns name of package which provides given application"""
		process = Memory.process_by_name(app_name)
		f = process.cmdline[0]

		p = subprocess.Popen(['equery', '-q', 'b', f], stdout=subprocess.PIPE)
		pkg_name, err = p.communicate()
		pkg_name = pkg_name.split('\n')[0]

		return self._pkg_name_without_version(pkg_name)
