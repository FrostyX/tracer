#-*- coding: utf-8 -*-
"""Module to work with yum package manager class
Copyright 2013 Jakub Kadlčík"""

from ipackageManager import IPackageManager

class Yum(IPackageManager):

	def packages_newer_than(self, unix_time):
		return 0

	def is_from(self, pkg_name, file_name):
		return 0

	def _transactions_newer_than(self, unix_time):
		"""Returns list of transactions which were modified between unix_time and present"""
		return 0

	def _package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		return 0
