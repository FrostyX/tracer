#-*- coding: utf-8 -*-
"""This class should be inherited by any other package manager
Copyright 2013 Jakub Kadlčík"""

class IPackageManager:
	def packages_newer_than(self, unix_time):
		"""Returns list of packages which were modified between unix_time and present"""
		raise NotImplementedError

	def package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		raise NotImplementedError
