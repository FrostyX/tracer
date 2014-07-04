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
from tracer.paths import DATA_DIR

class Rules:

	DEFINITIONS = DATA_DIR + "/rules.xml"

	ACTIONS = {
		"CALL-PARENT"  :  "call-parent",
		"PRINT"        :  "print",
	}
	_DEFAULT_ACTION = ACTIONS["CALL-PARENT"]
	_rules = None

	@staticmethod
	def find(app_name):
		if not Rules._rules:
			Rules._load()

		for rule in Rules._rules:
			if rule["name"] == app_name:
				return rule

	@staticmethod
	def all():
		if not Rules._rules:
			Rules._load()

		return Rules._rules

	@staticmethod
	def _load():
		Rules._rules = []
		f = open(Rules.DEFINITIONS)
		soup = BeautifulSoup(f.read())

		for rule in soup.find_all("rule"):
			r = rule.attrs
			r.setdefault('action', Rules._DEFAULT_ACTION)
			Rules._rules.append(r)

		f.close();
