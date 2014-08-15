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
from tracer.paths import DATA_DIR
from tracer.resources.exceptions import PathNotFound
from tracer.resources.lang import _


class Applications:

	DEFINITIONS = DATA_DIR + "/applications.xml"

	TYPES = {
		"DAEMON"       :  "daemon",
		"STATIC"       :  "static",
		"SESSION"      :  "session",
		"APPLICATION"  :  "application"
	}
	DEFAULT_TYPE = TYPES["APPLICATION"]
	_apps = None

	def __init__(self):
		pass

	@staticmethod
	def find(app_name):
		if not Applications._apps:
			Applications._load()

		for app in Applications._apps:
			if app["name"] == app_name:
				app.setdefault('type', Applications.DEFAULT_TYPE)
				app.setdefault('helper', Applications._helper(app))
				return app

		return {"name" : app_name, "type" : Applications.DEFAULT_TYPE, "helper" : None}

	@staticmethod
	def all():
		if not Applications._apps:
			Applications._load()

		return Applications._apps

	@staticmethod
	def _load():
		try:
			Applications._apps = []
			f = open(Applications.DEFINITIONS)
			soup = BeautifulSoup(f.read())

			for child in soup.applications.children:
				if not isinstance(child, element.Tag):
					continue

				if child.name == "app":
					Applications._apps.append(child.attrs)

				if child.name == "group":
					for app in child.findChildren():
						app.attrs.update(child.attrs)
						Applications._apps.append(app.attrs)

			f.close()

		except IOError:
			raise PathNotFound('DATA_DIR')

	@staticmethod
	def _helper(app):
		if app["type"] == Applications.TYPES["DAEMON"]:
			return "service {0} restart".format(app["name"])

		elif app["type"] == Applications.TYPES["STATIC"]:
			return _("static_restart")

		elif app["type"] == Applications.TYPES["SESSION"]:
			return _("session_restart")

		return None


class Application:

	"""
	Represent the application defined in `applications.xml`

	Attributes
	----------
	name : str
	type : str
		See `Applications.TYPES` for possible values
	helper : str
		Describes how to restart the applications
	"""

	_attributes = None

	def __init__(self, attributes_dict):
		self._attributes = attributes_dict

	def __getattr__(self, item):
		return self._attributes[item]

	def __str__(self):
		return "<Application: " + self._attributes["name"] + ">"
