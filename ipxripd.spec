Summary:	IPX RIP/SAP daemon - routing for IPX networks
Name:		ipxripd
Version:	0.7
Release:	2
Group:		Networking/Daemons
Copyright:	GPL
Source:		ftp://ftp.gwdg.de/pub/linux/misc/ncpfs/%{name}-%{version}.tar.gz
Patch:		ipxripd-glibc2.1.patch
Vendor:		Volker Lendecke <lendecke@namu01.gwdg.de>
BuildRoot:	/tmp/%{name}-%{version}-root

%description
ipxripd is an implementation of Novell's RIP and SAP protocols. It 
automagically builds and updates IPX routing table in the Linux kernel.
Usefull when trying to get a Linux box to act as an IPX router.

%prep
%setup -q -n ipxripd
%patch -p1

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8}}

install -s ipxd $RPM_BUILD_ROOT%{_sbindir}
install ipxd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install ipx_ticks.5 $RPM_BUILD_ROOT%{_mandir}/man5

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{5,8}/* \
	README ipx_ticks ipxripd-0.7.lsm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,ipx_ticks,ipxripd-0.7.lsm}.gz
%attr(755, root, root) %{_sbindir}/ipxd
%{_mandir}/man8/ipxd.8.gz
%{_mandir}/man5/ipx_ticks.5.gz
