#-*- coding: utf-8 -*-
# collections.py
# Define various kind of collections
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

from operator import attrgetter


class ApplicationsCollection(list):

	def sorted(self, attribute):
		return sorted(self, key=attrgetter(attribute))


class ProcessesCollection(list):

	def owned_by(self, user):
		processes = filter(lambda process: process.username == user, self)
		return ProcessesCollection(processes)

	def newer_than(self, timestamp):
		processes = filter(lambda process: process.create_time >= timestamp, self)
		return ProcessesCollection(processes)
