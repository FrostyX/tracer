#-*- coding: utf-8 -*-
# applications.py
# Manager for applications file
#
# Copyright (C) 2016 Jakub Kadlcik
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

from xml.dom import minidom
from xml.parsers.expat import ExpatError
from tracer.paths import DATA_DIR, USER_CONFIG_DIRS
from tracer.resources.exceptions import PathNotFound, TracerError
from tracer.resources.collections import ApplicationsCollection
from tracer.resources.lang import _
from tracer.resources.processes import Processes
from tracer.resources.system import System
from tracer.resources.SystemdDbus import SystemdDbus
from tracer.resources.pycomp import lru_cache
import os
import re


class Applications(object):

	DEFINITIONS = map(lambda x: x + "/applications.xml", [DATA_DIR] + USER_CONFIG_DIRS)

	TYPES = {
		"DAEMON"       :  "daemon",
		"STATIC"       :  "static",
		"SESSION"      :  "session",
		"APPLICATION"  :  "application",
		"ERASED"       :  "erased",
		"UNDEF"        :  "undefined" #Internal only
	}
	DEFAULT_TYPE = TYPES["APPLICATION"]
	_apps = None

	@staticmethod
	def find(app_name):
		if not Applications._apps:
			Applications._load_definitions()

		for app in Applications._apps:
			if app.name == app_name:
				return app if "rename" not in app else Applications.find(app.rename)

		# Return the default application
		return Application({
			"name": app_name,
			"type": Applications.TYPES["UNDEF"],
			"helper": None,
			"note": None,
			"ignore": False,
		})

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

	@classmethod
	def _load(cls, file):
		try:
			with open(file, "r") as f:
				xmldoc = minidom.parseString(f.read())
		except IOError:
			raise PathNotFound('DATA_DIR')
		except ExpatError as ex:
			msg = "Unable to parse {0}\nHint: {1}".format(file, ex)
			raise TracerError(msg)

		for applications in xmldoc.getElementsByTagName("applications"):
			cls._remove_unwanted_children(applications)
			for child in applications.childNodes:
				if child.nodeName == "app":
					attrs = dict(child.attributes.items())
					Applications._append_application(attrs)

				if child.nodeName == "group":
					cls._remove_unwanted_children(child)
					for app in child.childNodes:
						app_attrs = dict(app.attributes.items())
						group_attrs = dict(child.attributes.items())
						Applications._append_application(app_attrs, group_attrs)

	@classmethod
	def _remove_unwanted_children(cls, node):
		for child in node.childNodes:
			if child.nodeType != node.ELEMENT_NODE:
				node.removeChild(child)

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
			application.setdefault('note', None)
			application.setdefault('ignore', False)
			Applications._apps.append(application)

	@staticmethod
	def _helper(app):
		if app.type == Applications.TYPES["DAEMON"]:
			if System.init_system() == "systemd":
				return "systemctl restart {0}".format(app.name)
			else:
				return "service {0} restart".format(app.name)

		elif app.type == Applications.TYPES["STATIC"]:
			return _("You will have to reboot your computer")

		elif app.type == Applications.TYPES["SESSION"]:
			return _("You will have to log out & log in again")

		return None


class Application:

	"""
	Represent the application defined in ``applications.xml``

	:param str name: The name of the application
	:param str type: See ``Applications.TYPES`` for possible values
	:param str helper: Describes how to restart the applications
	:param bool note: Provides additional informations to the ``helper``
	:param bool ignore: If ``True``, the application won't be printed
	:param Processes processes_factory: Class providing list of running processes

	"""

	processes_factory = Processes
	_attributes = None

	def __init__(self, attributes_dict):
		self._attributes = attributes_dict
		self._cached_name = None

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
		return "<" + self.__class__.__name__ + ": " + self._attributes["name"] + ">"

	def __repr__(self):
		return self.__str__()

	def setdefault(self, key, value):
		self._attributes.setdefault(key, value)

	def update(self, values):
		if isinstance(values, Application):
			values = values._attributes
		self._attributes.update(values)

	@property
	def is_interpreted(self):
		# @TODO check all instances
		return self.instances and self.instances[0].is_interpreted

	@property
	@lru_cache(maxsize=None)
	def is_session(self):
		if self.name.startswith("ssh-") and self.name.endswith("-session"):
			return True
		return self.instances and self.instances[0].is_session

	@property
	def type(self):
		if self._attributes["type"] != Applications.TYPES["UNDEF"]:
			return self._attributes["type"]

		if self.is_session:
			return Applications.TYPES["SESSION"]

		if self.is_service:
			return Applications.TYPES["DAEMON"]

		return Applications.DEFAULT_TYPE

	@property
	@lru_cache(maxsize=None)
	def is_service(self):
		if System.init_system() == "systemd":
			return SystemdDbus().unit_path_from_id("{0}.service".format(self.name))

	# @TODO rename to helper_format
	@property
	def helper(self):
		helper = self._attributes["helper"] or Applications._helper(self)
		if System.user() != "root" and self.type == Applications.TYPES["DAEMON"]:
			if helper and not helper.startswith("sudo "):
				helper = "sudo " + helper
		return helper

	@property
	def helper_contains_formating(self):
		if not self.helper:
			return None
		return bool(re.search(r"\{.*\}", self.helper))

	@property
	def helper_contains_name(self):
		if not self.helper:
			return None
		return bool(re.search(r"\{NAME\}", self.helper))

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
		if self.helper:
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
		return self.processes_factory.all().filtered(
			lambda process: self._attributes["name"] in [process.name(), process.real_name])

	affected_instances = None


class AffectedApplication(Application):
	@property
	def name(self):
		# We need to cache manually instead of using `@lru_cache` because this
		# property is used for self.__hash__
		if not self._cached_name:
			self._cached_name = self._name()
		return self._cached_name

	def _name(self):
		if System.init_system() == "systemd":
			bus = SystemdDbus()

			# Trying to access `self.instances` just once
			try:
				pid = self.instances[0].pid
			except IndexError:
				pid = None

			if pid:
				if self.instances and bus.unit_path_from_pid(pid):
					if not bus.has_service_property_from_pid(pid, 'PAMName'):
						Id = bus.get_unit_property_from_pid(pid, 'Id')
						if Id and re.search(r"\.service$", Id):
							return re.sub(r'\.service$', '', Id)

		if self.is_interpreted:
			return self.instances[0].real_name
		return self._attributes["name"]
