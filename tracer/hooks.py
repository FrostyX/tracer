# -*- coding: utf-8 -*-
# hooks.py
# Module providing hooks functionality
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

import os
from tracer.paths import HOOKS_DIRS
from tracer.resources.pycomp import load_source

_hooks = {}


class HooksObserver(object):
	"""
	Provides interface for calling user hooks

	When initializing, loads all hooks located in HOOKS_DIRS. Then it can called
	with application name as argument. Observer ensures calling all hooks defined for the application.
	"""
	def __init__(self):
		_register_hooks()

	def __call__(self, app):
		if app not in _hooks:
			return

		[f() for f in _hooks[app]]


def match(apps):
	"""
	Decorator for tracer hooks.

	Example::

		from tracer import hooks

		@hooks.match("foo")
		def hook_app():
		    print("Hey, application foo was found")

	.. note::
		You can match multiple applications by calling ``@hooks.match`` with list of them.

	"""
	def decorator(f):
		for app in apps if type(apps) == list else [apps]:
			if app not in _hooks:
				_hooks[app] = []
			_hooks[app].append(f)
		return f
	return decorator


def _register_hooks():
	# see search function here
	# http://stackoverflow.com/a/4788700/3285282

	for hook_dir in HOOKS_DIRS:
		for root, dirs, files in os.walk(hook_dir):
			for fname in files:
				modname = os.path.splitext(fname)[0]
				try:
					load_source(modname, os.path.join(root, fname))
				except Exception:
					continue
