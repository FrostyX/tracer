Name:		tracer
Version:	0.6.10
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
BuildRequires:	python3-devel
BuildRequires:	asciidoc
BuildRequires:	gettext

%package -n python2-%{name}
Summary:		%{summary}
Provides:		%{name} = %{version}-%{release}
BuildRequires:	python-sphinx
BuildRequires:	python-beautifulsoup4
BuildRequires:	python-psutil
BuildRequires:	python-pygments
BuildRequires:	python-lxml
Requires:	rpm-python
Requires:	python
Requires:	python-beautifulsoup4
Requires:	python-psutil
%{?python_provide:%python_provide python2-%{name}}

%package -n python3-%{name}
Summary:		%{summary}
BuildRequires:	python3-sphinx
BuildRequires:	python3-beautifulsoup4
BuildRequires:	python3-psutil
BuildRequires:	python3-pygments
BuildRequires:	python3-lxml
Requires:	rpm-python3
Requires:	python3
Requires:	python3-beautifulsoup4
Requires:	python3-psutil
%{?python_provide:%python_provide python3-%{name}}


%description
Tracer determines which applications use outdated files and prints them. For
special kind of applications such as services or daemons, it suggests a standard
command to restart it. Detecting whether file is outdated or not is based on a
simple idea. If application has loaded in memory any version of a file
which is provided by any package updated since system was booted up, tracer
consider this application as outdated.

%description -n python2-%{name}
Tracer determines which applications use outdated files and prints them. For
special kind of applications such as services or daemons, it suggests a standard
command to restart it. Detecting whether file is outdated or not is based on a
simple idea. If application has loaded in memory any version of a file
which is provided by any package updated since system was booted up, tracer
consider this application as outdated.

%description -n python3-%{name}
Tracer determines which applications use outdated files and prints them. For
special kind of applications such as services or daemons, it suggests a standard
command to restart it. Detecting whether file is outdated or not is based on a
simple idea. If application has loaded in memory any version of a file
which is provided by any package updated since system was booted up, tracer
consider this application as outdated.


%prep
%setup -q


%build
%py2_build
%py3_build
make %{?_smp_mflags} man
sed "s/\/usr\/bin\/python/\/usr\/bin\/python2/" bin/tracer.py > bin/tracer-2
sed "s/\/usr\/bin\/python/\/usr\/bin\/python3/" bin/tracer.py > bin/tracer-3
chmod +x bin/tracer-2 bin/tracer-3


%install
# @TODO use following macros
# %%py2_install
# %%py3_install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/tracer
mkdir -p %{buildroot}/%{_mandir}/man8
mkdir -p %{buildroot}/%{python2_sitelib}/tracer
mkdir -p %{buildroot}/%{python3_sitelib}/tracer

cp -a bin/tracer-2 %{buildroot}/%{_bindir}/
cp -a bin/tracer-3 %{buildroot}/%{_bindir}/
ln -s %{_bindir}/tracer-2 %{buildroot}/%{_bindir}/tracer

cp -a data/* %{buildroot}/%{_datadir}/tracer/
cp -ar tracer/* tests %{buildroot}/%{python2_sitelib}/tracer/
cp -ar tracer/* tests %{buildroot}/%{python3_sitelib}/tracer/
install -m644 doc/build/man/tracer.8 %{buildroot}/%{_mandir}/man8/
make DESTDIR=%{buildroot}/usr/share/ mo
%find_lang %{name}


%files -n python2-%{name} -f %{name}.lang
%license LICENSE
%doc README.md
%{python2_sitelib}/tracer
%{_bindir}/tracer-2
%{_bindir}/tracer
%{_datadir}/tracer/
%doc %{_mandir}/man8/tracer.8*

%files -n python3-%{name} -f %{name}.lang
%license LICENSE
%doc README.md
%{python3_sitelib}/tracer
%{_bindir}/tracer-3
%{_datadir}/tracer/
%doc %{_mandir}/man8/tracer.8*


%changelog
* Mon Aug 01 2016 Jakub Kadlčík <frostyx@email.cz> 0.6.10-1
- Split RPM package into separate python2 and python3 subpackages
  (frostyx@email.cz)
- Fix localization errors from exception texts (frostyx@email.cz)
- Release for F23, F24 and rawhide (frostyx@email.cz)

* Thu Apr 14 2016 Jakub Kadlčík <frostyx@email.cz> 0.6.9-1
- Declare official python3 support (frostyx@email.cz)

* Wed Feb 17 2016 Jakub Kadlčík <frostyx@email.cz> 0.6.8-1
- Fix /etc/os-release issues on CentOS (tingping@tingping.se)
- Add support for Arch Linux (tingping@tingping.se)

* Wed Dec 16 2015 Jakub Kadlčík <frostyx@email.cz> 0.6.7-1
- Recognize root user from -r or --root arguments; Fix #51 (frostyx@email.cz)
- Don't force root, rather catch exceptions; See #49 (frostyx@email.cz)
- Use non-zero exit codes to indicate various situations; See #46
  (frostyx@email.cz)
- Fix unicode error from raw_input (RhBug:1279409) (frostyx@email.cz)
- Change distro name retrieval to try to  read /etc/os-release first
  (ngompa13@gmail.com)

* Tue Sep 08 2015 Jakub Kadlčík <frostyx@email.cz> 0.6.6-1
- Release new packages even for Fedora 23 (frostyx@email.cz)

* Sat Aug 22 2015 Jakub Kadlčík <frostyx@email.cz> 0.6.5-1
- Fix OSError from os.getlogin() (RhBug:1251352) (frostyx@email.cz)

* Sun Aug 16 2015 Jakub Kadlčík <frostyx@email.cz> 0.6.4-1
- Catch NoSuchProcess to fix #43 (RhBug:1215561) (frostyx@email.cz)

* Mon Aug 10 2015 Jakub Kadlčík <frostyx@email.cz> 0.6.3-1
- Add compatibility layer for psutil.pids(); Fix 1251687
- Don't release for F20 anymore

* Wed Aug 05 2015 Jakub Kadlčík <frostyx@email.cz> 0.6.2-1
- Add --daemons-only and --hooks-only into manpage (frostyx@email.cz)

* Sun Aug 02 2015 Jakub Kadlčík <frostyx@email.cz> 0.6.1-1
- Print unique package names in Affected by section; Fix #36 (frostyx@email.cz)
- Implement services autodetect functionality (frostyx@email.cz)
- Add equivalent --services-only and --daemons-only arguments
  (frostyx@email.cz)
- Fix testing views on non-english systems (frostyx@email.cz)
- Fix compatibility issues on psutil-3; Fix #41 (frostyx@email.cz)

* Mon Jul 27 2015 Jakub Kadlčík <frostyx@email.cz> 0.6.0-1
- Fix warning on new BeautifulSoup4-4.4.0 (RhBug:1240115) (frostyx@email.cz)
- Add block with uninstalled packages (frostyx@email.cz)
- Find provided files only once per package name Significant performance
  improvement (frostyx@email.cz)
- Implement hooks functionality (frostyx@email.cz)

* Mon May 18 2015 Jakub Kadlčík <frostyx@email.cz> 0.5.9-1
- Pick the most recent sqlite database (RhBug:1214961) (frostyx@email.cz)
- Obsolete positional arguments with --packages (frostyx@email.cz)
- Implement application rename functionality (frostyx@email.cz)
- Add LXDE applications (frostyx@email.cz)
- Add Xfce applications (frostyx@email.cz)
- Add MATE applications (frostyx@email.cz)
- Print if application affects something else (frostyx@email.cz)
- Add Czech translation (frostyx@email.cz)
- Use localization system and transifex
- Print python version in system view (frostyx@email.cz)
- Implement Python3 support
- Add setup.py script for pip (frostyx@email.cz)
- Add dependency to 'rpm-python' (frostyx@email.cz)
- Add small API

* Mon Feb 23 2015 Jakub Kadlčík <frostyx@email.cz> 0.5.8-1
- There is children instead of get_children in psutil2 (frostyx@email.cz)
- ProcessWrapper provides api of new version, so use it (frostyx@email.cz)
- Get summary instead of description; Fix mistake from dfae2b6

* Fri Feb 20 2015 Jakub Kadlčík <frostyx@email.cz> 0.5.7-1
- Update informations about DNF plugin (frostyx@email.cz)
- Prevent traceback when deleted user; See #33 (frostyx@email.cz)
- Rename 'print' action to 'return' and set it to rules (frostyx@email.cz)
- Add ProcessWrapper to ensure psutil compatibility (frostyx@email.cz)
- Drop dnf plugin (moved to dnf-plugins-extras) (i.gnatenko.brain@gmail.com)
- Use rpm-python library instead of calling rpm commands (i.gnatenko.brain@gmail.com)
- Use Yum as package manager on CentOS (frostyx@email.cz)

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

