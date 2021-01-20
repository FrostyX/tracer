from .__meta__ import *
from tracer.paths import DATA_DIR
from tracer.resources.rules import Rules, Rule

try:
	from unittest.mock import patch, mock_open
	builtins_open = "builtins.open"
except:
	from mock import patch, mock_open
	builtins_open = "__builtin__.open"


class TestRules(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.DEFINITIONS = [x for x in Rules.DEFINITIONS
						   if x.startswith(DATA_DIR)]

	def setUp(self):
		Rules.DEFINITIONS = self.DEFINITIONS
		Rules._rules = None

	def test_rules_types(self):
		for rule in Rules.all():
			self.assertIsInstance(rule, Rule)

	def test_rules_attributes(self):
		i = 1
		for r in Rules.all():
			if ("name" not in r) or ("action" not in r):
				self.fail("Missing attributes in rule #" + str(i))

			if r.action not in Rules.ACTIONS.values():
				self.fail("Unknown action in rule: " + r.name)

			if len(r) > 2:
				self.fail("Unsupported attributes in rule: " + r.name)

			i += 1

	def test_rules_duplicity(self):
		rules = Rules.all()
		for r in rules:
			if rules.count(r) > 1:
				self.fail("Duplicate rules for: " + r.name)

	def test_app_with_no_rule(self):
		self.assertIsNone(Rules.find("NON_EXISTING_APPLICATION"))

	def test_representations(self):
		rule = Rule({"name": "foo"})
		self.assertEqual(str(rule), "<Rule: foo>")
		self.assertEqual(repr(rule), "<Rule: foo>")

	def test_update(self):
		r1 = Rule({"name": "foo", "action": "bar"})
		r2 = Rule({"name": "foo", "action": "baz"})

		r1.update(r2)
		self.assertEqual(r1.action, "baz")

	def test_load(self):
		"""
		Test parsing a single XML file with rules
		"""
		Rules.DEFINITIONS = ["whatever-file.xml"]
		data = (
			"<rules>"
			"    <rule name='foo' action='return' />"
			"    <rule name='bar' />"
			"</rules>"
		)
		with patch(builtins_open, mock_open(read_data=data)):
			rules = Rules.all()
			self.assertEqual(len(rules), 2)
			self.assertTrue(all([isinstance(x, Rule) for x in rules]))
			self.assertEqual(rules[0].name, "foo")
			self.assertEqual(rules[0].action, "return")
			self.assertEqual(rules[1].name, "bar")

	def _count(self, app_name, apps):
		count = 0
		for a in apps:
			if a.name == app_name:
				count += 1
		return count


if __name__ == '__main__':
	unittest.main()
