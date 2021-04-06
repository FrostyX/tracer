#-*- coding: utf-8 -*-
# yum.py
# Module to work with YUM package manager class
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


from tracer.resources.system import System
if System.distribution() in ["fedora", "rhel", "centos", "centos-7", "ol"]:

	from tracer.packageManagers.rpm import Rpm

	class Yum(Rpm):

		@property
		def history_path(self): return '/var/lib/yum/history/'
