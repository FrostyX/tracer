#-*- coding: utf-8 -*-
# args_parser.py
# Module for parsing console arguments
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

import argparse

try:
    import argcomplete
except ImportError:
    pass

parser = argparse.ArgumentParser(
	prog = 'tracer',
	description='Tracer finds outdated running applications in your system',
)

# Obsolete
parser.add_argument('pkgs',
	nargs='*',
	type=str,
	help='Obsolete: Use --packages instead'
)

parser.add_argument('--packages',
	dest='packages',
	nargs='*',
	type=str,
	default=[],
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

parser.add_argument('-t', '--timestamp',
	nargs=1,
	default=[None],
	dest='timestamp',
	help='since when the updates should be'
)

parser.add_argument('-q', '--quiet',
	dest='quiet',
	action='store_true',
	help='do not print additional information'
)

parser.add_argument('-v', '--verbose',
	dest='verbose',
	action='count',
	default=0,
	help='print more informations. Use -v or -vv'
)

parser.add_argument('-s', '--show',
	nargs='+',
	dest='helper',
	metavar='app_name',
	help='show helper for given application'
)

parser.add_argument('--helpers',
	dest='helpers',
	action='store_true',
	help='not list applications, but list their helpers'
)

parser.add_argument('-a', '--all',
	dest='all',
	action='store_true',
	help='list even session and unrestartable applications'
)

parser.add_argument('--daemons-only', '--services-only',
	dest='daemons_only',
	action='store_true',
	help='list only daemons/services'
)

parser.add_argument('--hooks-only',
	dest='hooks_only',
	action='store_true',
	help='do not print traced applications, only run their hooks'
)

parser.add_argument('--version',
	dest='version',
	action='store_true',
	help='print program version'
)

parser.add_argument('--show-resource',
	nargs=1,
	choices=['packages', 'processes', 'rules', 'applications', 'system'],
	dest='resource',
	help='provide informations about selected resource'
)

user = parser.add_mutually_exclusive_group()
user.add_argument("-u", "--user",
	nargs=1,
	dest='user',
	metavar='username'
)

user.add_argument("-r", "--root",
	dest='user',
	action="store_const",
	const='root'
)

user.add_argument("-e", "--everyone",
	dest='user',
	action="store_const",
	const='*'
)

user.add_argument("--erased",
	dest="erased",
	action="store_true",
	help="print even section with erased packages (DNF only)",
	default=False
)
try:
    argcomplete.autocomplete(parser)
except NameError:
    pass
