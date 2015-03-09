#-*- coding: utf-8 -*-
# applications.py
# Manager for applications file
#
# Copyright (C) 2014 Jakub Kadlčík
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

from bs4 import BeautifulSoup, element
from tracer.paths import DATA_DIR, USER_CONFIG_DIRS
from tracer.resources.exceptions import PathNotFound
from tracer.resources.collections import ApplicationsCollection
from tracer.resources.lang import _
from tracer.resources.processes import Processes
import os
import re


class Applications(object):

	DEFINITIONS = map(lambda x: x + "/applications.xml", [DATA_DIR] + USER_CONFIG_DIRS)

	TYPES = {
		"DAEMON"       :  "daemon",
		"STATIC"       :  "static",
		"SESSION"      :  "session",
		"APPLICATION"  :  "application"
	}
	DEFAULT_TYPE = TYPES["APPLICATION"]
	_apps = None

	@staticmethod
	def find(app_name):
		if not Applications._apps:
			Applications._load_definitions()

		for app in Applications._apps:
			if app.name == app_name:
				return app

		# Return the default application
		return Application({"name" : app_name, "type" : Applications.DEFAULT_TYPE, "helper" : None, "ignore" : False})

	@staticmethod
	def all():
		if not Applications._apps:
			Applications._load_definitions()

		return Applications._apps

	@staticmethod
	def _load_definitions():
		Applications._apps = ApplicationsCollection()
		for file in Applications.DEFINITIONS:
			try: Applications._load(file)
			except PathNotFound as ex:
				if not os.path.dirname(file) in USER_CONFIG_DIRS:
					raise ex

	@staticmethod
	def _load(file):
		try:
			f = open(file)
			soup = BeautifulSoup(f.read())

			for child in soup.applications.children:
				if not isinstance(child, element.Tag):
					continue

				if child.name == "app":
					Applications._append_application(child.attrs)

				if child.name == "group":
					for app in child.findChildren():
						Applications._append_application(app.attrs, child.attrs)
			f.close()

		except IOError:
			raise PathNotFound('DATA_DIR')

	@staticmethod
	def _append_application(default_attrs, specific_attrs={}):
		application = Application(default_attrs)
		application.update(specific_attrs)
		if application in Applications._apps:
			i = Applications._apps.index(application)
			Applications._apps[i].update(application)
		else:
			application.setdefault('type', Applications.DEFAULT_TYPE)
			application.setdefault('helper', Applications._helper(application))
			application.setdefault('ignore', False)
			Applications._apps.append(application)

	@staticmethod
	def _helper(app):
		if app.type == Applications.TYPES["DAEMON"]:
			return "service {0} restart".format(app.name)

		elif app.type == Applications.TYPES["STATIC"]:
			return _("static_restart")

		elif app.type == Applications.TYPES["SESSION"]:
			return _("session_restart")

		return None


class Application:

	"""
	Represent the application defined in ``applications.xml``

	:param str name: The name of the application
	:param str type: See ``Applications.TYPES`` for possible values
	:param str helper: Describes how to restart the applications
	:param bool ignore: If ``True``, the application won't be printed
	:param Processes processes_factory: Class providing list of running processes

	"""

	processes_factory = Processes
	_attributes = None

	def __init__(self, attributes_dict):
		self._attributes = attributes_dict

	def __eq__(self, other):
		return isinstance(other, Application) and self.name == other.name

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.name)

	def __getattr__(self, item):
		return self._attributes[item]

	def __len__(self):
		return len(self._attributes)

	def __contains__(self, item):
		return item in self._attributes

	def __str__(self):
		return "<Application: " + self._attributes["name"] + ">"

	def __repr__(self):
		return self.__str__()

	def setdefault(self, key, value):
		self._attributes.setdefault(key, value)

	def update(self, values):
		if isinstance(values, Application):
			values = values._attributes
		self._attributes.update(values)

	# @TODO rename to helper_format
	@property
	def helper(self):
		helper = self._attributes["helper"]
		if os.getlogin() != "root" and self.type == Applications.TYPES["DAEMON"]:
			if helper and not helper.startswith("sudo "):
				helper = "sudo " + helper
		return helper

	@property
	def helper_contains_formating(self):
		return bool(re.search("\{.*\}", self.helper))

	@property
	def helper_contains_name(self):
		return bool(re.search("\{NAME\}", self.helper))

	@property
	def helpers(self):
		"""
		Return the list of helpers which describes how to restart the application.
		When no ``helper_format`` was described, empty list will be returned.
		If ``helper_format`` contains process specific arguments such a ``{PID}``, etc.
		list will contain helper for every application instance.
		In other cases, there will be just one helper in the list.
		"""
		helpers = []
		if not self.helper_contains_formating:
			helpers.append(self.helper)
		else:
			for process in self.affected_instances:
				helpers.append(self.helper.format(
					NAME=self.name,
					PNAME=process.name,
					PID=process.pid,
					EXE=process.exe,
				))
		return helpers

	@property
	def instances(self):
		"""
		Return collection of processes with same name as application.
		I.e. running instances of the application
		"""
		return self.processes_factory.all().filtered(lambda process: process.name() == self.name)

	affected_instances = None
