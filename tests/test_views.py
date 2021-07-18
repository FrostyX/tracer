from __future__ import unicode_literals
from .__meta__ import *


from tracer.resources.pycomp import StringIO
from tracer.views.default import DefaultView
from tracer.views.helper import HelperView
from tracer.resources.applications import Applications, Application
from tracer.resources.collections import ApplicationsCollection
from tracer.resources.package import Package
from .test_tracer import ProcessMock, AffectedProcessMock


import tracer.views.default
import tracer.views.helper
import tracer.views.note_for_hidden

import gettext
t = gettext.translation('tracer', fallback=True, languages=["en"])
_ = t.ugettext

try:
	from unittest.mock import patch
except:
	from mock import patch

# Mock the gettext function to use only english
tracer.views.default._ = _
tracer.views.helper._ = _
tracer.views.note_for_hidden._ = _


class TestViews(unittest.TestCase):

	def setUp(self):
		self.out = StringIO()

	def test_default_none(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock())
		view.assign("applications", ApplicationsCollection([]))
		view.render()
		self.assertEqual(self.out.getvalue(), "")

	def test_default_with_helpers(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock())
		view.assign("applications", ApplicationsCollection([
			Application({"type": "application", "helper": "first helper", "name": "first"}),
			Application({"type": "application", "helper": "second helper", "name": "second"}),
			Application({"type": "application", "helper": "third helper", "name": "third"}),
		]))
		view.render()
		self.assertEqual(self.out.getvalue(), (
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
		self.assertEqual(self.out.getvalue(), (
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
			Application({"type": "application", "helper": "first helper", "name": "first"}),
			Application({"type": "application", "helper": "second helper", "name": "second"}),
			Application({"type": "application", "helper": "third helper", "name": "third"}),
			Application({"type": "application", "name": "foo", "helper": None}),
			Application({"type": "application", "name": "bar", "helper": None}),
			Application({"type": "application", "name": "baz", "helper": None}),
		]))
		view.render()
		self.assertEqual(self.out.getvalue(), (
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
		self.assertEqual(self.out.getvalue(), (
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
		self.assertEqual(self.out.getvalue(), (
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
		self.assertEqual(self.out.getvalue(), (
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
			Application({"type": "application", "helper": "first helper", "name": "first"}),
			Application({"type": "application", "helper": "second helper", "name": "second"}),
			Application({"type": "application", "name": "foo", "helper": None}),
			Application({"type": "application", "name": "bar", "helper": None}),
			Application({"type": "session", "name": "baz", "helper": "h1"}),
			Application({"type": "session", "name": "qux", "helper": "h2"}),
			Application({"type": "static",  "name": "aaa", "helper": "h3"}),
			Application({"type": "static",  "name": "bbb", "helper": "h4"}),
		]))
		view.render()
		self.assertEqual(self.out.getvalue(), (
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
			Application({"type": "application", "helper": "first helper", "name": "first"}),
			Application({"type": "application", "helper": "second helper", "name": "second"}),
			Application({"type": "application", "name": "foo", "helper": None}),
			Application({"type": "application", "name": "bar", "helper": None}),
			Application({"type": "session", "name": "baz", "helper": "h1"}),
			Application({"type": "session", "name": "qux", "helper": "h2"}),
			Application({"type": "static",  "name": "aaa", "helper": "h3"}),
		]))
		view.render()
		self.assertEqual(self.out.getvalue(), (
			"You should restart:\n"
			"  * Some applications using:\n"
			"      first helper\n"
			"      second helper\n"
			"\n"
			"  * These applications manually:\n"
			"      bar\n"
			"      foo\n"
			"\n"
			"Additionally, there are:\n"
			"  - 2 processes requiring restart of your session (i.e. Logging out & Logging in again)\n"
			"  - 1 processes requiring reboot\n"
		))

	def test_default_note_only(self):
		view = DefaultView(self.out)
		view.assign("args", ArgsMock())
		view.assign("applications", ApplicationsCollection([
			Application({"type": "session", "name": "foo", "helper": "h1"}),
			Application({"type": "session", "name": "bar", "helper": "h2"}),
			Application({"type": "static",  "name": "baz", "helper": "h3"}),
		]))
		view.render()
		self.assertEqual(self.out.getvalue(), (
			"There are:\n"
			"  - 2 processes requiring restart of your session (i.e. Logging out & Logging in again)\n"
			"  - 1 processes requiring reboot\n"
		))

	@patch('tracer.resources.applications.System.init_system', return_value="dummy")
	def test_helper(self, init_system):
		processes = [
			ProcessMock(2, "foo", 1234, ["file1", "file2"]),
			ProcessMock(3, "foo", 5678, ["file2", "file3"]),
		]

		package = Package("foopackage")
		package.modified = None
		package.description = "Foo package description"
		package.category = "categ"
		package.files = ["file1", "file2"]

		a1 = AffectedProcessMock(2)
		a1.packages = set([package])
		affected_by = [a1]

		view = HelperView(self.out)
		view.assign("args", ArgsMock(verbose=2))
		view.assign("processes", processes)
		view.assign("application", Applications.find("foo"))
		view.assign("package", package)
		view.assign("affected_by", affected_by)
		view.assign("affects", None)
		view.render()
		self.assertEqual(self.out.getvalue(), (
			"* foo\n"
			"    Package:     foopackage\n"
			"    Description: Foo package description\n"
			"    Type:        Application\n"
			"    State:       foo has been started by None some-time ago. PID - 2\n"
			"                 foo has been started by None some-time ago. PID - 3\n"
			"\n"
			"    Affected by:\n"
			"        foopackage\n"
			"            file1\n"
			"            file2\n"
		))


class ArgsMock(object):
	all = quiet = None

	def __init__(self, all=False, quiet=False, user=False, verbose=False):
		self.all = all
		self.quiet = quiet
		self.user = user
		self.verbose = verbose


class ProcessMock(object):
	def __init__(self, pid, name, create_time, files):
		self.parent = None
		self.pid = pid
		self.files = files
		self._name = name
		self._create_time = create_time
		self.str_started_ago = "some-time"

	def name(self):
		return self._name

	def create_time(self):
		return self._create_time

	def children(self):
		return []

	def username(self):
		return None
