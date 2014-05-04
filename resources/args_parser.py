#-*- coding: utf-8 -*-
# args_parser.py
# Module for parsing console arguments
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

import argparse

parser = argparse.ArgumentParser(
	prog = 'tracer',
	description='Tracer finds outdated running applications in your system',
)

parser.add_argument('packages',
	nargs='*',
	type=str,
	help='packages that only should be traced'
)

parser.add_argument('-i', '--interactive',
	dest='interactive',
	action='store_true',
	help='run tracer in interactive mode. Print numbered applications and give helpers based on numbers'
)

parser.add_argument('-n', '--now',
	dest='now',
	action='store_true',
	help='when there are specified packages, dont look for time of their update. Use "now" instead'
)

parser.add_argument('-s', '--show',
	nargs=1,
	dest='helper',
	metavar='app_name',
	help='show helper for given application'
)

args = parser.parse_args()
