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
		self.assertEqual("/usr/bin/gvim", self.cleaner.strip("/usr/bin/gvim#new (deleted)"))

		self.assertEqual("/usr/lib64/kde4/kded_networkmanagement.so",
			self.cleaner.strip("/usr/lib64/kde4/kded_networkmanagement.so;53c7cd86")
		)

		self.assertEqual("/usr/lib64/firefox/plugin-container",
			 self.cleaner.strip("/usr/lib64/firefox/plugin-container.#prelink#.N3n7Rk (deleted)")
		)
