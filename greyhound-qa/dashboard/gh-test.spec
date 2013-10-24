%define	debug_package %{nil}
%define php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%define php_version  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP Version => //p') | tail -1)
%define basedir /opt/zynga/greyhound/

%define conf_d /etc/httpd/conf.d/
%define expand_path() (sed -i'' \\\
	-e 's/[%]{greyhound_version}/%{version}-%{release}/g' \\\
	-e 's@[%]{basedir}@%{basedir}@g' \\\
	%*); 

%define _unpackaged_files_terminate_build 0 

# up priority for each release
%define priority %(python  -c 'import sys,re; print int("".join(["%02d" % int(x) for x in (re.split(r"[.-]", sys.argv[1]))]))' %{version}-%{release})

Summary: GHTest
Name: gh-test
Version: 1.4.0
Release: 3
License: Zynga 
Group: Applications/Server
URL: http://www.zynga.com/
Packager: Greyhound, Zynga Inc
Vendor: Zynga Inc
Source: /gh-test-%{version}-%{release}.tgz
BuildRoot: %{_topdir}/gh-test-%{version}-%{release}
BuildArch: noarch
Requires: python26, python26-PyYAML, python26-simplejson,python26-testoob,python26-4Suite-XML,pycurl
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description
TestQA platform installer


%prep
%setup -q -c -n testQA

%clean
%{__rm} -rf %{buildroot}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}
%{__make} -f Makefile install INSTALL_ROOT=%{buildroot}
# expand the alias line in apache.conf
%expand_path %{buildroot}/%{basedir}/%{version}-%{release}/gh_test/apache-tests.conf
%expand_path %{buildroot}/%{basedir}/%{version}-%{release}/use-version


%post 
%{_sbindir}/update-alternatives --install %{conf_d}/gh-test.conf ghtest %{basedir}/%{version}-%{release}/gh_test/apache-tests.conf %{priority}

%postun
%{_sbindir}/update-alternatives --remove ghtest %{basedir}/%{version}-%{release}/gh_test/apache-tests.conf


%files 
#%ghost %{basedir}/current/
%{basedir}/%{version}-%{release}/gh_test/
%attr(0777, root, root) %{basedir}/%{version}-%{release}/gh_test/scripts/config/load_config.yaml
%attr(0777, root, root) %{basedir}/%{version}-%{release}/gh_test/scripts/test/results
%{basedir}/%{version}-%{release}/internal/services/user.payments.meta.append.php
#%{basedir}/%{version}-%{release}/internal/services/user.blob.revert.php


