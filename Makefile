release: test
	tito tag
	@echo
	@echo Please visit https://github.com/FrostyX/tracer/tags and edit release notes

packages: rpm

test:
	sudo unit2 discover ./tests/

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

