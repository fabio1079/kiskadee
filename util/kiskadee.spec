%define debug_package %{nil}

Name:           kiskadee
Version:        0.3.1
Release:        1%{?dist}
Summary:        kiskadee is a continuous static analysis tool which writes the analysis results into a Firehose database.

License:        GPLv3
URL:            https://pagure.io/kiskadee
Source0:        %{name}-%{version}.tar.gz

BuildRequires: openssl-devel
BuildRequires: python3-devel
BuildRequires: gcc
BuildRequires: redhat-rpm-config

Requires: docker
Requires: python3-psutil
Requires: python3-psycopg2
Requires: python3-firehose
Requires: python3-sqlalchemy
Requires: python-debian
Requires: python3-chardet
Requires: python3-packaging
Requires: python3-PyYAML
Requires: python3-flask-restless
Requires: python3-marshmallow
Requires: python3-nose
Requires: python2-fedmsg-consumers

# BUG: https://bugzilla.redhat.com/show_bug.cgi?id=1114413
#Requires: python3-flask-cors

%description

%prep
%autosetup

%build
%py3_build


%install
%py3_install


%files
%license LICENSE
%doc doc
%{_bindir}/%{name}
%{_bindir}/%{name}_api
%{python3_sitelib}/%{name}/
%{python3_sitelib}/%{name}*.egg-info/


%changelog
* Wed Oct 25 2017 David Carlos <ddavidcarlos1392@gmail.com>
-
