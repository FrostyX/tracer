import os
import shutil
from distutils.core import setup
from tracer.version import __version__


if not os.path.exists('build/pip'):
	os.makedirs('build/pip')
shutil.copyfile('bin/tracer.py', 'build/tracer')

setup(
	name='tracer',
	version=__version__,
	author='FrostyX',
	author_email='frostyx@email.cz',
	url='http://tracer-package.com/',
	license='LICENSE',
	description='Finds outdated running applications in your system',
	long_description=open('README.md').read(),

	install_requires=[
		"psutil",
		"BeautifulSoup4",
		"sphinx_rtd_theme",
		"Pygments",
	],

	packages=[
		'tracer',
		'tracer.controllers',
		'tracer.packageManagers',
		'tracer.resources',
		'tracer.views',
		'data',
	],

	scripts=['build/tracer'],

	package_data={'data': [
		'applications.xml',
		'rules.xml',
	]},

)
