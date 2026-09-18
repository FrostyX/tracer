import gettext
import unittest

import tracer
from tracer.controllers.helper import HelperController
from tracer.resources.pycomp import StringIO

from .__meta__ import *

t = gettext.translation('tracer', fallback=True, languages=["en"])
_ = t.ugettext

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

tracer.views.helper._ = _


class ArgsMock:
    helper = []
    now = None
    verbose = 0

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestHelperController(unittest.TestCase):

    def setUp(self):
        self.args = ArgsMock()

    @patch('tracer.controllers.helper.Tracer')
    @patch('tracer.controllers.helper.System')
    @patch('tracer.controllers.helper.HelperView')
    def test_render_with_helper(self, mock_view, mock_system, mock_tracer):
        args = ArgsMock(helper=["test-app"])
        
        mock_app = MagicMock()
        mock_app.name = "test-app"
        mock_app.instances = [MagicMock()]
        mock_app.instances[0].pid = 1234
        
        mock_tracer.return_value.now = None
        mock_tracer.return_value.specified_packages = None
        
        with patch('tracer.controllers.helper.Applications') as mock_apps:
            mock_apps.find.return_value = mock_app
            
            controller = HelperController(args)
            controller.render()

    @patch('tracer.controllers.helper.Tracer')
    @patch('tracer.controllers.helper.System')
    @patch('tracer.controllers.helper.HelperView')
    def test_print_helper_with_instances(self, mock_view, mock_system, mock_tracer):
        args = ArgsMock()
        
        mock_app = MagicMock()
        mock_app.name = "test-app"
        mock_app.instances = [MagicMock()]
        mock_app.instances[0].pid = 1234
        
        mock_package = MagicMock()
        mock_package.load_info = MagicMock()
        
        mock_tracer.return_value.now = None
        mock_tracer.return_value.specified_packages = None
        
        with patch('tracer.controllers.helper.System') as mock_sys:
            mock_sys.package_manager.return_value.provided_by.return_value = mock_package
            
            with patch('tracer.controllers.helper.Tracer') as mock_tracer_cls:
                mock_tracer_instance = MagicMock()
                mock_tracer_cls.return_value = mock_tracer_instance
                mock_tracer_instance.trace_application.return_value = []
                
                controller = HelperController(args)
                controller.print_helper(mock_app, args)

    @patch('tracer.controllers.helper._')
    def test_print_helper_without_instances(self, mock_underscore):
        args = ArgsMock()
        
        mock_app = MagicMock()
        mock_app.name = "test-app"
        mock_app.instances = []
        
        out = StringIO()
        controller = HelperController(args, out)
        controller.print_helper(mock_app, args)
        
        mock_underscore.assert_called()


if __name__ == '__main__':
    unittest.main()
