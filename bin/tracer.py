#!/usr/bin/python
# -*- coding: utf-8 -*-
# Tracer finds outdated running packages in your system
# Copyright 2013 Jakub Kadlčík

# Enable importing modules from parent directory (tracer's root directory)
import os
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.sys.path.insert(0, parentdir)

import sys
import time
from resources.tracer import Tracer
from resources.args_parser import args
from resources.package import Package


def main(argv=sys.argv, stdin=[]):
	# If there is something on stdin (that means piped into tracer)
	stdin_packages = []
	if not sys.stdin.isatty():
		stdin_packages = sys.stdin.readline().split()

	# All input packages enchanced by actual time (as modified time)
	packages = []
	for package in args.packages + stdin_packages:
		packages.append(Package(package, time.time() if args.now else None))

	tracer = Tracer()
	tracer.specified_packages = packages
	tracer.now = args.now
	for package in set(tracer.trace_running()):
		# More times a package is updated the more times it is contained in a package list.
		print package.name

if __name__ == '__main__':
	if os.getuid() != 0:
		print "Only root can use this application"
		sys.exit();

	main()
