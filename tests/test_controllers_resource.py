import unittest

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from tracer.controllers.resource import ResourceController

from .__meta__ import *


class ArgsMock:
    resource = []
    timestamp = [None]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestResourceController(unittest.TestCase):

    def setUp(self):
        self.args = ArgsMock()

    @patch('tracer.controllers.resource.ProcessesView')
    @patch('tracer.controllers.resource.Processes')
    def test_render_processes(self, mock_processes, mock_view):
        args = ArgsMock(resource=["processes"])
        
        mock_processes.all.return_value = []
        
        controller = ResourceController(args)
        controller.render()
        
        mock_view.return_value.render.assert_called_once()

    @patch('tracer.controllers.resource.PackagesView')
    @patch('tracer.controllers.resource.System')
    def test_render_packages(self, mock_system, mock_view):
        args = ArgsMock(resource=["packages"], timestamp=[1234567890])
        
        mock_package_manager = MagicMock()
        mock_package_manager.packages_newer_than.return_value = []
        mock_system.package_manager.return_value = mock_package_manager
        mock_system.boot_time.return_value = 1234567890
        
        controller = ResourceController(args)
        controller.render()
        
        mock_view.return_value.render.assert_called_once()

    @patch('tracer.controllers.resource.RulesView')
    @patch('tracer.controllers.resource.Rules')
    def test_render_rules(self, mock_rules, mock_view):
        args = ArgsMock(resource=["rules"])
        
        mock_rules.all.return_value = []
        
        controller = ResourceController(args)
        controller.render()
        
        mock_view.return_value.render.assert_called_once()

    @patch('tracer.controllers.resource.ApplicationsView')
    @patch('tracer.controllers.resource.Applications')
    def test_render_applications(self, mock_apps, mock_view):
        args = ArgsMock(resource=["applications"])
        
        mock_apps.all.return_value = []
        
        controller = ResourceController(args)
        controller.render()
        
        mock_view.return_value.render.assert_called_once()

    @patch('tracer.controllers.resource.SystemView')
    @patch('tracer.controllers.resource.psutil')
    @patch('tracer.controllers.resource.System')
    @patch('tracer.controllers.resource.Rules')
    @patch('tracer.controllers.resource.Applications')
    def test_render_system(self, mock_apps, mock_rules, mock_system, mock_psutil, mock_view):
        args = ArgsMock(resource=["system"])
        
        mock_system.python_version.return_value = "3.8.0"
        mock_system.distribution.return_value = "test-distro"
        mock_system.user.return_value = "testuser"
        
        mock_package_manager = MagicMock()
        mock_package_manager.names.return_value = ["yum", "dnf"]
        mock_system.package_manager.return_value = mock_package_manager
        
        mock_psutil.get_users.return_value = [MagicMock(name="user1")]
        
        mock_rules.all.return_value = []
        mock_apps.all.return_value = []
        
        controller = ResourceController(args)
        controller.render()
        
        mock_view.return_value.render.assert_called_once()


if __name__ == '__main__':
    unittest.main()
