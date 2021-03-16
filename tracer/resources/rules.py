#-*- coding: utf-8 -*-
# rules.py
# Manager for rules file
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
from os.path import dirname


class Rules(object):

	DEFINITIONS = map(lambda x: x + "/rules.xml", [DATA_DIR] + USER_CONFIG_DIRS)

	ACTIONS = {
		"CALL-PARENT"  :  "call-parent",
		"RETURN"        :  "return",
	}
	_DEFAULT_ACTION = ACTIONS["CALL-PARENT"]
	_rules = None

	@staticmethod
	def find(app_name):
		if not Rules._rules:
			Rules._load_definitions()

		for rule in Rules._rules:
			if rule.name == app_name:
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
			with open(file, "r") as f:
				xmldoc = minidom.parseString(f.read())
		except IOError:
			raise PathNotFound('DATA_DIR')
		except ExpatError as ex:
			msg = "Unable to parse {0}\nHint: {1}".format(file, ex)
			raise TracerError(msg)

		for rules in xmldoc.getElementsByTagName("rules"):
			for rule in rules.getElementsByTagName("rule"):
				attrs = dict(rule.attributes.items())
				r = Rule(attrs)
				if r in Rules._rules:
					i = Rules._rules.index(r)
					Rules._rules[i].update(r)
				else:
					r.setdefault('action', Rules._DEFAULT_ACTION)
					Rules._rules.append(r)


class Rule(object):

	"""
	Represent the rule defined in `rules.xml`

	Attributes
	----------
	name : str
	action : str
		See `Rules.ACTIONS` for possible values
	"""

	_attributes = None

	def __init__(self, attributes_dict):
		self._attributes = attributes_dict

	def __eq__(self, other):
		return isinstance(other, Rule) and self.name == other.name

	def __ne__(self, other):
		return not self.__eq__(other)

	def __getattr__(self, item):
		return self._attributes[item]

	def __len__(self):
		return len(self._attributes)

	def __contains__(self, item):
		return item in self._attributes

	def __str__(self):
		return "<Rule: " + self._attributes["name"] + ">"

	def __repr__(self):
		return self.__str__()

	def setdefault(self, key, value):
		self._attributes.setdefault(key, value)

	def update(self, values):
		if isinstance(values, Rule):
			values = values._attributes
		self._attributes.update(values)
