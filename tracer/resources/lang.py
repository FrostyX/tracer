#-*- coding: utf-8 -*-
# lang.py
# Module working with language localizations
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

import locale
import gettext
from gettext import NullTranslations
from sys import version_info
from tracer.paths import LANG_DIR

# python 3 compabillity settings
if version_info.major >= 3:
	# u?gettext dont exists in python3 NullTranslations
	NullTranslations.ugettext = NullTranslations.gettext
	NullTranslations.ungettext = NullTranslations.ngettext

t = gettext.translation('tracer', fallback=True, localedir=LANG_DIR)
_ = t.ugettext
