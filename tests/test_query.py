from .__meta__ import *
from tracer.query import Query, Lazy


class TestQuery(unittest.TestCase):

	def setUp(self):
		self.query = Query(tracer=TracerMock)

	def test_affected_applications(self):
		apps_query = self.query.affected_applications()
		self.assertIsInstance(apps_query, Lazy)
		self.assertTrue(hasattr(apps_query, "get"))
		self.assertListEqual(list(apps_query.get()), ["A", "B", "C"])


class TracerMock(object):
	def __init__(self, *args):
		pass

	def trace_affected(self, user=None):
		return ["A", "B", "C"]



if __name__ == '__main__':
	unittest.main()
