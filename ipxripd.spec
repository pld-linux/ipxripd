Summary:	IPX RIP/SAP daemon - routing for IPX networks
Name:		ipxripd
Version:	0.7
Release:	3
Group:		Networking/Daemons
Copyright:	GPL
Source0:	ftp://ftp.gwdg.de/pub/linux/misc/ncpfs/%{name}-%{version}.tar.gz
Source1:	ipxripd.init
Source2:	ipxripd.sysconfig
Patch:		ipxripd-glibc2.1.patch
Vendor:		Volker Lendecke <lendecke@namu01.gwdg.de>
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/var/log}
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d}}

install -s ipxd $RPM_BUILD_ROOT%{_sbindir}
install ipxd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install ipx_ticks.5 $RPM_BUILD_ROOT%{_mandir}/man5

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ipxripd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ipxripd

:> $RPM_BUILD_ROOT/var/log/ipxd

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{5,8}/* \
	README ipx_ticks ipxripd-0.7.lsm

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
chmod 640 /var/log/cron

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del ipxripd
	/etc/rc.d/init.d/ipxripd stop >&2
fi

%files
%defattr(644,root,root,755)
%doc {README,ipx_ticks,ipxripd-0.7.lsm}.gz

%attr(754,root,root) /etc/rc.d/init.d/ipxripd
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/*

%attr(755, root, root) %{_sbindir}/ipxd

%{_mandir}/man8/ipxd.8.gz
%{_mandir}/man5/ipx_ticks.5.gz

%attr(640,root,root) %ghost /var/log/*
