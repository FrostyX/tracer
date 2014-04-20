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

from bs4 import BeautifulSoup
from os.path import dirname, realpath
parentdir = dirname(dirname(realpath(__file__)))

class Rules:

	DEFINITIONS = parentdir + "/rules/rules.xml"

	ACTIONS = {
		"CALL-PARENT"  :  "call-parent",
		"PRINT"        :  "print",
	}
	_DEFAULT_ACTION = ACTIONS["CALL-PARENT"]

	@staticmethod
	def find(app_name):
		f = open(Rules.DEFINITIONS)
		soup = BeautifulSoup(f.read())

		rule = soup.find("rule", {"name" : app_name})
		if not rule:
			return None

		rule.attrs.setdefault("action", Rules._DEFAULT_ACTION)
		return rule.attrs


	@staticmethod
	def all():
		rules = []
		f = open(Rules.DEFINITIONS)
		soup = BeautifulSoup(f.read())

		for rule in soup.find_all("rule"):
			r = rule.attrs
			r.setdefault('action', Rules._DEFAULT_ACTION)
			rules.append(r)

		f.close();
		return rules
