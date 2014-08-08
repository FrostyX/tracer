Name:		tracer
Version:	0.4.4
Release:	1%{?dist}
Summary:	finds outdated running applications in your system

BuildArch:	noarch
Group:		Applications/System
License:	GPLv2
URL:		https://github.com/FrostyX/tracer/wiki
# Sources can be obtained by
# git clone git@github.com:FrostyX/tracer.git
# cd tracer
# tito build --tgz
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	python2-devel
Requires:	python
Requires:	python-beautifulsoup4
Requires:	python-psutil

%description
Tracer finds outdated running applications in your system.

How does he do it? He simply finds all packages you have modified since you boot
up. Then he traces their files in the jungle of your memory, ... senses them,
and finally, finds them. In the end you will get list of packages what have been
running while you updated or removed them.

%package -n dnf-tracer-plugin
Summary:	DNF plugin for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	dnf >= 0.4.9

%description -n dnf-tracer-plugin
Tracer finds outdated running applications in your system.

This is plugin for DNF which runs tracer after every successful transaction

%prep
%setup -q


%build


%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/tracer
mkdir -p %{buildroot}/%{python2_sitelib}/tracer
cp -a bin/tracer.py %{buildroot}/%{_bindir}/tracer
cp -a data/* %{buildroot}/%{_datadir}/tracer/
cp -ar tracer/* tests %{buildroot}/%{python2_sitelib}/tracer/

mkdir -p %{buildroot}/%{python2_sitelib}/dnf-plugins
cp -ar integration/dnf/plugins/tracer.py %{buildroot}/%{python2_sitelib}/dnf-plugins/tracer.py


%files
%doc LICENSE README.md
%{_bindir}/tracer
%{_datadir}/tracer/
%{python2_sitelib}/tracer/

%files -n dnf-tracer-plugin
%{python2_sitelib}/dnf-plugins/tracer.py*

%changelog
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

