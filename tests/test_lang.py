from .__meta__ import *
import tracer.resources.lang as lang
import os


class TestLang(unittest.TestCase):

	def test_provide_underscore_function(self):
		self.assertTrue(hasattr(lang, '_'))


if __name__ == '__main__':
	unittest.main()
