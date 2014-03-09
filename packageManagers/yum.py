#-*- coding: utf-8 -*-
"""Module to work with YUM package manager class
Copyright 2013 Jakub Kadlčík"""

from rpm import Rpm

class Yum(Rpm):

	@property
	def history_path(self): return '/var/lib/yum/history/'
