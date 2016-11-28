import os
import shutil
from distutils.core import setup
from tracer.version import __version__


if not os.path.exists('build/pip'):
	os.makedirs('build/pip')
shutil.copyfile('bin/tracer.py', 'build/tracer')


with open("requirements.txt") as f:
	install_requires = f.read().splitlines()

data_files = []
if hasattr(os, 'geteuid') and os.geteuid() == 0:
    data_files = [('/etc/bash_completion.d', ['scripts/tracer.bash_completion']),]

setup(
	name='tracer',
	version=__version__,
	author='FrostyX',
	author_email='frostyx@email.cz',
	url='http://tracer-package.com/',
	license='LICENSE',
	description='Finds outdated running applications in your system',
	long_description=open('README.md').read(),
	install_requires=install_requires,
        data_files=data_files,

	packages=[
		'tracer',
		'tracer.controllers',
		'tracer.packageManagers',
		'tracer.resources',
		'tracer.views',
		'tracer.views.resource',
		'data',
	],

	scripts=['build/tracer'],

	package_data={'data': [
		'applications.xml',
		'rules.xml',
	]},
)
