%define debug_package %{nil}

Name:           kiskadee
Version:        0.4.1
Release:        1%{?dist}
Summary:        A continuous static analysis system

License:        GPLv3
URL:            https://pagure.io/kiskadee
Source0:        https://releases.pagure.org/kiskadee/%{name}-%{version}.tar.gz

BuildRequires: openssl-devel
BuildRequires: python3-devel
BuildRequires: python2-devel
BuildRequires: gcc
BuildRequires: redhat-rpm-config
BuildRequires: python3-psutil
BuildRequires: python3-psycopg2
BuildRequires: python3-firehose
BuildRequires: python3-sqlalchemy
BuildRequires: python3-chardet
BuildRequires: python3-packaging
BuildRequires: python3-PyYAML
BuildRequires: python3-flask
BuildRequires: python3-flask-restless
BuildRequires: python3-marshmallow
BuildRequires: python3-nose
BuildRequires: python3-fedmsg

Requires: python3-psutil
Requires: python3-psycopg2
Requires: python3-firehose
Requires: python3-sqlalchemy
Requires: python3-chardet
Requires: python3-packaging
Requires: python3-PyYAML
Requires: python3-flask
Requires: python3-flask-restless
Requires: python3-marshmallow
Requires: python3-nose
Requires: python3-fedmsg

# BUG: https://bugzilla.redhat.com/show_bug.cgi?id=1114413
#Requires: python3-flask-cors

%description
kiskadee is a system to support static analysis usage during software
development by providing ranked static analysis reports.
First, it runs multiple security-oriented static analyzers on the source code.
Then, using a classification model, the possible bugs detected by the static
analyzers are ranked based on their importance, where critical flaws are
ranked first and potential false positives are ranked last.

%prep
%autosetup

%build
%py3_build

%install
%py3_install
install -m 644 util/kiskadee.conf -D $RPM_BUILD_ROOT%{_sysconfdir}/kiskadee.conf

%files
%license LICENSE
%doc doc
%{_bindir}/%{name}
%{_bindir}/%{name}_api
%{python3_sitelib}/%{name}/
%{python3_sitelib}/%{name}*.egg-info/
%config %{_sysconfdir}/kiskadee.conf

%changelog
* Sun Nov 05 2017 David Carlos <ddavidcarlos1392@gmail.com> - 0.4.0-1
- Initial packaging work for Fedora

