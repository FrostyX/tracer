#-*- coding: utf-8 -*-
"""Module to work with yum package manager class
Copyright 2013 Jakub Kadlčík"""

from os import listdir
from ipackageManager import IPackageManager

class Yum(IPackageManager):

	def packages_newer_than(self, unix_time):
		return 0

	def is_from(self, pkg_name, file_name):
		return 0

	def _transactions_newer_than(self, unix_time):
		"""Returns list of transactions which ran between unix_time and present"""
		return 0

	def _package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		return 0

	def _database_file(self):
		"""Returns path to yum history database file"""
		history_path = '/var/lib/yum/history/'
		return history_path + os.listdir(history_path)[-1]
