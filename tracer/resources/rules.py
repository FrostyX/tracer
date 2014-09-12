#-*- coding: utf-8 -*-
# rules.py
# Manager for rules file
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

from bs4 import BeautifulSoup
from tracer.paths import DATA_DIR, USER_CONFIG_DIRS
from tracer.resources.exceptions import PathNotFound
from os.path import dirname


class Rules:

	DEFINITIONS = map(lambda x: x + "/rules.xml", [DATA_DIR] + USER_CONFIG_DIRS)

	ACTIONS = {
		"CALL-PARENT"  :  "call-parent",
		"PRINT"        :  "print",
	}
	_DEFAULT_ACTION = ACTIONS["CALL-PARENT"]
	_rules = None

	def __init__(self):
		pass

	@staticmethod
	def find(app_name):
		if not Rules._rules:
			Rules._load_definitions()

		for rule in Rules._rules:
			if rule["name"] == app_name:
				return rule

	@staticmethod
	def all():
		if not Rules._rules:
			Rules._load_definitions()

		return Rules._rules

	@staticmethod
	def _load_definitions():
		Rules._rules = []
		for file in Rules.DEFINITIONS:
			try: Rules._load(file);
			except PathNotFound as ex:
				if not dirname(file) in USER_CONFIG_DIRS:
					raise ex

	@staticmethod
	def _load(file):
		try:
			f = open(file)
			soup = BeautifulSoup(f.read())

			for rule in soup.find_all("rule"):
				r = rule.attrs
				if r in Rules._rules:
					i = Rules._rules.index(r)
					Rules._rules[i].update(r)
				else:
					r.setdefault('action', Rules._DEFAULT_ACTION)
					Rules._rules.append(r)

			f.close()

		except IOError:
			raise PathNotFound('DATA_DIR')

