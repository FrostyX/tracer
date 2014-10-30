from __meta__ import *
import tracer.resources.lang as Lang
import os

class TestLang(unittest.TestCase):

	def test_locale_implementation(self):
		default_locale = Lang._locale(Lang.DEFAULT_LANG)
		for lang in self._languages():
			locale = Lang._locale(lang)

			for key, value in default_locale.items():
				self.assertIn(key, locale, "Locale '{0}' doesn't implement '{1}' label".format(lang, key))

			for key, value in locale.items():
				self.assertIn(key, default_locale, "Locale '{0}' shouldn't implement '{1}' label".format(lang, key))

	def _languages(self):
		languages = []
		for file in os.listdir(Lang._LANG_PATH):
			file = file.split(".")[0]
			if file.startswith("__") or file.endswith("__"):
				continue

			languages.append(file)
		return set(languages)


if __name__ == '__main__':
	unittest.main()
