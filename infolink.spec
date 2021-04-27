# Build this using apx-rpmbuild.
%define name infolink

Name:           %{name}
Version:        %{version_rpm_spec_version}
Release:        %{version_rpm_spec_release}%{?dist}
Summary:        APx IPMC Info Link

License:        Reserved
URL:            https://github.com/uwcms/APx-%{name}
Source0:        %{name}-%{version_rpm_spec_version}.tar.gz

#BuildRequires:  #
Requires:       elmlink

%global debug_package %{nil}

%description
A tool to provide general ELM information to the IPMC, and get general IPMC
information on the ELM.


%prep
%setup -q


%build
##configure
# make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
install -D -m 0755 get_ipmc_info.py %{buildroot}/%{_bindir}/get_ipmc_info
install -D -m 0755 infolinkd.py %{buildroot}/%{_libexecdir}/infolinkd
install -D -m 0644 infolink.service %{buildroot}/%{_unitdir}/infolink.service
mkdir -p %{buildroot}/%{_sysconfdir}/infolink.d
rsync -a --chmod='u=rwX,go=rX' infolink.d/ %{buildroot}/%{_sysconfdir}/infolink.d/

%files
%{_bindir}/get_ipmc_info
%{_libexecdir}/infolinkd
%{_unitdir}/infolink.service
%dir %{_sysconfdir}/infolink.d
%{_sysconfdir}/infolink.d/*


%post
%systemd_post infolink.service


%preun
%systemd_preun infolink.service


%postun
%systemd_postun_with_restart infolink.service


%changelog
* Thu Mar 04 2021 Jesra Tikalsky <jtikalsky@hep.wisc.edu>
- Initial spec file
