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

from bs4 import BeautifulSoup, element
from os.path import dirname, realpath
parentdir = dirname(dirname(realpath(__file__)))

class Applications:

	DEFINITIONS = parentdir + "/data/applications.xml"

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
			Applications._load()

		for app in Applications._apps:
			if app["name"] == app_name:
				return app

		return {"name" : app_name, "type" : Applications.DEFAULT_TYPE}

	@staticmethod
	def all():
		if not Applications._apps:
			Applications._load()

		return Applications._apps

	@staticmethod
	def _load():
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

		f.close();
