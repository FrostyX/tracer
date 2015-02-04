Name:		tracer
Version:	0.5.6
Release:	1%{?dist}
Summary:	Finds outdated running applications in your system

BuildArch:	noarch
Group:		Applications/System
License:	GPLv2
URL:		http://tracer-package.com/
# Sources can be obtained by
# git clone git@github.com:FrostyX/tracer.git
# cd tracer
# tito build --tgz
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	python2-devel
BuildRequires:	asciidoc
BuildRequires:	python-sphinx
BuildRequires:	libxslt
Requires:	python
Requires:	python-beautifulsoup4
Requires:	python-psutil

%description
Tracer determines which applications use outdated files and prints them. For
special kind of applications such as services or daemons, it suggests a standard
command to restart it. Detecting whether file is outdated or not is based on a
simple idea. If application has loaded in memory any version of a file
which is provided by any package updated since system was booted up, tracer
consider this application as outdated.

%prep
%setup -q


%build
make %{?_smp_mflags} man


%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/tracer
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}/%{python2_sitelib}/tracer
cp -a bin/tracer.py %{buildroot}/%{_bindir}/tracer
cp -a data/* %{buildroot}/%{_datadir}/tracer/
cp -ar tracer/* tests %{buildroot}/%{python2_sitelib}/tracer/
install -m644 doc/build/man/tracer.8 %{buildroot}/%{_mandir}/man8/


%files
%doc LICENSE README.md
%doc %{_mandir}/man8/tracer.8*
%{_bindir}/tracer
%{_datadir}/tracer/
%{python2_sitelib}/tracer/

%changelog
* Thu Jan 01 2015 Jakub Kadlčík <frostyx@email.cz> 0.5.6-1
- Sort applications in interactive controler To fix the issue that [number]
  doesn't correspond to printed application (frostyx@email.cz)
- Strip .#prelink#. from filenames; See #19 (frostyx@email.cz)
- Add argument forgotten in dcf0178 (frostyx@email.cz)

* Wed Dec 31 2014 Jakub Kadlčík <frostyx@email.cz> 0.5.5-1
- On Fedora, use DNF and YUM at once; (RhBug:1168807) (frostyx@email.cz)
- Return empty collection if DNF wasn't used yet; (RhBug:1168807)
  (frostyx@email.cz)
- Rewrite default view using blocks Print blocks of session and static
  applications when `-a`; Fix #23 (frostyx@email.cz)
- Implement helper arguments functionality; Close #21 (frostyx@email.cz)
- Make set step by step; Fix #25 (frostyx@email.cz)
- Don't run tracer when uninstalling it; Fix #24 (frostyx@email.cz)
- Add fedora-git releaser (frostyx@email.cz)
- Implement '--show-resource' parameter (frostyx@email.cz)
- Use parallel make (frostyx@email.cz)

* Thu Oct 30 2014 Jakub Kadlčík <frostyx@email.cz> 0.5.4-1
- Rename DNF plugin to dnf-plugin-tracer (frostyx@email.cz)
- Trace affected applications instead of processes (frostyx@email.cz)
- Rewrite the description (frostyx@email.cz)

* Sat Oct 25 2014 Jakub Kadlčík <frostyx@email.cz> 0.5.3-1
- Prevent traceback from theme (frostyx@email.cz)

* Sat Oct 25 2014 Jakub Kadlčík <frostyx@email.cz> 0.5.2-1
- Add manpage (8) (frostyx@email.cz)
- Print helpers for all arguments passed to --show (frostyx@email.cz)

* Sat Oct 18 2014 Jakub Kadlčík <frostyx@email.cz> 0.5.1-1
- Correct sentenses in note; Fix #18 (frostyx@email.cz)
- Dont automatically assume 'sudo'; Fix #17 (frostyx@email.cz)
- Sort applications alphabetically; Fix #16 (frostyx@email.cz)

* Wed Oct 15 2014 Jakub Kadlčík <frostyx@email.cz> 0.5.0-1
- Add sphinx documentation (frostyx@email.cz)
- Add support for Travis CI and coveralls (frostyx@email.cz)
- Print more lines of the state in helper (frostyx@email.cz)
- Implement the application's 'ignore' property (frostyx@email.cz)
- Return also list of packages affecting process children (frostyx@email.cz)
- Dont print how to restart if application actually doesnt need it
- Print sudo in helpers (frostyx@email.cz)
- In DNF plugin print command for more informations (frostyx@email.cz)
- Add timestamp argument (frostyx@email.cz)
- UX improvements - immediately print how to restart (frostyx@email.cz)
- Implement loading user-defined rules (frostyx@email.cz)
- Implement loading user-defined applications (frostyx@email.cz)
- Print 'how to restart' only when it has been set (frostyx@email.cz)
- Use FilenameCleaner instead of _filename_without_version (frostyx@email.cz)
- Deal with interpreted processes (frostyx@email.cz)
- Add property 'category' to package (frostyx@email.cz)
- Prevent from Ctrl+C traceback; Fix #14 (frostyx@email.cz)
- Fix #new problem in process's exe; Related with 6c7bc46 (frostyx@email.cz)
- Use Router to call the right controller and its method (frostyx@email.cz)
- Recognize between locked database and insufficient permissions
  (frostyx@email.cz)
- Specify program path to avoid conflict; Fix #12 (frostyx@email.cz)
- Refactor applications as objects instead of dicts (frostyx@email.cz)
- Fix lot of PEP warnings (frostyx@email.cz)
- Use MVC architecture (frostyx@email.cz)

* Fri Aug 08 2014 Jakub Kadlčík <frostyx@email.cz> 0.4.4-1
- Refactor determining whether application is running or not (frostyx@email.cz)
- Add verbose mode (frostyx@email.cz)
- Print 'affected by' section only in verbose mode (frostyx@email.cz)
- In second verbose level print even affected files (frostyx@email.cz)

* Mon Jul 28 2014 Jakub Kadlčík <frostyx@email.cz> 0.4.3-1
- Run tests before releasing new version (frostyx@email.cz)
- Add 'make test' target (frostyx@email.cz)
- Dont filter processes files (frostyx@email.cz)
- Print 'affected by' section in helpers (frostyx@email.cz)

* Mon Jul 21 2014 Jakub Kadlčík <frostyx@email.cz> 0.4.2-1
- Dont try to get list of files provided by non-installed RPM package
  (frostyx@email.cz)
- Print user-friendly exception when package database is locked
  (frostyx@email.cz)

* Fri Jul 18 2014 Jakub Kadlčík <frostyx@email.cz> 0.4.1-1
- Print 'You should restart' above processes list (frostyx@email.cz)
- Merge pull request #10 from xsuchy/pr-1 (frostyx@email.cz)
- Fix details in tracer.spec (frostyx@email.cz)
- Print 'how to restart' for session and static applications (frostyx@email.cz)
- Add 'tracer --helpers' parameter to list helpers (frostyx@email.cz)
* Tue Jul 08 2014 Jakub Kadlčík <frostyx@email.cz> 0.4.0-1
- new package built with tito

