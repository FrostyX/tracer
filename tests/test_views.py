from __meta__ import *

import StringIO
from tracer.views.default import DefaultView
from tracer.resources.applications import Application
from tracer.resources.collections import ApplicationsCollection


class TestViews(unittest.TestCase):

	def setUp(self):
		self.out = StringIO.StringIO()

	def test_default_none(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock())
		view.assign("applications", ApplicationsCollection([]))
		view.render()
		self.assertEquals(self.out.getvalue(), "")

	def test_default_with_helpers(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock())
		view.assign("applications", ApplicationsCollection([
			Application({"type": "application", "helper": "first helper"}),
			Application({"type": "application", "helper": "second helper"}),
			Application({"type": "application", "helper": "third helper"}),
		]))
		view.render()
		self.assertEquals(self.out.getvalue(), (
			"You should restart:\n"
		    "  * Some applications using:\n"
		    "      first helper\n"
		    "      second helper\n"
		    "      third helper\n"
		))

	def test_default_without_helpers(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock())
		view.assign("applications", ApplicationsCollection([
			Application({"type": "application", "name": "foo", "helper": None}),
			Application({"type": "application", "name": "bar", "helper": None}),
			Application({"type": "application", "name": "baz", "helper": None}),
		]))
		view.render()
		self.assertEquals(self.out.getvalue(), (
			"You should restart:\n"
			"  * These applications manually:\n"
			"      bar\n"
			"      baz\n"
			"      foo\n"
		))

	def test_default_with_without_helpers(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock())
		view.assign("applications", ApplicationsCollection([
			Application({"type": "application", "helper": "first helper"}),
			Application({"type": "application", "helper": "second helper"}),
			Application({"type": "application", "helper": "third helper"}),
			Application({"type": "application", "name": "foo", "helper": None}),
			Application({"type": "application", "name": "bar", "helper": None}),
			Application({"type": "application", "name": "baz", "helper": None}),
		]))
		view.render()
		self.assertEquals(self.out.getvalue(), (
			"You should restart:\n"
			"  * Some applications using:\n"
			"      first helper\n"
			"      second helper\n"
			"      third helper\n"
			"\n"
			"  * These applications manually:\n"
			"      bar\n"
			"      baz\n"
			"      foo\n"
		))

	def test_default_all_session(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock(all=True))
		view.assign("applications", ApplicationsCollection([
			Application({"type": "session", "name": "foo", "helper": "h1"}),
			Application({"type": "session", "name": "bar", "helper": "h2"}),
			Application({"type": "session", "name": "baz", "helper": "h3"}),
		]))
		view.render()
		self.assertEquals(self.out.getvalue(), (
			"You should restart:\n"
			"  * These applications restarting your session:\n"
			"      bar\n"
			"      baz\n"
			"      foo\n"
		))

	def test_default_all_static(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock(all=True))
		view.assign("applications", ApplicationsCollection([
			Application({"type": "static", "name": "foo", "helper": "h1"}),
			Application({"type": "static", "name": "bar", "helper": "h2"}),
			Application({"type": "static", "name": "baz", "helper": "h3"}),
		]))
		view.render()
		self.assertEquals(self.out.getvalue(), (
			"You should restart:\n"
			"  * These applications rebooting your computer:\n"
			"      bar\n"
			"      baz\n"
			"      foo\n"
		))

	def test_default_all_session_static(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock(all=True))
		view.assign("applications", ApplicationsCollection([
			Application({"type": "session", "name": "foo", "helper": "h1"}),
			Application({"type": "session", "name": "bar", "helper": "h2"}),
			Application({"type": "session", "name": "baz", "helper": "h3"}),
			Application({"type": "static",  "name": "aaa", "helper": "h4"}),
			Application({"type": "static",  "name": "bbb", "helper": "h5"}),
			Application({"type": "static",  "name": "ccc", "helper": "h6"}),
		]))
		view.render()
		self.assertEquals(self.out.getvalue(), (
			"You should restart:\n"
			"  * These applications restarting your session:\n"
			"      bar\n"
			"      baz\n"
			"      foo\n"
			"\n"
			"  * These applications rebooting your computer:\n"
		    "      aaa\n"
		    "      bbb\n"
		    "      ccc\n"
		))

	def test_default_all(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock(all=True))
		view.assign("applications", ApplicationsCollection([
			Application({"type": "application", "helper": "first helper"}),
			Application({"type": "application", "helper": "second helper"}),
			Application({"type": "application", "name": "foo", "helper": None}),
			Application({"type": "application", "name": "bar", "helper": None}),
			Application({"type": "session", "name": "baz", "helper": "h1"}),
			Application({"type": "session", "name": "qux", "helper": "h2"}),
			Application({"type": "static",  "name": "aaa", "helper": "h3"}),
			Application({"type": "static",  "name": "bbb", "helper": "h4"}),
		]))
		view.render()
		self.assertEquals(self.out.getvalue(), (
			"You should restart:\n"
			"  * Some applications using:\n"
			"      first helper\n"
			"      second helper\n"
			"\n"
			"  * These applications manually:\n"
			"      bar\n"
			"      foo\n"
			"\n"
			"  * These applications restarting your session:\n"
			"      baz\n"
			"      qux\n"
			"\n"
			"  * These applications rebooting your computer:\n"
			"      aaa\n"
			"      bbb\n"
		))

	def test_default_not_all(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock())
		view.assign("applications", ApplicationsCollection([
			Application({"type": "application", "helper": "first helper"}),
			Application({"type": "application", "helper": "second helper"}),
			Application({"type": "application", "name": "foo", "helper": None}),
			Application({"type": "application", "name": "bar", "helper": None}),
			Application({"type": "session", "name": "baz", "helper": "h1"}),
			Application({"type": "session", "name": "qux", "helper": "h2"}),
			Application({"type": "static",  "name": "aaa", "helper": "h3"}),
		]))
		view.render()
		self.assertEquals(self.out.getvalue(), (
			"You should restart:\n"
			"  * Some applications using:\n"
			"      first helper\n"
			"      second helper\n"
			"\n"
			"  * These applications manually:\n"
			"      bar\n"
			"      foo\n"
			"\n"
			"Additionally to those process above, there are:\n"
			"  - 2 processes requiring restart of your session (i.e. Logging out & Logging in again)\n"
			"  - 1 processes requiring reboot\n"
		))


class ArgsMock(object):
	all = quiet = None

	def __init__(self, all=False, quiet=False):
		self.all = all
		self.quiet = quiet
