from .__meta__ import *
from tracer.hooks import HooksObserver, match

called = None

@match("app1")
def hook_dummy():
	global called
	called = "dummy"

@match(["app2", "app3"])
def hook_dummy_list():
	global called
	called = "dummy_list"

@match("foo")
def hook_dummy_append1():
	global called
	called.append("foo")

@match("bar")
def hook_dummy_append2():
	global called
	called.append("bar")


class TestHooks(unittest.TestCase):

	def setUp(self):
		self.observer = HooksObserver()
		global called
		called = None

	def test_hook(self):
		self.observer("app1")
		self.assertEqual(called, "dummy")

		self.observer("app2")
		self.assertEqual(called, "dummy_list")

		self.observer("app3")
		self.assertEqual(called, "dummy_list")

	def test_hooks_list(self):
		global called
		called = []
		self.observer("foo")
		self.observer("bar")
		self.assertListEqual(called, ["foo", "bar"])

	def test_undefined_hook(self):
		global called
		self.observer("undefined")
		self.assertIsNone(called)



if __name__ == '__main__':
	unittest.main()
