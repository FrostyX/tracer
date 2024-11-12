%if 0%{?rhel}

%if 0%{?rhel} <= 7
%bcond_without python2
%bcond_with python3
%bcond_with suggest
%else
%bcond_with python2
%bcond_without python3
%bcond_without suggest
%endif

%else
%bcond_with python2
%bcond_without python3
%bcond_without suggest
%endif

Name:       tracer
Version:    1.2
Release:    1%{?dist}
Summary:    Finds outdated running applications in your system

BuildArch:  noarch
License:    GPL-2.0-or-later
URL:        http://tracer-package.com/
# Sources can be obtained by
# git clone git@github.com:FrostyX/tracer.git
# cd tracer
# tito build --tgz
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  asciidoc
BuildRequires:  gettext
BuildRequires:  make

%global _description \
Tracer determines which applications use outdated files and prints them. For\
special kind of applications such as services or daemons, it suggests a standard\
command to restart it. Detecting whether file is outdated or not is based on a\
simple idea. If application has loaded in memory any version of a file\
which is provided by any package updated since system was booted up, tracer\
consider this application as outdated.

%description %{_description}

%package common
Summary:        Common files for %{name}

%description common
%{summary}.

%if %{with python2}
%package -n python2-%{name}
Summary:        %{summary}
%if ! %{with python3}
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} <= 0.6.11
%endif
BuildRequires:  python2-devel
BuildRequires:  python2-sphinx
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  rpm-python
BuildRequires:  python2-mock
Requires:       rpm-python
%else
BuildRequires:  python2-rpm
Requires:       python2-rpm
%endif
BuildRequires:  python2-pytest
BuildRequires:  python2-psutil
BuildRequires:  python2-six
BuildRequires:  dbus-python
BuildRequires:  python2-distro
BuildRequires:  python2-backports-functools_lru_cache
Requires:       dbus-python
Requires:       python2-psutil
Requires:       python2-future
Requires:       python2-six
Requires:       python2-distro
Requires:       python2-backports-functools_lru_cache
Requires:       %{name}-common = %{version}-%{release}
%if %{with suggest}
Suggests:       python-argcomplete
%else
Requires:       python-argcomplete
%endif
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name} %{_description}

Python 2 version.
%endif

%if %{with python3}
%package -n python3-%{name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-pytest
BuildRequires:  python3-psutil
BuildRequires:  python3-six
BuildRequires:  python3-dbus
BuildRequires:  python3-rpm
BuildRequires:  python3-distro
BuildRequires:  python3-setuptools
%if 0%{?fedora}
BuildRequires:  python3-libdnf5
%endif
Requires:       python3-rpm
Requires:       python3-psutil
Requires:       python3-dbus
Requires:       python3-six
Requires:       python3-distro
Requires:       %{name}-common = %{version}-%{release}
%if 0%{?fedora}
Requires:       python3-libdnf5
%endif
%if %{with suggest}
Suggests:       python3-argcomplete
%else
Requires:       python3-argcomplete
%endif
%{?python_provide:%python_provide python3-%{name}}
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} <= 0.6.11

%description -n python3-%{name} %{_description}

Python 3 version.
%endif

%prep
%setup -q
%if %{with python2}
sed -i -e '1s|^#!.*$|#!%{__python2}|' bin/%{name}.py
%endif

%if %{with python3}
sed -i -e '1s|^#!.*$|#!%{__python3}|' bin/%{name}.py
%endif

%build
%if %{with python2}
%py2_build
%endif

%if %{with python3}
%py3_build
%endif
make %{?_smp_mflags} man

%check
%if %{with python3}
python3 -m pytest -v tests
%else
python2 -m pytest -v tests
%endif

%install
# @TODO use following macros
# %%py2_install
# %%py3_install

mkdir -p %{buildroot}%{_datadir}/%{name}/
cp -a data/* %{buildroot}%{_datadir}/%{name}/

%if %{with python2}
mkdir -p %{buildroot}%{python2_sitelib}/%{name}/
cp -ar %{name}/* tests %{buildroot}%{python2_sitelib}/%{name}/
%endif

%if %{with python3}
mkdir -p %{buildroot}%{python3_sitelib}/%{name}/
cp -ar %{name}/* tests %{buildroot}%{python3_sitelib}/%{name}/
%endif

install -Dpm0755 bin/%{name}.py %{buildroot}%{_bindir}/%{name}
install -Dpm0644 doc/build/man/%{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 scripts/tracer.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/tracer

make DESTDIR=%{buildroot}%{_datadir} mo
%find_lang %{name}

%files common -f %{name}.lang
%license LICENSE
%doc README.md
%{_datadir}/%{name}/
%{_sysconfdir}/bash_completion.d/tracer

%if %{with python2}
%files -n python2-%{name}
%{python2_sitelib}/%{name}/
%endif

%if %{with python3}
%files -n python3-%{name}
%{python3_sitelib}/%{name}/
%endif

%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*


%changelog
* Tue Nov 12 2024 Jakub Kadlcik <frostyx@email.cz> 1.2-1
- Implement support for DNF5 (frostyx@email.cz)

* Thu Oct 05 2023 Jakub Kadlcik <frostyx@email.cz> 1.1-1
- Fix parameters for specifying the target user (frostyx@email.cz)

* Fri Sep 15 2023 Jakub Kadlcik <frostyx@email.cz> 1.0-1
- Fix querying RPM files on EPEL7 (frostyx@email.cz)
- Use backported lru_cache on EPEL7 (frostyx@email.cz)
- Don't hang forever when executed via SSH (frostyx@email.cz)
- Don't check if package is installed before listing its files
  (frostyx@email.cz)
- Replace regexes where they are not needed (frostyx@email.cz)
- Query all packages at once, its faster than one by one (frostyx@email.cz)
- Cache some properties for a massive performance boost (frostyx@email.cz)
- Refactor unnecessary condition (frostyx@email.cz)
- Fix weird indentation (frostyx@email.cz)
- Pass the whole application to the provided_by function, not just its name
  (frostyx@email.cz)
- Stop using deprecated rpm.fi (frostyx@email.cz)
- Attempt to fix readthedocs deprecation error (frostyx@email.cz)
- More reliable check if /usr/lib/sysimage/dnf/ database should be used
  (frostyx@email.cz)

* Sun Jun 18 2023 Jakub Kadlcik <frostyx@email.cz> 0.7.11-1
- Rather create a /run/reboot-required not /var/run/reboot-required
  (frostyx@email.cz)

* Mon Jun 05 2023 Jakub Kadlcik <frostyx@email.cz> 0.7.10-1
- Update license to SPDX (frostyx@email.cz)
- Update tito releasers (frostyx@email.cz)

* Thu May 18 2023 Jakub Kadlcik <frostyx@email.cz> 0.7.9-1
- Create /var/run/reboot-required file (frostyx@email.cz)
- Recommend the correct command for restarting auditd (frostyx@email.cz)
- Add python3-setuptools dependency (frostyx@email.cz)
- Fix argument passed to print_helper() (ferdnyc@gmail.com)
- Add similar software to the readme (frostyx@email.cz)
- Update url references to point to tracer.readthedocs.io (dcampano@gmail.com)
- Oracle Linux 8 uses dnf, too (suttner@atix.de)
- Drop python-setuptools runtime dependency (frostyx@email.cz)
- Fix Python DeprecationWarning: invalid escape sequence
  (jvanderwaa@redhat.com)
- Add readthedocs configuration file (frostyx@email.cz)

* Mon Aug 23 2021 Jakub Kadlcik <frostyx@email.cz> 0.7.8-1
- Release also for F35 (frostyx@email.cz)
- Use distro.id() instead of platform.linux_distribution() (frostyx@email.cz)
- Implement compare_packages for the alpm backend (jvanderwaa@redhat.com)
- Add find_package support for alpm (jvanderwaa@redhat.com)
- Use importlib instead of deprecated imp (frostyx@email.cz)
- Drop beautifulsoup4/lxml dependencies (jvanderwaa@redhat.com)
- Drop F32 from releasers.conf (frostyx@email.cz)

* Sun Aug 01 2021 Jakub Kadlcik <frostyx@email.cz> 0.7.7-1
- Add installation instructions of EPEL 8 (frostyx@email.cz)
- Make the source of README.md more readable (frostyx@email.cz)
- Remove duplicates in suggested helpers (frostyx@email.cz)
- Make sure Collection.sorted doesn't traceback for None values
  (frostyx@email.cz)
- Ignore sudo and su in the output (frostyx@email.cz)
- Don't traceback for nonexisting PID (frostyx@email.cz)
- Access process PID only once (frostyx@email.cz)
- Rename tito master branch to rawhide (frostyx@email.cz)

* Fri Apr 16 2021 Jakub Kadlcik <frostyx@email.cz> 0.7.6-1
- Update tito releasers (frostyx@email.cz)
- CentOS-8 uses DNF (mmarusak@redhat.com)
- Add missing runtime dependency on python2-six (frostyx@email.cz)
- Add support for SUSE distributions using DNF (ngompa13@gmail.com)
- Print a user-friendly error when a xml file cannot be parsed
  (frostyx@email.cz)
- Update tito releasers (frostyx@email.cz)

* Sun Jan 24 2021 Jakub Kadlcik <frostyx@email.cz> 0.7.5-1
- Depend on python3-six instead of python3-future (frostyx@email.cz)
- Drop beautifulsoup4 in favor of built-in xml.dom (frostyx@email.cz)
- Drop nosetests dependency, use pytest instead (frostyx@email.cz)

* Mon Jun 08 2020 Jakub Kadlcik <frostyx@email.cz> 0.7.4-1
- Fix list index out of range for ssh process names (frostyx@email.cz)
- When there is no helper, it doesn't contain anything (frostyx@email.cz)
- Fix wrong parameters number when upating an application objects
  (frostyx@email.cz)
- Remove unnecessary string decoding (frostyx@email.cz)
- Fix the missing dist in release (frostyx@email.cz)

* Sat May 23 2020 Jakub Kadlčík <jkadlcik@redhat.com> - 0.7.3-2
- We lost release dist macro somewhere

* Fri May 22 2020 Jonathon Turel <jturel@gmail.com> 0.7.3-1
- Stub dbus calls in tests (jturel@gmail.com)

* Thu May 21 2020 Jonathon Turel <jturel@gmail.com> 0.7.2-3
- Update tito releaser branches (frostyx@email.cz)
- Not build for python2 package for Fedora anymore (frostyx@email.cz)

* Thu May 21 2020 Jonathon Turel <jturel@gmail.com> 0.7.2-2
- Fix build dependencies for EL7, EL8, F30 (jturel@gmail.com)

* Thu May 21 2020 Jonathon Turel <jturel@gmail.com> 0.7.2-1
- Use DNF on RHEL (jturel@gmail.com)
- Use PackageManager to determine kernel version (jturel@gmail.com)
- Use subprocess to check process path arguments (jturel@gmail.com)
- Find the right lxml version for Python 3.4 (jturel@gmail.com)
- Update Vagrantfile to use Fedora 30 (jturel@gmail.com)
- Ignore debug kernels when checking if kernel has been updated
  (jturel@gmail.com)
- Add build dependency for nosetests (frostyx@email.cz)
- Run tests within the %%check phase (frostyx@email.cz)
- Update fedora branches (frostyx@email.cz)

* Wed Jan 09 2019 Jakub Kadlčík <frostyx@email.cz> 0.7.1-1
- Fix #116 - Support currrent versions of DNF (elyscape@gmail.com)
- Fix #112 - handle PIDs that have no unit_path (seanokeeffe797@gmail.com)
- Fix #119 - Improve session detection logic to fix (elyscape@gmail.com)
- Fix space, instead of tabs (#115) (JensKuehnel@users.noreply.github.com)
- A lot of changes to spec file regarding python2/3 (seanokeeffe797@gmail.com)
* Thu Apr 19 2018 Sean O'Keeffe <seanokeeffe797@gmail.com> 0.7.0-1
- Fixes #98 - Don't try appending `None`, helpers (seanokeeffe797@gmail.com)
- Fixes #104 - Replace None with "" when sorting (seanokeeffe797@gmail.com)
- Update Python 2 dependency declarations to new packaging standards
  (seanokeeffe797@gmail.com)
- Fixes #105 - check ID_LIKE in /etc/os-release (seanokeeffe797@gmail.com)
- Cache process info (elyscape@gmail.com)
- Handle sshd sessions that use privilege separation (elyscape@gmail.com)
- fix typo in docs (seanokeeffe797@gmail.com)
- Switch Travis to container-based infrastructure (seanokeeffe797@gmail.com)
- Fix RHBug #1469282 - bash completion should exit cleanly if python-
  argcomplete is not installed (seanokeeffe797@gmail.com)
- Fix argparse logic in spec (#94) (frostyx@email.cz)
- Update branches for fedora releaser (frostyx@email.cz)
- Add epel releaser (seanokeeffe797@gmail.com)
- rename tito releasers (seanokeeffe797@gmail.com)

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.6.13.1-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 02 2017 Jakub Kadlčík <frostyx@email.cz> 0.6.13.1-2
- Fix argparse logic (RhBug: 1492078)

* Mon Sep 11 2017 Sean O'Keeffe <seanokeeffe797@gmail.com> 0.6.13.1-1
- Fixes #92 - Correct package version comparision (seanokeeffe797@gmail.com)
- EPEL uses python-argcomplete not pythonX-argcomplete
  (seanokeeffe797@gmail.com)

* Mon Jun 12 2017 Jakub Kadlčík <frostyx@email.cz> 0.6.13-1
- report reboot for new kernels (#83) (seanokeeffe797@gmail.com)
- Get daemon names from dbus (#82) (seanokeeffe797@gmail.com)
- Added Enterprise Linux install instructions (seanokeeffe797@gmail.com)
- bash completion support (seanokeeffe797@gmail.com)
- Use ID_LIKE in /etc/os-release (#81) (seanokeeffe797@gmail.com)
- Fixes #85 - Always respect app type defines (seanokeeffe797@gmail.com)
- Fixes #84 - ignore flag is now respected (seanokeeffe797@gmail.com)
- Fixes #20 - print executable in interactive mode (seanokeeffe797@gmail.com)
- Fixes #56 - Add Ubunut support (seanokeeffe797@gmail.com)
- Fixes #76 - polkitd service can be restarted (seanokeeffe797@gmail.com)
- Fixes #73 - add support for Oracle Linux (seanokeeffe797@gmail.com)
- Fixes #66 - reconise postfix process correctly (seanokeeffe797@gmail.com)
- Fixes #68 - recognised SSH sessions correctly (seanokeeffe797@gmail.com)
* Sun Nov 06 2016 Jakub Kadlčík <frostyx@email.cz> 0.6.12-1
- Add Vagrantfile for more convenient testing (frostyx@email.cz)
- Recommend systemctl instead of service on systemd machines (seanokeeffe797@gmail.com)
- Implement --now and --packages as API Query methods (frostyx@email.cz)
- Improve support for python applications (Fix #64) (frostyx@email.cz)
* Sat Aug 06 2016 Jakub Kadlčík <frostyx@email.cz> 0.6.11-1
- Release even for F25 (frostyx@email.cz)
- Obsolete old tracer version (frostyx@email.cz)
- :retab the specfile (frostyx@email.cz)

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
