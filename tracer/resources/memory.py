#-*- coding: utf-8 -*-
# memory.py
# Module to work with files in memory
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

from tracer.resources.processes import Processes
import psutil


def dump_memory(user=None):
	"""
	Returns memory in BTree structure

	{ file_1 : [process_1, process_2, ..., process_n],
		...
	}

	Which describes that processes 1 to `n` is using file_1
	"""
	memory = {}
	for process in Processes.all().owned_by(user).unique():
		try:
			for file in process.files:
				if file in memory:
					memory[file].append(process)
				else:
					memory[file] = [process]

		except psutil.NoSuchProcess: pass
		except psutil.AccessDenied: pass

	return memory
