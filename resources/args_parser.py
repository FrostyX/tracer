import argparse

parser = argparse.ArgumentParser(
	prog = 'tracer',
	description='Tracer finds outdated running packages in your system',
)

parser.add_argument('packages',
	nargs='*',
	type=str,
	help='packages that only should be traced'
)

parser.add_argument('-n', '--now',
	dest='now',
	action='store_true',
	help='when there are specified packages, dont look for time of their update. Use "now" instead'
)

args = parser.parse_args()
