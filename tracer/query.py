#-*- coding: utf-8 -*-
# query.py
# Module providing querying operations to Tracer API
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

from tracer.resources.tracer import Tracer
from tracer.resources.system import System
from tracer.resources.rules import Rules
from tracer.resources.applications import Applications
from tracer.resources.memory import dump_memory


class Query(object):
	"""
	Provide API for Tracer querying operations.
	They are executed kind of lazily, so running the operation will
	return just an wrapper class with ``get()`` method.

	Example::

		from tracer.query import Query
		q = Query()
		q.affected_applications().get()

	.. note::
		Some querying methods can require root permissions

	"""

	def __init__(self, tracer=Tracer):
		self._tracer = tracer(System.package_manager(), Rules, Applications, dump_memory)

	def from_packages(self, packages):
		"""List of ``Package`` that only should be traced"""
		self._tracer.specified_packages = packages
		return self

	def now(self):
		"""
		Pretend that specified packages have been updated just now.
		Benefit of this is absolutely no need for openning the package history database
		"""
		self._tracer.now = True
		return self

	def affected_applications(self, user=None):
		"""
		Return list of applications which use some outdated files
		"""
		return Lazy(self._tracer.trace_affected, {"user": user})


class Lazy(object):
	def __init__(self, method, kwargs):
		self._method = method
		self._kwargs = kwargs

	def get(self):
		return self._method(**self._kwargs)
