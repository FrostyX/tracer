# SystemdUnit.py
# Module for getting data from Systemd about Units

# Copyright (C) 2017 Sean O'Keeffe
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

import dbus

class SystemdDbus(object):
	def __init__(self):
		self.__systemd = dbus.SystemBus().get_object('org.freedesktop.systemd1','/org/freedesktop/systemd1')
		self.__manager = dbus.Interface(self.__systemd, dbus_interface='org.freedesktop.systemd1.Manager')

	def unit_path_from_pid(self, pid):
		try:
			return self.__manager.GetUnitByPID(pid)
		except dbus.exceptions.DBusException:
			return False

	def unit_path_from_id(self, Id):
		try:
			return self.__manager.GetUnit(Id)
		except dbus.exceptions.DBusException:
			return False

	def has_service_property_from_pid(self, pid, attr):
		try:
			unit = self.unit_path_from_pid(pid)
			if not unit:
				return False

			proxy = dbus.SystemBus().get_object('org.freedesktop.systemd1', unit)
			propty = proxy.Get('org.freedesktop.systemd1.Service', attr, dbus_interface='org.freedesktop.DBus.Properties')
		except dbus.exceptions.DBusException:
			return False
		return bool(propty)

	def get_unit_property_from_pid(self, pid, attr):
		unit_path = self.unit_path_from_pid(pid)
		if bool(unit_path):
			proxy = dbus.SystemBus().get_object('org.freedesktop.systemd1', self.unit_path_from_pid(pid))
			return proxy.Get('org.freedesktop.systemd1.Unit', attr, dbus_interface='org.freedesktop.DBus.Properties')
		else:
			return False
