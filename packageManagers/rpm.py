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

from os import listdir
from ipackageManager import IPackageManager
from resources.package import Package
import sqlite3
import subprocess
import re

class Rpm(IPackageManager):

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

		packages = []
		sqlite = self._database_file()
		conn = sqlite3.connect(sqlite)
		conn.row_factory = sqlite3.Row
		c = conn.cursor()

		for t in self._transactions_newer_than(unix_time):
			c.execute(sql, [t['tid']])
			for p in c.fetchall():
				packages.append(Package(p['name'], t['end']))

		return packages

	def package_files(self, pkg_name):
		"""
		Returns list of files provided by package
		See also: http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch04s02s03.html
		"""

		p = subprocess.Popen(['rpm', '-ql', pkg_name], stdout=subprocess.PIPE)
		files, err = p.communicate()
		return files.split('\n')[:-1]

	def provided_by(self, app_name):
		"""Returns name of package which provides given application"""
		p = subprocess.Popen(['which', app_name], stdout=subprocess.PIPE)
		which, err = p.communicate()
		which = which.split('\n')[0]

		p = subprocess.Popen(['rpm', '-qf', which], stdout=subprocess.PIPE)
		pkg_name, err = p.communicate()
		pkg_name = package.split('\n')[0]

		return self._pkg_name_without_version(pkg_name)

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
		c = conn.cursor()
		c.execute(sql, [unix_time])
		return c.fetchall()

	def _database_file(self):
		"""
		Returns path to yum history database file
		Requires root permissions.
		"""

		for file in listdir(self.history_path):
			if file.startswith("history-") and file.endswith(".sqlite"):
				return self.history_path + file

