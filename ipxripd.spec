Summary:	IPX RIP/SAP daemon - routing for IPX networks
Summary(pl):	Demon IPX RIP/SAP - routing dla sieci IPX
Summary(pt_BR):	O ipxripd é uma implementação dos protocolos RIP e SAP da Novell
Name:		ipxripd
Version:	0.7
Release:	6
License:	GPL
Group:		Networking/Daemons
Vendor:		Volker Lendecke <lendecke@namu01.gwdg.de>
Source0:	ftp://ftp.gwdg.de/pub/linux/misc/ncpfs/%{name}-%{version}.tar.gz
# Source0-md5:	5e1ae45421d45eca67a435c6e5467ea1
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		%{name}-glibc2.1.patch
Prereq:		rc-scripts >= 0.2.0
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ipxripd is an implementation of Novell's RIP and SAP protocols. It
automagically builds and updates IPX routing table in the Linux
kernel. Useful when trying to get a Linux box to act as an IPX router.

%description -l pl
ipxripd jest implementacj± protoko³ów RIP i SAP Novella. Automagicznie
buduje i uaktualnia tablice routingu IPX w kernelu Linuksa. U¿yteczny
kiedy chcemy by Linux dzia³a³ jako router IPX.

%description -l pt_BR
O ipxripd é uma implementação dos protocolos RIP e SAP da Novell. Ele
gerencia de forma automática tabelas de roteamento IPX no kernel
Linux. Útil quando se deseja utilizar uma máquina Linux como roteador
IPX.

%prep
%setup -q -n ipxripd
%patch -p1

%build
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/var/log} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,logrotate.d,rc.d/init.d}

install ipxd $RPM_BUILD_ROOT%{_sbindir}
install ipxd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install ipx_ticks.5 $RPM_BUILD_ROOT%{_mandir}/man5

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ipxripd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ipxripd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/ipxripd

:> $RPM_BUILD_ROOT/var/log/ipxripd

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
%doc README ipx_ticks

%attr(754,root,root) /etc/rc.d/init.d/ipxripd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
%attr(640,root,root) /etc/logrotate.d/ipxripd

%attr(755,root,root) %{_sbindir}/ipxd

%{_mandir}/man[58]/*

%attr(640,root,root) %ghost /var/log/*
