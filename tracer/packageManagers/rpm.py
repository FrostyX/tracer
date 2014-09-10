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

from os import listdir
from .ipackageManager import IPackageManager
from tracer.resources.package import Package
from tracer.resources.exceptions import LockedDatabase, DatabasePermissions
import tracer.resources.memory as Memory
import sqlite3
import subprocess
import rpm
import os


class Rpm(IPackageManager):

	"""
	Package manager class - RPM
	"""

	# noinspection PyMissingConstructor
	def __init__(self):
		pass

	@property
	def history_path(self): return NotImplemented

	def packages_newer_than(self, unix_time):
		"""
		Returns list of packages which were modified between unix_time and present
		Requires root permissions.
		"""

		sql = """
			SELECT pkgtups.name
			FROM trans_data_pkgs JOIN pkgtups ON trans_data_pkgs.pkgtupid=pkgtups.pkgtupid
			WHERE trans_data_pkgs.tid = ?
			ORDER BY pkgtups.pkgtupid
		"""

		try:
			packages = []
			sqlite = self._database_file()
			conn = sqlite3.connect(sqlite)
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()

			for tran in self._transactions_newer_than(unix_time):
				cursor.execute(sql, [tran['tid']])
				for pkg in cursor.fetchall():
					packages.append(Package(pkg['name'], tran['end']))

			return packages

		except sqlite3.OperationalError as e:
			raise LockedDatabase() if e.message == 'database is locked' else DatabasePermissions()

	def package_files(self, pkg_name):
		"""
		Returns list of files provided by package
		See also: http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch04s02s03.html
		"""
		if self._is_installed(pkg_name):
			process = subprocess.Popen(['rpm', '-ql', pkg_name], stdout=subprocess.PIPE)
			files = process.communicate()[0]
			return files.split('\n')[:-1]
		return []

	def package_info(self, app_name):
		"""Returns package object with all attributes"""
		description = None
		category = None
		name = self.provided_by(app_name)
		if not name:
			return None

		process = subprocess.Popen(['rpm', '-qi', name], stdout=subprocess.PIPE)
		out = process.communicate()[0]
		out = out.split('\n')

		for line in out:
			if line.startswith("Summary"):
				description = line.split("Summary     :")[1].strip()

			if line.startswith("Group"):
				category = line.split("Group       :")[1].strip()

		package = Package(name)
		package.description = description
		package.category = category
		return package

	def provided_by(self, app_name):
		"""Returns name of package which provides given application"""
		# `rpm -qf ...` needs full path to binary, not only its name
		process = Memory.process_by_name(app_name)
		package = self._file_provided_by(process.exe)
		if package:
			# If package is interpreter, return the package providing that interpreted file
			if package.category == 'Development/Languages':
				for arg in process.cmdline[1:]:
					if os.path.isfile(arg):
						package = self._file_provided_by(arg)
						return package.name if package else None
			return package.name
		return None

	def _file_provided_by(self, file):
		"""Returns name of package which provides given file"""
		command = ['rpm', '-qf', file, "--queryformat", "%{NAME}"]
		process = subprocess.Popen(command, stdout=subprocess.PIPE)
		pkg_name = process.communicate()[0]

		# File is not provided by any package
		if len(pkg_name.split(" ")) > 1:
			return None

		p = Package(pkg_name)
		p.category = self._package_category(pkg_name)
		return p

	def _package_category(self, pkg_name):
		"""Returns category of given package name; @TODO Use package_info as soon as possible"""
		process = subprocess.Popen(['rpm', '-qi', pkg_name], stdout=subprocess.PIPE)
		out = process.communicate()[0]
		out = out.split('\n')

		for line in out:
			if line.startswith("Group"):
				return line.split("Group       :")[1].strip()
		return None

	def _transactions_newer_than(self, unix_time):
		"""
		Returns list of transactions which ran between unix_time and present.
		Requires root permissions.
		"""

		sql = """
			SELECT trans_beg.tid, trans_beg.timestamp AS beg, trans_end.timestamp AS end
			FROM trans_beg JOIN trans_end ON trans_beg.tid=trans_end.tid
			WHERE beg > ?
			ORDER BY trans_beg.tid
		"""

		sqlite = self._database_file()
		conn = sqlite3.connect(sqlite)
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute(sql, [unix_time])
		return cursor.fetchall()

	def _database_file(self):
		"""
		Returns path to yum history database file
		Requires root permissions.
		"""

		for file in listdir(self.history_path):
			if file.startswith("history-") and file.endswith(".sqlite"):
				return self.history_path + file


	@staticmethod
	def _is_installed(pkg_name):
		"""Returns True if package is installed"""

		ts = rpm.TransactionSet()
		mi = ts.dbMatch('name', pkg_name)
		return True if len(mi) > 0 else False
