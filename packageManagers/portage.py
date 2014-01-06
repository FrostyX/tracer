#-*- coding: utf-8 -*-
"""Module to work with portage package manager class
Copyright 2013 Jakub Kadlčík"""

#from os import listdir
from ipackageManager import IPackageManager
import commands
import time

class Portage(IPackageManager):

	def packages_newer_than(self, unix_time):
		"""
		Returns list of packages which were modified between unix_time and present
		Requires root permissions.
		"""
		newer = []
		packages = commands.getoutput('sudo qlop -lC').split('\n')
		for package in packages:
			package = package.split(" >>> ")

			# There actually should be %e instead of %d
			modified = time.mktime(time.strptime(package[0], "%a %b %d %H:%M:%S %Y"))
			if modified >= unix_time:
				pkg_name = package[1]
				pkg_name = pkg_name[:pkg_name.index('.')]  # Cut from first . to end
				pkg_name = pkg_name[:pkg_name.rindex('-')] # Cut from last  - to end
				newer.append({"name":pkg_name})
		return newer

	def is_from(self, pkg_name, file_name):
		"""Predicates if file is provided by package"""
		raise NotImplementedError


	def _package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		return commands.getoutput('equery -q f ' + pkg_name).split('\n')

