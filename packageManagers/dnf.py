#-*- coding: utf-8 -*-
"""Module to work with DNF package manager class
Copyright 2013 Jakub Kadlčík"""

from rpm import Rpm

class Dnf(Rpm):

	@property
	def history_path(self): return '/var/lib/dnf/history/'
