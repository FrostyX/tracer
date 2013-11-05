#-*- coding: utf-8 -*-
"""This class should be inherited by any other package manager
Copyright 2013 Jakub Kadlčík"""

class IPackageManager:
	def packages_newer_than(self, unix_time):
		"""Returns list of packages which were modified between unix_time and present"""
		raise NotImplementedError

	def is_from(self, pkg_name, file_name):
		"""Predicates if file is provided by package"""
		raise NotImplementedError
