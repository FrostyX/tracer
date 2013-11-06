#!/usr/bin/python
# -*- coding: utf-8 -*-
# Tracer finds outdated running packages in your system
# Copyright 2013 Jakub Kadlčík

# Enable importing modules from parent directory (tracer's root directory)
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

# Tracer modules
from packageManagers.yum import Yum


print "Hello world"
