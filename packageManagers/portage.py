#-*- coding: utf-8 -*-
"""Module to work with portage package manager class
Copyright 2013 Jakub Kadlčík"""

from ipackageManager import IPackageManager
import subprocess
import time

class Portage(IPackageManager):

	def packages_newer_than(self, unix_time):
		"""
		Returns list of packages which were modified between unix_time and present
		Requires root permissions.
		"""
		newer = []
		p = subprocess.Popen(['qlop', '-lC'], stdout=subprocess.PIPE)
		packages, err = p.communicate()
		for package in packages.split('\n')[:-1]:
			package = package.split(" >>> ")

			# There actually should be %e instead of %d
			modified = time.mktime(time.strptime(package[0], "%a %b %d %H:%M:%S %Y"))
			if modified >= unix_time:
				pkg_name = package[1] # Package name with version, let's cut it off
				pkg_name = pkg_name[:pkg_name.index('.')]  # Cut from first . to end
				pkg_name = pkg_name[:pkg_name.rindex('-')] # Cut from last  - to end
				newer.append({"name":pkg_name, "modified":modified})
		return newer

	def package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		p = subprocess.Popen(['equery', '-q', 'f', pkg_name], stdout=subprocess.PIPE)
		files, err = p.communicate()
		return files.split('\n')[:-1]

