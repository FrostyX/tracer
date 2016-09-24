#-*- coding: utf-8 -*-
# system.py
# Module for getting data about your operating system
# Dont worry, only necessary data required for this application.
# Tracer *will not* store, collect or send your data anywhere.
#
# Copyright (C) 2013 Jakub Kadlcik
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

# WARNING: There are imports in package_manager()
import os
import pwd
import importlib
import platform
import psutil
from sys import version_info
from tracer.resources.PackageManager import PackageManager
from tracer.resources.processes import Process


class System(object):

	@staticmethod
	def distribution():
		# Checks if /etc/os-release exists, and if it does,
		# use it to divine the name of the distribution
		# Otherwise, revert to using platform.linux_distribution()
		if os.path.isfile("/etc/os-release"):
			with open("/etc/os-release") as os_release_file:
				os_release_data = {}

				# Remove empty lines and trailing spaces
				lines = [line.rstrip() for line in os_release_file if line.rstrip()]
				for line in lines:
						os_release_key, os_release_value = line.split("=")
						os_release_data[os_release_key] = os_release_value.strip('"')
				return os_release_data["ID"]
		else:
			return platform.linux_distribution(full_distribution_name=False)[0]

	@staticmethod
	def package_manager(**kwargs):
		"""Returns instance of package manager according to installed linux distribution"""

		def get_instance(pair):
			# WARNING: Imports here
			path, name = pair
			module = importlib.import_module(path)
			return getattr(module, name)(**kwargs)

		managers = {
			"gentoo":  [("tracer.packageManagers.portage", "Portage")],
			"debian":  [("tracer.packageManagers.dpkg", "Dpkg")],
			"rhel":    [("tracer.packageManagers.yum", "Yum")],
			"centos":  [("tracer.packageManagers.yum", "Yum")],
			"mageia":  [("tracer.packageManagers.dnf", "Dnf")],
			"arch":    [("tracer.packageManagers.alpm", "Alpm")],
			"archarm": [("tracer.packageManagers.alpm", "Alpm")],
			"fedora":  [
				("tracer.packageManagers.dnf", "Dnf"),
				("tracer.packageManagers.yum", "Yum"),
			],
		}

		distro = System.distribution()
		if distro not in managers:
			return None

		return PackageManager(*list(map(get_instance, managers[distro])))

	@staticmethod
	def init_system():
		"""
		Returns name of init system you are using
		e.g. init, systemd, upstart
		"""

		init = Process(1)
		name = init.name().split(" ")[0]
		return name

	@staticmethod
	def boot_time():
		# psutil-2.x.x is not backward compatible to psutil-1.x.x
		try: return psutil.boot_time()
		except AttributeError: return psutil.get_boot_time()

	@staticmethod
	def python_version():
		return "{}.{}.{}".format(version_info.major, version_info.minor, version_info.micro)

	@staticmethod
	def user():
		# getlogin is prefered because it return current username even
		# if python process is executed with sudo
		try: return os.getlogin()
		except OSError: return pwd.getpwuid(os.getuid())[0]
