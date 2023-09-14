#-*- coding: utf-8 -*-
# rpm.py
# Base RPM package manager class
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
if System.distribution() in ["fedora", "rhel", "centos", "centos-7", "mageia", "ol"]:

	from os import listdir
	from .ipackageManager import IPackageManager
	from tracer.resources.package import Package
	from tracer.resources.collections import PackagesCollection
	from tracer.resources.exceptions import LockedDatabase, DatabasePermissions
	from tracer.resources.pycomp import PY3
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

			if self.opts.get('modern_swdb'):
				sql = """
					SELECT DISTINCT rpm.name, trans.dt_end AS end

					FROM trans JOIN trans_item JOIN rpm
					ON trans.id=trans_item.trans_id
					AND trans_item.item_id=rpm.item_id

					WHERE trans.dt_begin > ?
					ORDER BY rpm.name
				"""
			else:
				sql = """
					SELECT DISTINCT pkgtups.name, trans_end.timestamp AS end

					FROM trans_beg JOIN trans_end JOIN trans_data_pkgs JOIN pkgtups
					ON trans_beg.tid=trans_end.tid
					AND trans_data_pkgs.tid=trans_beg.tid
					AND trans_data_pkgs.pkgtupid=pkgtups.pkgtupid

					WHERE trans_beg.timestamp > ?
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
				raise LockedDatabase() if str(e) == 'database is locked' else DatabasePermissions()

		def package_files(self, pkg_name):
			"""
			Returns list of files provided by package
			See also: http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch04s02s03.html
			"""
			ts = rpm.TransactionSet()
			mi = ts.dbMatch("name", pkg_name)
			packages = list(mi)

			# Tracer will not find uninstalled applications
			if not packages:
				return []

			if PY3:
				files = rpm.files(packages[0])
				return [x.name for x in files]
			else:
				files = rpm.fi(packages[0])
				return [f[0] for f in files]

		def find_package(self, name, evra):
			evra = self._splitEvra(evra)
			ts = rpm.TransactionSet()
			mi = ts.dbMatch("name", name)

			for hdr in mi:
				if hdr[rpm.RPMTAG_EPOCH] == evra[0] and hdr[rpm.RPMTAG_VERSION] == evra[1] and hdr[rpm.RPMTAG_RELEASE] == evra[2] and hdr[rpm.RPMTAG_ARCH] == evra[3]:
					package = Package(name)
					self._load_package_info_from_hdr(package, hdr)

					return package

			return None

		def load_package_info(self, package):
			"""From database load informations about given package and set them to it"""
			if not package:
				return None

			ts = rpm.TransactionSet()
			mi = ts.dbMatch("name", package.name)

			""" Find the latest one if there are multiple versions"""
			latest = None
			for hdr in mi:
				if latest is None:
					latest = hdr
				else:
					compare = rpm.labelCompare((str(latest[rpm.RPMTAG_EPOCH]), str(latest[rpm.RPMTAG_VERSION]), str(latest[rpm.RPMTAG_RELEASE])),
						(str(hdr[rpm.RPMTAG_EPOCH]), str(hdr[rpm.RPMTAG_VERSION]), str(hdr[rpm.RPMTAG_RELEASE])))

					if compare == -1:
						latest = hdr

			if latest is None:
				return

			self._load_package_info_from_hdr(package, latest)

		def compare_packages(self, p1, p2):
			"""
			labelCompare returns:
			0 if the EVR matches
			1 if EVR(1) > EVR(2)
			-1 if EVR(2) > EVR(1)
			"""
			return rpm.labelCompare((str(p1.epoch), str(p1.version), str(p1.release)), (str(p2.epoch), str(p2.version), str(p2.release)))

		def provided_by(self, app):
			"""Returns name of package which provides given application"""
			# `rpm -qf ...` needs full path to binary, not only its name
			process = app.instances[0]  # @TODO Reimplement for all processes
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

		def _splitEvra(self, evra):
			"""
			Derived from rpmUtils.miscutils.splitFilename
			https://github.com/rpm-software-management/yum/blob/master/rpmUtils/miscutils.py

			Given: 9-123a.ia64
			Return: (9, 123a, 1, ia64)
			"""

			archIndex = evra.rfind('.')
			arch = evra[archIndex + 1:]

			relIndex = evra[:archIndex].rfind('-')
			rel = evra[relIndex + 1:archIndex]

			verIndex = evra[:relIndex].rfind('-')
			ver = evra[verIndex + 1:relIndex]

			epochIndex = evra.find(':')
			if epochIndex == -1:
				epoch = None
			else:
				epoch = evra[:epochIndex]

			return epoch, ver, rel, arch

		def _load_package_info_from_hdr(self, package, hdr):
			package.description = hdr[rpm.RPMTAG_SUMMARY]
			package.category = hdr[rpm.RPMTAG_GROUP]

			epoch = hdr[rpm.RPMTAG_EPOCH]
			if epoch:
				package.epoch = epoch

			package.version = hdr[rpm.RPMTAG_VERSION]
			package.release = hdr[rpm.RPMTAG_RELEASE]

		def _file_provided_by(self, file):
			"""Returns name of package which provides given file"""
			ts = rpm.TransactionSet()
			db = ts.dbMatch("basenames", file)
			if db.count() == 0:
				return None

			pkg = next(db)
			p = Package(pkg[rpm.RPMTAG_NAME])
			p.category = pkg[rpm.RPMTAG_GROUP]
			return p

		def _database_file(self):
			"""Returns path to yum history database file"""
			if self.opts.get('modern_swdb'):
				return self.history_path
			for file in sorted(listdir(self.history_path), reverse=True):
				if file.startswith("history-") and file.endswith(".sqlite"):
					return self.history_path + file
