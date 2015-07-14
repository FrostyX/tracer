#-*- coding: utf-8 -*-
# rpm.py
# Base RPM package manager class
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

from __future__ import absolute_import


from tracer.resources.system import System
if System.distribution() in ["fedora", "centos"]:

	from os import listdir
	from .ipackageManager import IPackageManager
	from tracer.resources.package import Package
	from tracer.resources.collections import PackagesCollection
	from tracer.resources.exceptions import LockedDatabase, DatabasePermissions
	from tracer.resources.applications import Applications
	import sqlite3
	import rpm
	import os

	class Rpm(IPackageManager):

		"""
		Package manager class - RPM
		"""

		# noinspection PyMissingConstructor
		def __init__(self, **kwargs):
			self.opts = kwargs

		@property
		def history_path(self): return NotImplemented

		def packages_newer_than(self, unix_time):
			"""
			Returns list of packages which were modified between unix_time and present
			Requires root permissions.
			"""

			# Package manager wasn't used yet
			if not os.path.exists(self.history_path):
				return PackagesCollection([])

			sql = """
				SELECT DISTINCT pkgtups.name, trans_end.timestamp AS end

				FROM trans_beg JOIN trans_end JOIN trans_data_pkgs JOIN pkgtups
				ON trans_beg.tid=trans_end.tid
				AND trans_data_pkgs.tid=trans_beg.tid
				AND trans_data_pkgs.pkgtupid=pkgtups.pkgtupid

				WHERE  trans_beg.timestamp > ?
				ORDER BY pkgtups.name
			"""

			try:
				packages = PackagesCollection()
				sqlite = self._database_file()
				conn = sqlite3.connect(sqlite)
				conn.row_factory = sqlite3.Row
				cursor = conn.cursor()
				cursor.execute(sql, [unix_time])

				for result in cursor.fetchall():
					packages.append(Package(result['name'], result['end']))

				return packages

			except sqlite3.OperationalError as e:
				raise LockedDatabase() if e.message == 'database is locked' else DatabasePermissions()

		def package_files(self, pkg_name):
			"""
			Returns list of files provided by package
			See also: http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch04s02s03.html
			"""
			if self._is_installed(pkg_name):
				ts = rpm.TransactionSet()
				mi = ts.dbMatch("name", pkg_name)
				fi = rpm.fi(next(mi))
				return [f[0] for f in fi]

			# Tracer will not find uninstalled applications
			return []

		def load_package_info(self, package):
			"""From database load informations about given package and set them to it"""
			description = None
			category = None
			if not package:
				return None

			ts = rpm.TransactionSet()
			mi = ts.dbMatch("name", package.name)
			package_hdr = next(mi)
			package.description = package_hdr[rpm.RPMTAG_SUMMARY].decode()
			package.category = package_hdr[rpm.RPMTAG_GROUP].decode()

		def provided_by(self, app_name):
			"""Returns name of package which provides given application"""
			# `rpm -qf ...` needs full path to binary, not only its name
			process = Applications.find(app_name).instances[0]  # @TODO Reimplement for all processes
			package = self._file_provided_by(process.exe)
			if package:
				# If package is interpreter, return the package providing that interpreted file
				if package.category == 'Development/Languages':
					for arg in process.cmdline()[1:]:
						if os.path.isfile(arg):
							package = self._file_provided_by(arg)
							return package if package else None
				return package
			return None

		def _file_provided_by(self, file):
			"""Returns name of package which provides given file"""
			ts = rpm.TransactionSet()
			db = ts.dbMatch("basenames", file)
			if db.count() == 0:
				return None

			pkg = next(db)
			p = Package(pkg[rpm.RPMTAG_NAME].decode())
			p.category = pkg[rpm.RPMTAG_GROUP].decode()
			return p

		def _database_file(self):
			"""Returns path to yum history database file"""
			for file in sorted(listdir(self.history_path), reverse=True):
				if file.startswith("history-") and file.endswith(".sqlite"):
					return self.history_path + file

		@staticmethod
		def _is_installed(pkg_name):
			"""Returns True if package is installed"""

			ts = rpm.TransactionSet()
			mi = ts.dbMatch('name', pkg_name)
			return True if len(mi) > 0 else False
