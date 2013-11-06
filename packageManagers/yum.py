#-*- coding: utf-8 -*-
"""Module to work with yum package manager class
Copyright 2013 Jakub Kadlčík"""

from os import listdir
from ipackageManager import IPackageManager
import sqlite3

class Yum(IPackageManager):

	def packages_newer_than(self, unix_time):
		return 0

	def is_from(self, pkg_name, file_name):
		return 0

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

	def _package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		return 0

	def _database_file(self):
		"""
		Returns path to yum history database file
		Requires root permissions.
		"""
		history_path = '/var/lib/yum/history/'
		return history_path + listdir(history_path)[-1]
