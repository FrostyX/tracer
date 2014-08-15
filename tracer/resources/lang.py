#-*- coding: utf-8 -*-
# lang.py
# Module working with language localizations
#
# Copyright (C) 2013 Jakub Kadlčík
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

DEFAULT_LANG = "en"

# WARNING: There are imports in package_manager()
from os import environ
from os.path import dirname, realpath
parentdir = dirname(dirname(realpath(__file__)))
_LANG_PATH = parentdir + "/lang/"

# Languages supported by system, sorted by priority
def _system_languages():
	lang = []
	for l in environ.get('LANG', '').split(':'):
		lang.append(l.split("_")[0])

	lang.append(DEFAULT_LANG)
	return lang

# Import language locale (throws ImportError)
def _locale(lang):
	return __import__("tracer.lang.%s" % lang, fromlist=["LOCALE"]).LOCALE

# Import a dictionary containing all localization lines for system language
_LOCALE = None
for lang in _system_languages():
	try: _LOCALE = _locale(lang); break
	except ImportError: pass

# Whenever you want print some language-specific text, use this function
def _(string_label):
	try: return _LOCALE[string_label]
	except KeyError: return string_label
