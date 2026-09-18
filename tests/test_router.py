import argparse
import contextlib
import io
import sys
import unittest

from .__meta__ import *

try:
	from unittest.mock import MagicMock, patch
except ImportError:
	from mock import MagicMock, patch

from tracer.resources.router import Router
from tracer.version import __version__


def _args(**overrides):
	values = {'helper': None, 'version': False, 'resource': None,
	          'helpers': False, 'interactive': False, 'erased': False, 'now': False, 'quiet': False, 'all': False, 'user': None, 'timestamp': [None], 'packages': [], 'reboot_only': False, 'daemons_only': False, 'hooks_only': False}
	values.update(overrides)
	return argparse.Namespace(**values)


class TestRouter(unittest.TestCase):

	def test_dispatch_helper(self):
		helper_mod = MagicMock(name='helper_controller_module')
		args = _args(helper='foo')
		packages = ['pkg1']
		with patch.dict(sys.modules, {'tracer.controllers.helper': helper_mod}):
			Router(args, packages).dispatch()
		helper_mod.HelperController.assert_called_once_with(args, packages)
		helper_mod.HelperController.return_value.render.assert_called_once()

	def test_dispatch_version(self):
		buf = io.StringIO()
		with contextlib.redirect_stdout(buf):
			Router(_args(version=True), []).dispatch()
		self.assertEqual(buf.getvalue().strip(), __version__)

	def test_dispatch_resource(self):
		resource_mod = MagicMock(name='resource_controller_module')
		args = _args(resource=['system'])
		with patch.dict(sys.modules, {'tracer.controllers.resource': resource_mod}):
			Router(args, []).dispatch()
		resource_mod.ResourceController.assert_called_once_with(args)
		resource_mod.ResourceController.return_value.render.assert_called_once()

	def _assert_default_call(self, render_method, helpers=False, interactive=False):
		default_mod = MagicMock(name='default_controller_module')
		args = _args(helpers=helpers, interactive=interactive)
		packages = ['pkg1', 'pkg2']
		with patch.dict(sys.modules, {'tracer.controllers.default': default_mod}):
			Router(args, packages).dispatch()
		default_mod.DefaultController.assert_called_once_with(args, packages)
		getattr(default_mod.DefaultController.return_value,
		        render_method).assert_called_once()

	def test_dispatch_default_plain(self):
		self._assert_default_call('render')

	def test_dispatch_default_helpers(self):
		self._assert_default_call('render_helpers', helpers=True)

	def test_dispatch_default_interactive(self):
		self._assert_default_call('render_interactive', interactive=True)

	def test_dispatch_with_no_packages(self):
		helper_mod = MagicMock(name='helper_controller_module')
		args = _args(helper='foo')
		packages = []
		with patch.dict(sys.modules, {'tracer.controllers.helper': helper_mod}):
			Router(args, packages).dispatch()
		helper_mod.HelperController.assert_called_once_with(args, packages)

	def test_dispatch_with_multiple_packages(self):
		helper_mod = MagicMock(name='helper_controller_module')
		args = _args(helper='foo')
		packages = ['pkg1', 'pkg2', 'pkg3']
		with patch.dict(sys.modules, {'tracer.controllers.helper': helper_mod}):
			Router(args, packages).dispatch()
		helper_mod.HelperController.assert_called_once_with(args, packages)

	def test_dispatch_with_helper_none(self):
		helper_mod = MagicMock(name='helper_controller_module')
		args = _args(helper=None)
		packages = ['pkg1']
		with patch.dict(sys.modules, {'tracer.controllers.helper': helper_mod}):
			with self.assertRaises(SystemExit):
				Router(args, packages).dispatch()


if __name__ == '__main__':
	unittest.main()
