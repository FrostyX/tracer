import os
import tempfile
import unittest

from tracer.resources import pycomp

from .__meta__ import *


class TestPycomp(unittest.TestCase):

	def test_py3_flag(self):
		self.assertTrue(pycomp.PY3)

	def test_lru_cache_available(self):
		@pycomp.lru_cache(maxsize=None)
		def add(a, b):
			return a + b
		self.assertEqual(add(1, 2), 3)

	def test_string_io(self):
		buf = pycomp.StringIO()
		buf.write("hello")
		self.assertEqual(buf.getvalue(), "hello")

	def test_load_source(self):
		code = "VALUE = 42\n\ndef value():\n\treturn VALUE\n"
		with tempfile.NamedTemporaryFile('w', suffix='.py',
		                                 delete=False) as f:
			f.write(code)
			path = f.name
		try:
			module = pycomp.load_source('fake_loaded_module', path)
			self.assertEqual(module.VALUE, 42)
			self.assertEqual(module.value(), 42)
			self.assertEqual(module.__name__, 'fake_loaded_module')
		finally:
			os.unlink(path)


if __name__ == '__main__':
	unittest.main()
