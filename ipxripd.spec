%define Name	ipxripd
%define Version	0.7

Summary		: IPX RIP/SAP daemon for advertising IPX routes and services.
Name		: %{Name}
Version		: %{Version}
Release		: 4
Group		: Server/Network

Copyright	: GPL
Packager	: okir@lst.de (Olaf Kirch)
Icon		: ipxripd.xpm

BuildRoot	: /tmp/%{Name}-%{Version}


Source0: ftp://ftp.gwdg.de/pub/linux/misc/ncpfs/ipxripd-0.7.tgz
Source1: generic-LST.init
Patch0:  %{Name}-%{Version}-no-sap.patch

%Description
The IPX RIP/SAP daemon ipxd is invoked at boot time to manage the
kernel IPX routing tables. It distributes and receives routing
updates via RIP and SAP.

%Prep
%setup -n ipxripd
%patch0 -p1


%Build
make CFLAGS="$RPM_OPT_FLAGS -Wall -Wno-format"


%Install
DESTDIR=$RPM_BUILD_ROOT; export DESTDIR
[ -n "`echo $DESTDIR | sed -n 's:^/tmp/[^.].*$:OK:p'`" ] && rm -rf $DESTDIR ||
(echo "Invalid BuildRoot: '$DESTDIR'! Check this .spec ..."; exit 1) || exit 1

for dir in etc/{rc.d/init.d,sysconfig/daemons} usr/sbin usr/man/man{5,8}; do
	install -o root -g root -m 755 -d $DESTDIR/$dir
done

install -o root -g root -m 644 ipx_ticks $DESTDIR/etc
install -o root -g root -m 755 -s ipxd $DESTDIR%{_sbindir}
install -o root -g root -m 644 ipxd.8 $DESTDIR%{_mandir}/man8
install -o root -g root -m 644 ipx_ticks.5 $DESTDIR%{_mandir}/man5
install -o root -g root -m 755 $RPM_SOURCE_DIR/generic-LST.init $DESTDIR/etc/rc.d/init.d/ipxripd

# Create and install daemon config file
cat > daemon.cfg <<EOF
IDENT=ipxripd
DESCRIPTIVE="IPX RIP/SAP daemon"
DAEMON=%{_sbindir}/ipxd
DAEMON_ARGS=-r
ONBOOT=no
EOF
install -o root -g root -m 644 daemon.cfg $DESTDIR/etc/sysconfig/daemons/ipxripd

# gzip man pages and fix sym-links
MANPATHS=`find $DESTDIR -type d -name "man[1-9n]" -print`
if [ -n "$MANPATHS" ]; then
  chown -Rvc root.root $MANPATHS
  find $MANPATHS -type l -print |
    perl -lne '($f=readlink($_))&&unlink($_)&&symlink("$f.gz","$_.gz")||die;'
  find $MANPATHS -type f -print |
    xargs -r gzip -v9nf
fi


%Clean
DESTDIR=$RPM_BUILD_ROOT; export DESTDIR
[ -n "`echo $DESTDIR | sed -n 's:^/tmp/[^.].*$:OK:p'`" ] && rm -rf $DESTDIR ||
(echo "Invalid BuildRoot: '$DESTDIR'! Check this .spec ..."; exit 1) || exit 1

%Post
lisa --SysV-init install ipxripd S27 3:4:5 K73 0:1:2:6

%PostUn
lisa --SysV-init remove ipxripd $1

%Files
%doc README
%config /etc/ipx_ticks
%config /etc/sysconfig/daemons/ipxripd
/etc/rc.d/init.d/ipxripd
%{_sbindir}/ipxd
%{_mandir}/man5/ipx_ticks.5.gz
%{_mandir}/man8/ipxd.8.gz


%ChangeLog
* Mon Jan 01 1997 ...
$Id: ipxripd.spec,v 1.3 1999-05-17 23:39:55 kloczek Exp $
