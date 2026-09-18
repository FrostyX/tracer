import gettext
import unittest

from tracer.controllers.default import DefaultController
from tracer.resources.applications import Application
from tracer.resources.collections import ApplicationsCollection
from tracer.resources.pycomp import StringIO

from .__meta__ import *

t = gettext.translation('tracer', fallback=True, languages=["en"])
_ = t.ugettext

import tracer.views.default
import tracer.views.helper
import tracer.views.note_for_hidden

tracer.views.default._ = _
tracer.views.helper._ = _
tracer.views.note_for_hidden._ = _

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch


class ArgsMock:
    all = quiet = hooks_only = daemons_only = reboot_only = False
    user = False
    erased = False
    now = None
    timestamp = [None]
    helper = []

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestDefaultController(unittest.TestCase):

    @patch('tracer.controllers.default.Tracer')
    @patch('tracer.controllers.default.DefaultView')
    @patch('tracer.controllers.default.HooksObserver')
    def test_render_with_applications(self, mock_hooks, mock_view, mock_tracer):
        args = ArgsMock()
        apps = ApplicationsCollection([
            Application({"name": "test-app", "type": "application"})
        ])
        
        mock_tracer.return_value.trace_affected.return_value = apps
        mock_tracer.return_value.specified_packages = None
        
        controller = DefaultController(args, None)
        try:
            controller.render()
        except SystemExit:
            pass
        
        mock_view.return_value.render.assert_called_once()

    @patch('tracer.controllers.default.Tracer')
    @patch('tracer.controllers.default.HooksObserver')
    def test_status_code_no_applications(self, mock_hooks, mock_tracer):
        args = ArgsMock()
        apps = ApplicationsCollection([])
        
        mock_tracer.return_value.trace_affected.return_value = apps
        
        controller = DefaultController(args, None)
        code = controller.status_code()
        
        self.assertEqual(code, 0)

    @patch('tracer.controllers.default.Tracer')
    @patch('tracer.controllers.default.HooksObserver')
    def test_status_code_with_applications(self, mock_hooks, mock_tracer):
        args = ArgsMock()
        apps = ApplicationsCollection([
            Application({"name": "test-app", "type": "application"})
        ])
        
        mock_tracer.return_value.trace_affected.return_value = apps
        
        controller = DefaultController(args, None)
        code = controller.status_code()
        
        self.assertEqual(code, 101)

    @patch('tracer.controllers.default.Tracer')
    @patch('tracer.controllers.default.HooksObserver')
    def test_status_code_with_daemons(self, mock_hooks, mock_tracer):
        args = ArgsMock()
        apps = ApplicationsCollection([
            Application({"name": "test-daemon", "type": "daemon"})
        ])
        
        mock_tracer.return_value.trace_affected.return_value = apps
        
        controller = DefaultController(args, None)
        code = controller.status_code()
        
        self.assertEqual(code, 102)

    @patch('tracer.controllers.default.Tracer')
    @patch('tracer.controllers.default.HooksObserver')
    def test_status_code_with_session(self, mock_hooks, mock_tracer):
        args = ArgsMock()
        apps = ApplicationsCollection([
            Application({"name": "test-session", "type": "session"})
        ])
        
        mock_tracer.return_value.trace_affected.return_value = apps
        
        controller = DefaultController(args, None)
        code = controller.status_code()
        
        self.assertEqual(code, 103)

    @patch('tracer.controllers.default.Tracer')
    @patch('tracer.controllers.default.HooksObserver')
    def test_status_code_with_static(self, mock_hooks, mock_tracer):
        args = ArgsMock()
        apps = ApplicationsCollection([
            Application({"name": "test-static", "type": "static"})
        ])
        
        mock_tracer.return_value.trace_affected.return_value = apps
        
        controller = DefaultController(args, None)
        code = controller.status_code()
        
        self.assertEqual(code, 104)

    @patch('tracer.controllers.default.Tracer')
    @patch('tracer.controllers.default.HooksObserver')
    def test_render_helpers(self, mock_hooks, mock_tracer):
        args = ArgsMock()
        apps = ApplicationsCollection([
            Application({"name": "test-app", "type": "application", "helper": "test-helper"})
        ])
        
        mock_tracer.return_value.trace_affected.return_value = apps
        
        controller = DefaultController(args, None)
        
        StringIO()
        with patch('tracer.controllers.default.HelperController') as mock_helper_ctrl:
            mock_helper = MagicMock()
            mock_helper_ctrl.return_value = mock_helper
            
            with patch('tracer.controllers.default.NoteForHiddenView') as mock_note_view:
                mock_note = MagicMock()
                mock_note_view.return_value = mock_note
                
                controller.render_helpers()
                
                mock_helper.print_helper.assert_called_once()


if __name__ == '__main__':
    unittest.main()
