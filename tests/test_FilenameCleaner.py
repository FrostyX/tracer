from unittest import TestCase
from tracer.resources.FilenameCleaner import FilenameCleaner


class TestFilenameCleaner(TestCase):
	def setUp(self):
		self.cleaner = FilenameCleaner()

	def test_strip(self):
		self.assertEqual("/lib/libdl.so", self.cleaner.strip("/lib/libdl-2.19.so"))
		self.assertEqual("/lib/libncurses.so", self.cleaner.strip("/lib/libncurses.so.5.9"))
		self.assertEqual("/bin/bash", self.cleaner.strip("/bin/bash"))
		self.assertEqual("/usr/share/wicd/curses/wicd-curses.py", self.cleaner.strip("/usr/share/wicd/curses/wicd-curses.py"))
