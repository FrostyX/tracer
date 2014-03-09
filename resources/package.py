# -*- coding: utf-8 -*-

class Package:
	"""
	Represents single package
	Copyright 2013 Jakub Kadlčík
	"""

	_name = None
	_modified = None

	def __init__(self, name, modified=None):
		self._name = name
		self._modified = modified

	def __eq__(self, package):
		"""Packages are equal when they have same name"""
		return (isinstance(package, self.__class__)
			and self._name == package._name)

	def __ne__(self, package):
		return not self.__eq__(package)

	def __repr__(self):
		return "<Package:" + self._name + ">"

	def __str__(self):
		return self._name

	def __hash__(self):
		return hash(id(self))

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
		self._name = name

	@property
	def modified(self):
		return self._modified

	@modified.setter
	def modified(self, name):
		self._modified = modified
