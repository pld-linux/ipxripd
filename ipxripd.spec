Summary:	IPX RIP/SAP daemon - routing for IPX networks
Name:		ipxripd
Version:	0.7
Release:	4
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Vendor:		Volker Lendecke <lendecke@namu01.gwdg.de>
Source0:	ftp://ftp.gwdg.de/pub/linux/misc/ncpfs/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-glibc2.1.patch
Prereq:		rc-scripts >= 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ipxripd is an implementation of Novell's RIP and SAP protocols. It
automagically builds and updates IPX routing table in the Linux
kernel. Usefull when trying to get a Linux box to act as an IPX
router.

%prep
%setup -q -n ipxripd
%patch -p1

%build
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/var/log} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d}

install ipxd $RPM_BUILD_ROOT%{_sbindir}
install ipxd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install ipx_ticks.5 $RPM_BUILD_ROOT%{_mandir}/man5

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ipxripd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ipxripd

:> $RPM_BUILD_ROOT/var/log/ipxd

gzip -9nf README ipx_ticks

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ipxripd
if [ -f /var/lock/subsys/ipxripd ]; then
	/etc/rc.d/init.d/ipxripd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ipxripd start\" to start IPX routing daemon."
fi
touch /var/log/ipxd

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ipxripd ]; then
		/etc/rc.d/init.d/ipxripd stop >&2
	fi
	/sbin/chkconfig --del ipxripd
fi

%files
%defattr(644,root,root,755)
%doc {README,ipx_ticks}.gz

%attr(754,root,root) /etc/rc.d/init.d/ipxripd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*

%attr(755,root,root) %{_sbindir}/ipxd

%{_mandir}/man[58]/*

%attr(640,root,root) %ghost /var/log/*
