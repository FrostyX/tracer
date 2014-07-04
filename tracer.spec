Name:		tracer
Version:	0.3.1
Release:	1%{?dist}
Summary:	Tracer finds outdated running applications in your system

BuildArch:	noarch
Group:		Applications/System
License:	GPLv2
URL:		https://github.com/FrostyX/tracer/wiki
Source0:	tracer-%{version}.tar.gz

BuildRequires:	python2-devel
Requires:	python
Requires:	python-beautifulsoup4
Requires:	python-psutil

%description
Tracer finds outdated running applications in your system

How does he do it? He simply finds all packages you have modified since you boot up. Then he traces their files in the jungle of your memory, ... senses them, and finally, finds them. In the end you will get list of packages what have been running while you updated or removed them.

%package -n dnf-tracer-plugin
Summary:	DNF plugin for %{name}
Requires:	%{name} = %{version}-%{release}

%description -n dnf-tracer-plugin
Tracer finds outdated running applications in your system

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
%{python2_sitelib}/dnf-plugins/tracer.py
%{python2_sitelib}/dnf-plugins/tracer.pyc
%{python2_sitelib}/dnf-plugins/tracer.pyo

%changelog
* Mon Jun 30 2014 Jakub Kadlčík <frostyx@email.cz> 0.3
- create tracer package
