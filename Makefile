.PHONY: doc

DESTDIR=build

help:
	@echo "Please use \`make <target>' where <target> is one of these"
	@echo "* General targets"
	@echo "    test           to run all automated tests for this project"
	@echo "    doc            to build documentation"
	@echo "    man            to build manpage"
	@echo "    release        to release new minor version"
	@echo "    packages       to build packages for all distributions"
	@echo ""
	@echo "* Fedora targets"
	@echo "    rpm            to build fedora package"
	@echo "    rpm-test       to build fedora package locally"
	@echo "    rpm-try        to build fedora package and install it"
	@echo "    rpm-copr       to build fedora package through copr"
	@echo "    rpm-fedora     to build fedora package through koji"
	@echo ""
	@echo "* Localization targets"
	@echo "    pot            to generate .pot file from the code"
	@echo "    tx-push        to push .pot file to transifex.com"
	@echo "    tx-pull        to pull translated .po files from transifex.com"
	@echo "    mo             to build .mo files"

release: test
	tito tag
	@echo
	@echo Please visit https://github.com/FrostyX/tracer/tags and edit release notes

packages: rpm

test:
	python -m pytest -v tests

doc:
	@echo Move to ./doc/ directory and run
	@echo     make help

man:
	make --directory=doc man


#
# Localizations
#

pot:
	cd po && find ../tracer -iname "*.py" | \
	xargs xgettext --from-code=UTF-8 --output=tracer.pot

tx-push: pot
	tx push -s

tx-pull:
	tx pull -s

mo:
	mkdir -p $(DESTDIR)/locale/cs/LC_MESSAGES/
	@# @TODO Rewrite next line to scan all languages
	msgcat po/cs.po | msgfmt -o $(DESTDIR)/locale/cs/LC_MESSAGES/tracer.mo -


#
# RPM
#

rpm: rpm-copr

rpm-test:
	tito build --rpm --test

rpm-try:
	tito build --rpm --test --install

rpm-copr:
	tito release copr

rpm-copr-test:
	tito release copr-test

rpm-fedora:
	tito release fedora-git
