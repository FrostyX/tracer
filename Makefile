release:
	tito tag

packages: rpm


#
# RPM
#

rpm: rpm-copr

rpm-test:
	tito build --rpm --test

rpm-copr:
	tito release copr-frostyx

rpm-copr-test:
	tito release copr-frostyx-test

