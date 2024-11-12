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
if System.distribution() in ["rhel", "fedora", "centos", "centos-7", "mageia", "suse", "ol"]:

	import subprocess
	from tracer.packageManagers.rpm import Rpm
	from tracer.resources.package import Package
	from tracer.resources.collections import PackagesCollection

	class Dnf(Rpm):

		def __init__(self, **kwargs):
			super(Dnf, self).__init__(**kwargs)
			if os.path.exists('/usr/lib/sysimage/dnf/history.sqlite'):
				self.opts['sysimage_persistdir'] = True
			if os.path.exists('/usr/lib/sysimage/dnf/history.sqlite') or os.path.exists('/var/lib/dnf/history.sqlite'):
				self.opts['modern_swdb'] = True

		@property
		def history_path(self):
			if self.opts.get('modern_swdb'):
				if self.opts.get('sysimage_persistdir'):
					return '/usr/lib/sysimage/dnf/history.sqlite'
				else:
					return '/var/lib/dnf/history.sqlite'
			if self.opts.get('sysimage_persistdir'):
				return '/usr/lib/sysimage/dnf/history/'
			else:
				return '/var/lib/dnf/history/'

		def package_files(self, pkg_name):
			if not self.opts.get("erased"):
				return super(Dnf, self).package_files(pkg_name)

			# TODO Running an external command is tooooo slow, use python API instead
			process = subprocess.Popen(["dnf", "repoquery", "-q", "-l", pkg_name], stdout=subprocess.PIPE)
			out = process.communicate()[0]
			return out.decode().split("\n")


	class FakeDnf5(Dnf):
		def packages_newer_than(self, unix_time):
			return []

		def package_files(self, pkg_name):
			return []


	class Dnf5(Dnf):
		def __new__(cls, *args, **kwargs):
			"""
			We are going to enable DNF5 on all Fedora, EPEL, Mageia, openSUSE,
			etc systems and not all of them may have DNF5 (yet).
			"""
			try:
				import libdnf5
				return super().__new__(cls)
			except ImportError:
				return FakeDnf5(*args, **kwargs)

		def packages_newer_than(self, unix_time):
			import libdnf5
			base = libdnf5.base.Base()
			base.setup()

			# Package names as a keys and timestamps as values
			packages = {}

			history = base.get_transaction_history()
			for transaction in history.list_all_transactions():
				if transaction.get_dt_start() < unix_time:
					continue
				for package in transaction.get_packages():
					packages[package.get_name()] = transaction.get_dt_start()

			collection = PackagesCollection()
			for name, timestamp in packages.items():
				collection.append(Package(name, timestamp))

			return collection

		def package_files(self, pkg_name):
			if not self.opts.get("erased"):
				return super(Dnf, self).package_files(pkg_name)

			import libdnf5
			base = libdnf5.base.Base()
			base.setup()

			repo_sack = base.get_repo_sack()
			if hasattr(repo_sack, "load_repos"):
				# On F41+, this is what should be done
				repo_sack.load_repos()
			else:
				# On F40 there is only python3-libdnf5-5.1.17 so we have to use
				# this now-deprecated function
				repo_sack.update_and_load_enabled_repos(True)

			query = libdnf5.rpm.PackageQuery(base)
			query.filter_name([pkg_name])
			paths = []
			for pkg in query:
				paths.extend(pkg.get_files())
			return paths
