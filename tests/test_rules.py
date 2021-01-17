from .__meta__ import *
from tracer.resources.rules import Rules, Rule


class TestRules(unittest.TestCase):

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


if __name__ == '__main__':
	unittest.main()
