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

from bs4 import BeautifulSoup
from os.path import dirname, realpath
parentdir = dirname(dirname(realpath(__file__)))

class Applications:

	DEFINITIONS = parentdir + "/data/applications.xml"

	TYPES = {
		"DAEMON" : "daemon",
		"STATIC" : "static",
	}
	_apps = None

	@staticmethod
	def find(app_name):
		if not Applications._apps:
			Applications._load()

		for app in Applications._apps:
			if app["name"] == app_name:
				return app

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

		for app in soup.find_all("app"):
			if(len(app.attrs) > 1):
				Applications._apps.append(app.attrs)

		for group in soup.find_all("group"):
			for app in group.findChildren():
				app.attrs.update(group.attrs)
				Applications._apps.append(app.attrs)

		f.close();
