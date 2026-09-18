import unittest
from tracer.resources.processes import Process


class TestProcessMethods(unittest.TestCase):

	def test_process_wrapper_rebuild_cache(self):
		# Just test that rebuild_cache doesn't raise an error
		p = Process(1)
		p.rebuild_cache()
		self.assertTrue(hasattr(p, '_procdict'))

	def test_process_wrapper_children(self):
		p = Process(1)
		children = p.children()
		self.assertIsInstance(children, list)

	def test_process_wrapper_children_recursive(self):
		p = Process(1)
		children = p.children(recursive=True)
		self.assertIsInstance(children, list)

	def test_process_safe_isfile_true(self):
		# Test with /bin/ls which should exist
		result = Process.safe_isfile('/bin/ls')
		self.assertTrue(result)

	def test_process_safe_isfile_false(self):
		result = Process.safe_isfile('/nonexistent/path/file')
		self.assertFalse(result)


if __name__ == '__main__':
	unittest.main()
