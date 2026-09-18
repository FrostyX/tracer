import unittest
from tracer.resources.SystemdDbus import SystemdDbus


class TestSystemdDbus(unittest.TestCase):

	def test_init(self):
		dbus = SystemdDbus()
		self.assertIsNotNone(dbus)


if __name__ == '__main__':
	unittest.main()
