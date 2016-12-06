#!/usr/bin/python
#-*- coding: utf-8 -*-
# tracer.py
# Tracer finds outdated running applications in your system
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

from __future__ import unicode_literals
import os
import sys

if __name__ != "__main__":
	sys.stderr.write('The executable tracer module must not be imported.')
	sys.exit(1)

here = sys.path[0]
if here != '/usr/bin':
	toplevel = os.path.dirname(here)
	sys.path[0] = toplevel

import tracer.main
tracer.main.run()
