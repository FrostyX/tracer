#-*- coding: utf-8 -*-
# FilenameCleaner.py
# Module to stripping the version numers from filenames
#
# i.e.:
#     /lib/libdl-2.19.so   -->   /lib/libdl.so
#     /lib/libncurses.so.5.9   -->   /lib/libncurses.so
#
# This implementation really sux and surely there is a much better
# way how to implement following methods. They are properly tested
# in `test_FilenameCleaner.py` so feel free to refactor them.
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


class FilenameCleaner(object):

	@staticmethod
	def strip(filename):
		filename = FilenameCleaner._strip_abnormalities(filename)
		try:
			slash = filename.rindex('/')
			dirname = filename[:slash]
			basename = filename[slash+1:]

			if "." in basename:
				basename = FilenameCleaner._strip_around_so_delimited_dots(basename)
				basename = FilenameCleaner._strip_after_dash(basename)
			return dirname + '/' + basename

		except IndexError: pass
		except ValueError: pass
		return filename

	@staticmethod
	def _strip_abnormalities(filename):
		# Doesnt matter what is after space cause filename ends with first space
		try: filename = filename[:filename.index(' ')]
		except ValueError: pass

		# On Gentoo, there is #new after some files in lsof
		# i.e. /usr/bin/gvim#new (deleted)
		if filename.endswith('#new'):
			filename = filename[0:-4]

		# On Fedora, there is something like ;541350b3 after some files in lsof
		# See issue #9
		if ';' in filename:
			filename = filename[0:filename.index(';')]

		# On Fedora, there is something like .#prelink#.N3n7Rk (deleted) after some files in lsof
		# See issue #9
		if '.#prelink#.' in filename:
			filename = filename[0:filename.rindex('.#prelink#.')]

		return filename

	@staticmethod
	def _strip_around_so_delimited_dots(basename):
		try:
			split = basename.split(".so")
			basename = split[0]
			if len(split) > 1:
				basename += ".so"
			first_dot_i = basename.index(".")
			last_dot_i = basename.rindex(".")
			basename = basename[:first_dot_i] + basename[last_dot_i:]

		except IndexError: pass
		except ValueError: pass
		return basename

	@staticmethod
	def _strip_after_dash(basename):
		try:
			dash = basename.rindex("-")
			dot = basename.index(".", dash)
			if FilenameCleaner._is_version(basename[dash+1:dot]):
				basename = basename[:dash] + basename[dot:]

		except IndexError: pass
		except ValueError: pass
		return basename

	@staticmethod
	def _is_version(string):
		"""
		Returns True if string contains only digits and dots
		"""
		for char in string:
			if (not char.isdigit()) or char == ".":
				return False
		return True
