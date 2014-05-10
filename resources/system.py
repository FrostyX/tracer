#-*- coding: utf-8 -*-
# system.py
# Module for getting data about your operating system
# Dont worry, only necessary data required for this application.
# Tracer *will not* store, collect or send your data anywhere.
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

import os
import platform
import resources.psutils as psutil
from packageManagers.dnf import Dnf
from packageManagers.yum import Yum
from packageManagers.portage import Portage
from packageManagers.dpkg import Dpkg
from resources.exceptions import UnsupportedDistribution

def package_manager():
	"""Returns instance of package manager according to installed linux distribution"""

	distro = platform.linux_distribution(full_distribution_name=False)[0]
	def e(): raise UnsupportedDistribution(distro)

	return {
		'gentoo': Portage,
		'fedora': Dnf,
		'debian': Dpkg,
	}.get(distro, e)()

def init_system():
	"""
	Returns name of init system you are using
	e.g. init, systemd, upstart
	"""

	init = psutil.Process(1)
	name = init.name.split(" ")[0]
	return name
