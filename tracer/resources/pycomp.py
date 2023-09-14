#-*- coding: utf-8 -*-
# pycomp.py
# Compatibility layer between python2 and python3
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

from sys import version_info

PY3 = version_info.major >= 3

if PY3:
	from io import StringIO
	from functools import lru_cache
else:
	from StringIO import StringIO
	from backports.functools_lru_cache import lru_cache


def load_source(module_name, path):
	"""
	Read and evaluate a python file
	This is useful when we don't know the module name beforehand and somehow
	figure it out at the runtime (e.g. user-defined hook files)
	"""
	if not PY3:
		import imp
		return imp.load_source(module_name, path)

	from importlib.machinery import SourceFileLoader
	import types
	loader = SourceFileLoader(module_name, path)
	loaded = types.ModuleType(loader.name)
	return loader.exec_module(loaded)
