release:
	tito tag

packages: rpm


#
# RPM
#

rpm: rpm-copr

rpm-test:
	tito build --rpm --test

rpm-try:
	tito build --rpm --test --install

rpm-copr:
	tito release copr-frostyx

rpm-copr-test:
	tito release copr-frostyx-test

