#-*- coding: utf-8 -*-
# en.py
# English localization module
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

import textwrap

LOCALE = {

	# Global
	"root_only"         : "Only root can use this application",
	"not_unlisted_apps" : "Please note that there are:",
	"requiring_session" : "  - {0} processes requiring restarting your session (i.e. Logging out & Logging in again)",
	"reuquiring_reboot" : "  - {0} processes requiring reboot",

	# Interactive
	"prompt_help"      : "Press application number for help or 'q' to quit",
	"press_enter"      : "-- Press enter to get list of applications --",
	"wrong_app_number" : "Wrong application number",

	# Helpers
	"app_not_running"   : "Application called {0} is not running",
	"not_known_restart" : "Sorry, It's not known",
	"helper"            : textwrap.dedent("""\
				* {app_name}
				    Package:     {pkg_name}
				    Description: {pkg_description}
				    Type:        {type}
				    State:       {app_name} has been started by {user} {time} ago. PID - {pid}

				    How to restart:
						 {how_to_restart}
				"""),
}
