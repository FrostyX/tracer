import gettext
import unittest

import tracer
from tracer.resources.pycomp import StringIO
from tracer.views.blocks import BlocksView
from tracer.views.interactive import InteractiveView
from tracer.views.note_for_hidden import NoteForHiddenView
from tracer.views.resource.applications import ApplicationsView
from tracer.views.resource.packages import PackagesView
from tracer.views.resource.processes import ProcessesView
from tracer.views.resource.rules import RulesView
from tracer.views.resource.system import SystemView

from .__meta__ import *

t = gettext.translation('tracer', fallback=True, languages=["en"])
_ = t.ugettext

try:
	from unittest.mock import patch
except ImportError:
	from mock import patch

tracer.views.interactive._ = _
tracer.views.blocks._ = _
tracer.views.note_for_hidden._ = _
tracer.views.resource.processes._ = _
tracer.views.resource.packages._ = _
tracer.views.resource.rules._ = _
tracer.views.resource.applications._ = _
tracer.views.resource.system._ = _


class ArgsMock:
    all = quiet = None


class TestInteractiveView(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()

    @patch('tracer.views.interactive.input')
    @patch('builtins.print')
    def test_render_with_applications(self, mock_print, mock_input):
        apps = [type('App', (), {'name': 'app1'})(), type('App', (), {'name': 'app2'})()]
        args = ArgsMock()
        args.all = False
        args.session_count = 1
        args.static_count = 1
        
        view = InteractiveView(self.out)
        view.assign("applications", apps)
        view.assign("args", args)
        view.assign("total_count", 3)
        view.assign("session_count", 1)
        view.assign("static_count", 1)
        view.render()
        
        mock_print.assert_called()

    @patch('tracer.views.interactive.input')
    @patch('builtins.print')
    def test_render_without_applications(self, mock_print, mock_input):
        apps = []
        args = ArgsMock()
        args.all = False
        args.session_count = 0
        args.static_count = 0
        
        view = InteractiveView(self.out)
        view.assign("applications", apps)
        view.assign("args", args)
        view.assign("total_count", 0)
        view.assign("session_count", 0)
        view.assign("static_count", 0)
        view.render()
        
        calls = [str(c) for c in mock_print.call_args_list]
        self.assertFalse(any('You should restart' in str(c) for c in calls))


class TestBlocksView(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()

    def test_render_with_blocks(self):
        blocks = [{"title": "Block 1", "content": "Content 1\n"}, {"title": "Block 2", "content": "Content 2\n"}]
        view = BlocksView(self.out)
        view.assign("blocks", blocks)
        view.render()
        self.assertTrue(view.has_content_and_title())

    def test_has_content_and_title(self):
        view = BlocksView(self.out)
        view.assign("blocks", [{"title": "B1", "content": "C1"}])
        self.assertTrue(view.has_content_and_title())

    def test_has_content_and_title_empty(self):
        view = BlocksView(self.out)
        view.assign("blocks", [{"title": "", "content": ""}])
        self.assertFalse(view.has_content_and_title())


class TestNoteForHiddenView(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()

    @patch('builtins.print')
    def test_render_with_session_count(self, mock_print):
        args = ArgsMock()
        args.quiet = False
        view = NoteForHiddenView(self.out)
        view.assign("args", args)
        view.assign("session_count", 2)
        view.assign("static_count", 0)
        view.assign("total_count", 2)
        view.render()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_render_with_static_count(self, mock_print):
        args = ArgsMock()
        args.quiet = False
        view = NoteForHiddenView(self.out)
        view.assign("args", args)
        view.assign("session_count", 0)
        view.assign("static_count", 1)
        view.assign("total_count", 1)
        view.render()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_render_quiet(self, mock_print):
        args = ArgsMock()
        args.quiet = True
        view = NoteForHiddenView(self.out)
        view.assign("args", args)
        view.assign("session_count", 2)
        view.assign("static_count", 0)
        view.assign("total_count", 2)
        view.render()
        mock_print.assert_not_called()


class TestProcessesView(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()

    @patch('builtins.print')
    def test_render_processes(self, mock_print):
        processes = [type('P', (), {'pid': 1, 'str_started_ago': '10s', 'username': lambda self: 'u', 'name': lambda self: 'p', 'create_time': lambda: 123})()]
        class Coll(list):
            def sorted(self, k):
                return list(self)
        view = ProcessesView(self.out)
        view.assign('processes', Coll(processes))
        view.render()
        mock_print.assert_called()


class TestPackagesView(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()

    @patch('builtins.print')
    def test_render_packages(self, mock_print):
        packages = [type('P', (), {'name': 'pkg1', 'modified': 1234567890})()]
        view = PackagesView(self.out)
        view.assign('packages', packages)
        view.render()
        mock_print.assert_called()


class TestApplicationsView(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()

    @patch('builtins.print')
    def test_render_applications(self, mock_print):
        apps = [type('A', (), {'name': 'app1', 'type': 'a', 'ignore': False, 'helper': 'h'})()]
        view = ApplicationsView(self.out)
        view.assign('applications', apps)
        view.render()
        mock_print.assert_called()


class TestSystemView(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()

    @patch('builtins.print')
    def test_render_system(self, mock_print):
        view = SystemView(self.out)
        view.assign('python', "3.8.0")
        view.assign('distribution', "test")
        view.assign('package_managers', ["yum"])
        view.assign('init', "systemd")
        view.assign('uptime', "1d")
        view.assign('user', "u")
        view.assign('users', ["u"])
        view.assign('version', "1.0")
        view.assign('rules_count', 1)
        view.assign('applications_count', 1)
        view.render()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_render_system_multiple_users(self, mock_print):
        view = SystemView(self.out)
        view.assign('python', "3.8.0")
        view.assign('distribution', "test")
        view.assign('package_managers', ["yum"])
        view.assign('init', "systemd")
        view.assign('uptime', "1d")
        view.assign('user', "u")
        view.assign('users', ["u1", "u2"])
        view.assign('version', "1.0")
        view.assign('rules_count', 1)
        view.assign('applications_count', 1)
        view.render()
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main()
