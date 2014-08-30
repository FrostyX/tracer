#-*- coding: utf-8 -*-
# psutils.py
# Personally modified python-psutil package
# https://code.google.com/p/psutil/
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

import psutil


class TracerProcess(psutil.Process):
	def __eq__(self, process):
		"""For our purposes, two processes are equal when they have same name"""
		return (isinstance(process, self.__class__)
			and self.name == process.name)

	def __ne__(self, process):
		return not self.__eq__(process)

	def __hash__(self):
		return hash(self.name)

	@property
	def parent(self):
		p = super(TracerProcess, self).parent
		if p:
			p.__class__ = TracerProcess
		return p

	@property
	def exe(self):
		# On Gentoo, there is #new after some files in lsof
		# i.e. /usr/bin/gvim#new (deleted)
		exe = super(TracerProcess, self).exe
		if exe.endswith('#new'):
			exe = exe[0:-4]
		return exe
