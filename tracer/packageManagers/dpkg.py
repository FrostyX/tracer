#-*- coding: utf-8 -*-
# dpkg.py
# Module to work with dpkg based package managers
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


from tracer.resources.system import System
if System.distribution() == "debian":

	from .ipackageManager import IPackageManager
	from tracer.resources.package import Package
	from tracer.resources.collections import PackagesCollection
	import subprocess
	import time
	import os

	class Dpkg(IPackageManager):

		"""
		Package manager class - DPKG
		"""

		# noinspection PyMissingConstructor
		def __init__(self, **kwargs):
			self.opts = kwargs

		@property
		def dpkg_log(self): return '/var/log/dpkg.log'

		def packages_newer_than(self, unix_time):
			"""
			Returns list of packages which were modified between unix_time and present
			Requires root permissions.
			"""
			newer = PackagesCollection()
			log = open(self.dpkg_log, 'r')
			for line in log:
				line = line.split(" ")

				if line[2] != "upgrade":
					continue

				# There actually should be %e instead of %d
				modified = time.mktime(
					time.strptime(line[0] + " " + line[1],
					"%Y-%m-%d %H:%M:%S"))

				if modified >= unix_time:
					pkg_name = line[3].split(":")[0]
					newer.append(Package(pkg_name, modified))
			return newer

		def package_files(self, pkg_name):
			"""Returns list of files provided by package"""
			files = []
			fnull = open(os.devnull, 'w')
			command = ['dpkg-query', '-L', pkg_name]
			process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=fnull)
			out = process.communicate()[0]
			for file in out.decode().split('\n')[:-1]:
				if os.path.isfile(file):
					files.append(file)
			return files

		def load_package_info(self, package):
			"""From database load informations about given package and set them to it"""
			description = None

			process = subprocess.Popen(['dpkg', '-s', package.name], stdout=subprocess.PIPE)
			out = process.communicate()[0]
			out = out.decode().split('\n')

			for line in out:
				if line.startswith("Description:"):
					description = line.split("Description:")[1].strip()

			package.description = description

		def provided_by(self, app):
			"""Returns name of package which provides given application"""
			command = ['dlocate', '-S', app.name]
			process = subprocess.Popen(command, stdout=subprocess.PIPE)
			pkg_name = process.communicate()[0]
			pkg_name = pkg_name.decode().split('\n')[0]
			return Package(pkg_name.split(':')[0])
