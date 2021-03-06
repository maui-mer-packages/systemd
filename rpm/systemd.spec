Name:           systemd
URL:            http://www.freedesktop.org/wiki/Software/systemd
Version:        216
Release:        1
License:        LGPLv2+ and MIT and GPLv2+
Group:          System/System Control
Summary:        A System and Service Manager
BuildRequires:  libcap-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(dbus-1) >= 1.3.2
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  libxslt
BuildRequires:  libacl-devel
BuildRequires:  glib2-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  pkgconfig(usbutils) >= 0.82
BuildRequires:  pkgconfig(blkid) >= 2.20
BuildRequires:  intltool >= 0.40.0
BuildRequires:  gperf
BuildRequires:  xz-devel
BuildRequires:  kmod-devel >= 15
BuildRequires:  fdupes
BuildRequires:  cryptsetup-luks-devel
BuildRequires:  gnutls-devel
BuildRequires:  elfutils-devel
BuildRequires:  libidn-devel
BuildRequires:  libcurl-devel
# ln --relative was introduced in 8.16
BuildRequires:  coreutils >= 8.16
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires:       dbus
Requires:       filesystem >= 3
Requires:       systemd-config
# fsck with -l option was introduced in 2.21.2 packaging
Requires:       util-linux >= 2.21.2
Source0:        http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
Source1:        systemctl-user
Source100:      systemd-rpmlintrc
Provides:       udev = %{version}
Obsoletes:      udev < 184 
Provides:       systemd-sysv = %{version}
Obsoletes:      systemd-sysv < %{version}
Provides:       systemd-sysv-docs = %{version}
Obsoletes:      systemd-sysv-docs < %{version}
Provides:       systemd-docs = %{version}
Obsoletes:      systemd-docs < %{version}
Provides:       systemd-console-ttyMFD2 = %{version}
Obsoletes:      systemd-console-ttyMFD2 <= 187
Provides:       systemd-console-ttyS0 = %{version}
Obsoletes:      systemd-console-ttyS0 <= 187
Provides:       systemd-console-ttyS1 = %{version}
Obsoletes:      systemd-console-ttyS1 <= 187
Provides:       systemd-console-tty01 = %{version}
Obsoletes:      systemd-console-tty01 <= 187
Provides:       systemd-console-ttyO2 = %{version}
Obsoletes:      systemd-console-ttyO2 <= 187
Provides:       systemd-console-ttyAMA0 = %{version}
Obsoletes:      systemd-console-ttyAMA0 <= 187

%description
systemd is a system and service manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package config-maui
Summary:    Default configuration for systemd
Group:      System/System Control
Requires:   %{name} = %{version}-%{release}
Provides:   systemd-config

%description config-maui
This package provides default configuration for systemd

%package analyze
Summary:    Analyze systemd startup timing
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
Provides:   %{name}-tools = %{version}
Obsoletes:  %{name}-tools <= 187

%description analyze
This package installs the systemd-analyze tool, which allows one to
inspect and graph service startup timing in table or graph format.

%package libs
Summary:        systemd libraries
License:        LGPLv2+ and MIT
Provides:       libudev = %{version}
Obsoletes:      libudev < %{version}
Obsoletes:      systemd <= 187
Conflicts:      systemd <= 187

%description libs
Libraries for systemd and udev, as well as the systemd PAM module.

%package devel
Group:          Development/Libraries
Summary:        Development headers for systemd
License:        LGPLv2+ and MIT
Requires:       %{name} = %{version}-%{release}
Provides:       libudev-devel = %{version}
Obsoletes:      libudev-devel < %{version}

%description devel
Development headers and auxiliary files for developing applications for systemd.

%package -n libgudev1
Summary:        Libraries for adding libudev support to applications that use glib
Group:          Development/Libraries
Conflicts:      filesystem < 3
Requires:       %{name} = %{version}-%{release}
License:        LGPLv2+

%description -n libgudev1
This package contains the libraries that make it easier to use libudev
functionality from applications that use glib.

%package -n libgudev1-devel
Summary:        Header files for adding libudev support to applications that use glib
Group:          Development/Libraries
Requires:       libgudev1 = %{version}-%{release}
License:        LGPLv2+

%description -n libgudev1-devel
This package contains the header and pkg-config files for developing
glib-based applications using libudev functionality.

%prep
%setup -q -n %{name}-%{version}/systemd

%build
./autogen.sh
%configure \
  --with-rootprefix= \
  --disable-coredump \
  --disable-static \
  --with-firmware-path=/lib/firmware/updates:/lib/firmware:/system/etc/firmware:/etc/firmware:/vendor/firmware:/firmware/image \
  --with-kbd-loadkeys=/bin/loadkeys \
  --disable-manpages \
  --disable-python-devel \
  --disable-kdbus \
  --enable-compat-libs \
  --disable-tests

make %{?_smp_mflags}

%install
%make_install

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
mkdir -p %{buildroot}/{%{_sbindir},sbin}
ln -s ../lib/systemd/systemd %{buildroot}/sbin/init
ln -s ../../bin/systemctl %{buildroot}%{_sbindir}/reboot
ln -s ../../bin/systemctl %{buildroot}%{_sbindir}/halt
ln -s ../../bin/systemctl %{buildroot}%{_sbindir}/poweroff
ln -s ../../bin/systemctl %{buildroot}%{_sbindir}/shutdown
ln -s ../../bin/systemctl %{buildroot}%{_sbindir}/telinit
ln -s ../../bin/systemctl %{buildroot}%{_sbindir}/runlevel

ln -sf ../bin/udevadm %{buildroot}%{_sbindir}/udevadm

# Make sure these directories are properly owned
mkdir -p %{buildroot}/lib/systemd/system/basic.target.wants
mkdir -p %{buildroot}/lib/systemd/system/default.target.wants
mkdir -p %{buildroot}/lib/systemd/system/dbus.target.wants
mkdir -p %{buildroot}/lib/systemd/system/getty.target.wants
mkdir -p %{buildroot}/lib/systemd/system/syslog.target.wants

# enable readahead by default
ln -s ../systemd-readahead-collect.service %{buildroot}/lib/systemd/system/sysinit.target.wants/systemd-readahead-collect.service
ln -s ../systemd-readahead-replay.service %{buildroot}/lib/systemd/system/sysinit.target.wants/systemd-readahead-replay.service

# Require network to be enabled with multi-user.target
mkdir -p %{buildroot}/lib/systemd/system/multi-user.target.wants/
ln -s ../network.target %{buildroot}/lib/systemd/system/multi-user.target.wants/network.target

# Install Fedora default preset policy
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-preset/

# Make sure the shutdown/sleep drop-in dirs exist
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-shutdown/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-sleep/

# Make sure directories in /var exist
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/coredump
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/catalog
mkdir -p %{buildroot}%{_localstatedir}/log/journal
touch %{buildroot}%{_localstatedir}/lib/systemd/catalog/database
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin
touch %{buildroot}%{_localstatedir}/lib/systemd/random-seed

mkdir -p %{buildroot}%{_sysconfdir}/sysctl.d
mkdir -p %{buildroot}%{_sysconfdir}/modules-load.d
mkdir -p %{buildroot}%{_sysconfdir}/binfmt.d

# Don't ship documentation in the wrong place
rm %{buildroot}/%{_docdir}/systemd/*

mkdir -p %{buildroot}/etc/systemd/system/basic.target.wants

# Add systemctl-user helper script
install -D -m 754 %{SOURCE1} %{buildroot}/bin/systemctl-user

%fdupes  %{buildroot}/%{_datadir}/man/

mkdir -p %{buildroot}/lib/security/
mv %{buildroot}%{_libdir}/security/pam_systemd.so %{buildroot}/lib/security/pam_systemd.so

# Move rpm macros
mkdir -p %{buildroot}%{_sysconfdir}/rpm
mv %{buildroot}%{_libdir}/rpm/macros.d/macros.systemd %{buildroot}%{_sysconfdir}/rpm/macros.systemd
rm -rf %{buildroot}%{_libdir}/rpm

%find_lang %{name}

%pre
getent group cdrom >/dev/null 2>&1 || groupadd -r -g 11 cdrom >/dev/null 2>&1 || :
getent group tape >/dev/null 2>&1 || groupadd -r -g 33 tape >/dev/null 2>&1 || :
getent group dialout >/dev/null 2>&1 || groupadd -r -g 18 dialout >/dev/null 2>&1 || :
getent group systemd-journal >/dev/null 2>&1 || groupadd -r -g 190 systemd-journal 2>&1 || :
getent group systemd-timesync >/dev/null 2>&1 || groupadd -r systemd-timesync 2>&1 || :
getent passwd systemd-timesync >/dev/null 2>&1 || useradd -r -l -g systemd-timesync -d / -s /usr/sbin/nologin -c "systemd Time Synchronization" systemd-timesync >/dev/null 2>&1 || :
getent group systemd-network >/dev/null 2>&1 || groupadd -r systemd-network 2>&1 || :
getent passwd systemd-network >/dev/null 2>&1 || useradd -r -l -g systemd-network -d / -s /usr/sbin/nologin -c "systemd Network Management" systemd-network >/dev/null 2>&1 || :
getent group systemd-resolve >/dev/null 2>&1 || groupadd -r systemd-resolve 2>&1 || :
getent passwd systemd-resolve >/dev/null 2>&1 || useradd -r -l -g systemd-resolve -d / -s /usr/sbin/nologin -c "systemd Resolver" systemd-resolve >/dev/null 2>&1 || :
getent group systemd-journal-gateway >/dev/null 2>&1 || groupadd -r systemd-journal-gateway 2>&1 || :
getent passwd systemd-journal-gateway >/dev/null 2>&1 || useradd -r -l -g systemd-journal-gateway -d / -s /usr/sbin/nologin -c "systemd Journal Gateway" systemd-journal-gateway >/dev/null 2>&1 || :
getent group systemd-journal-remote >/dev/null 2>&1 || groupadd -r systemd-journal-remote 2>&1 || :
getent passwd systemd-journal-remote >/dev/null 2>&1 || useradd -r -l -g systemd-journal-remote -d / -s /usr/sbin/nologin -c "systemd Journal Remote" systemd-journal-remote >/dev/null 2>&1 || :
getent group systemd-journal-upload >/dev/null 2>&1 || groupadd -r systemd-journal-upload 2>&1 || :
getent passwd systemd-journal-upload >/dev/null 2>&1 || useradd -r -l -g systemd-journal-upload -d / -s /usr/sbin/nologin -c "systemd Journal Upload" systemd-journal-upload >/dev/null 2>&1 || :

#### This user and group are needed for kdbus which is disable at the moment,
#### besides it's not a valid group name see error "groupadd: 'systemd-bus-proxy' is not a valid group name"
#getent group systemd-bus-proxy >/dev/null 2>&1 || groupadd -r systemd-bus-proxy 2>&1 || :
#getent passwd systemd-bus-proxy >/dev/null 2>&1 || useradd -r -l -g systemd-bus-proxy -d / -s /usr/sbin/nologin -c "systemd Bus Proxy" systemd-bus-proxy >/dev/null 2>&1 || :

systemctl stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service >/dev/null 2>&1 || :

%post
systemd-machine-id-setup >/dev/null 2>&1 || :
/usr/lib/systemd/systemd-random-seed save >/dev/null 2>&1 || :
systemctl daemon-reexec >/dev/null 2>&1 || :
systemctl start systemd-udevd.service >/dev/null 2>&1 || :
udevadm hwdb --update >/dev/null 2>&1 || :
journalctl --update-catalog >/dev/null 2>&1 || :
systemd-tmpfiles --create >/dev/null 2>&1 || :

# Make sure new journal files will be owned by the "systemd-journal" group
chgrp systemd-journal /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2> /dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2> /dev/null` >/dev/null 2>&1 || :
chmod g+s /run/log/journal/ /run/log/journal/`cat /etc/machine-id 2> /dev/null` /var/log/journal/ /var/log/journal/`cat /etc/machine-id 2> /dev/null` >/dev/null 2>&1 || :

# Apply ACL to the journal directory
setfacl -Rnm g:wheel:rx,d:g:wheel:rx,g:adm:rx,d:g:adm:rx /var/log/journal/ >/dev/null 2>&1 || :

if [ $1 -eq 1 ] ; then
	for unit in systemd-journal-gatewayd.socket systemd-journal-gatewayd.service; do
		systemctl preset $unit > /dev/null 2>&1 || :
	done
fi

%preun
if [ $1 -eq 0 ] ; then
	for unit in systemd-journal-gatewayd.socket systemd-journal-gatewayd.service; do
		systemctl --no-reload disable $unit > /dev/null 2>&1 || :
		systemctl stop $unit > /dev/null 2>&1 || :
	done
fi

%postun
if [ $1 -ge 1 ] ; then
	systemctl daemon-reload > /dev/null 2>&1 || :
	for unit in systemd-logind.service systemd-journal-gatewayd.service; do
		systemctl try-restart $unit >/dev/null 2>&1 || :
	done
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post -n libgudev1 -p /sbin/ldconfig
%postun -n libgudev1 -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%exclude %{_sysconfdir}/systemd/system/getty.target.wants/getty@tty1.service
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%dir %{_prefix}/lib/systemd
%dir %{_prefix}/lib/systemd/catalog
%dir %{_prefix}/lib/tmpfiles.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/binfmt.d
%dir %{_datadir}/systemd
%dir %{_localstatedir}/log/journal
%dir %{_localstatedir}/lib/systemd
%dir %{_localstatedir}/lib/systemd/catalog
%dir %{_localstatedir}/lib/systemd/coredump
%ghost %{_localstatedir}/lib/systemd/random-seed
%ghost %{_localstatedir}/lib/systemd/catalog/database
%ghost %{_localstatedir}/log/README

%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.login1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.locale1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.machine1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%config(noreplace) %{_sysconfdir}/systemd/bootchart.conf
%config(noreplace) %{_sysconfdir}/pam.d/systemd-user
%ghost %{_sysconfdir}/udev/hwdb.bin
%{_sysconfdir}/rpm/macros.systemd
%{_sysconfdir}/init.d/README
%config(noreplace) %{_sysconfdir}/xdg/systemd/user
%{_sysconfdir}/systemd/system/*
%{_libdir}/tmpfiles.d/*
%{_libdir}/sysusers.d/*
%{_libdir}/sysctl.d/50-default.conf
%{_libdir}/systemd/user/*

%dir /lib/udev/
/lib/udev/*

/bin/systemctl
/bin/systemctl-user
/bin/systemd-notify
/bin/systemd-ask-password
/bin/systemd-tty-ask-password-agent
/bin/systemd-machine-id-setup
/bin/loginctl
/bin/journalctl
/bin/machinectl
/bin/networkctl
/bin/systemd-tmpfiles
/bin/systemd-escape
/bin/systemd-firstboot
/bin/systemd-sysusers
%{_bindir}/systemd-path
%{_bindir}/systemd-run
/bin/udevadm
%{_bindir}/kernel-install
%{_bindir}/systemd-nspawn
%{_bindir}/systemd-stdio-bridge
%{_bindir}/systemd-cat
%{_bindir}/systemd-cgls
%{_bindir}/systemd-cgtop
%{_bindir}/systemd-delta
%{_bindir}/systemd-detect-virt
/bin/systemd-inhibit
%{_bindir}/hostnamectl
%{_bindir}/localectl
%{_bindir}/timedatectl
%{_bindir}/bootctl
%{_bindir}/busctl
%{_sbindir}/udevadm
/%{_lib}/systemd
%{_datadir}/dbus-1/*/org.freedesktop.systemd1.*
%{_datadir}/dbus-1/*/org.freedesktop.resolve1.*
%{_defaultdocdir}/systemd
%{_datadir}/factory/*
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy
%{_datadir}/bash-completion/completions/bootctl
%{_datadir}/bash-completion/completions/busctl
%{_datadir}/bash-completion/completions/hostnamectl
%{_datadir}/bash-completion/completions/machinectl
%{_datadir}/bash-completion/completions/journalctl
%{_datadir}/bash-completion/completions/localectl
%{_datadir}/bash-completion/completions/loginctl
%{_datadir}/bash-completion/completions/systemctl
%{_datadir}/bash-completion/completions/timedatectl
%{_datadir}/bash-completion/completions/udevadm
%{_datadir}/bash-completion/completions/systemd-analyze
%{_datadir}/bash-completion/completions/systemd-cat
%{_datadir}/bash-completion/completions/systemd-cgls
%{_datadir}/bash-completion/completions/systemd-cgtop
%{_datadir}/bash-completion/completions/systemd-delta
%{_datadir}/bash-completion/completions/systemd-detect-virt
%{_datadir}/bash-completion/completions/systemd-nspawn
%{_datadir}/bash-completion/completions/systemd-run
%{_datadir}/bash-completion/completions/kernel-install
%{_datadir}/zsh/site-functions/*

/usr/lib/systemd/catalog/systemd*.catalog
/usr/lib/kernel/install.d/50-depmod.install
/usr/lib/kernel/install.d/90-loaderentry.install

%{_sbindir}/halt
/sbin/init
%{_sbindir}/poweroff
%{_sbindir}/reboot
%{_sbindir}/runlevel
%{_sbindir}/shutdown
%{_sbindir}/telinit

%{_datadir}/systemd/kbd-model-map
# Just make sure we don't package these by default
%exclude /lib/systemd/system/default.target
%exclude %{_libdir}/systemd/user/default.target
%exclude %{_sysconfdir}/systemd/system/multi-user.target.wants/remote-fs.target
%exclude /lib/systemd/system/user@.service

%files config-maui
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/systemd/resolved.conf
%config(noreplace) %{_sysconfdir}/systemd/timesyncd.conf
%config(noreplace) %{_sysconfdir}/systemd/journal-upload.conf
%config(noreplace) %{_sysconfdir}/udev/udev.conf
/lib/systemd/system/default.target
/lib/systemd/system/user@.service

%files analyze
%defattr(-,root,root,-)
%{_bindir}/systemd-analyze

%files libs
%defattr(-,root,root,-)
/lib/security/pam_systemd.so
%{_libdir}/libnss_myhostname.so.2
%{_libdir}/libnss_mymachines.so.2
%{_libdir}/libnss_resolve.so.2
%{_libdir}/libsystemd-daemon.so.*
%{_libdir}/libsystemd-login.so.*
%{_libdir}/libsystemd-journal.so.*
%{_libdir}/libsystemd-id128.so.*
%{_libdir}/libsystemd.so.*
%{_libdir}/libudev.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/systemd
%{_libdir}/libsystemd-daemon.so
%{_libdir}/libsystemd-login.so
%{_libdir}/libsystemd-journal.so
%{_libdir}/libsystemd-id128.so
%{_libdir}/libudev.so
%{_libdir}/libsystemd.so
%{_includedir}/systemd/_sd-common.h
%{_includedir}/systemd/sd-daemon.h
%{_includedir}/systemd/sd-login.h
%{_includedir}/systemd/sd-journal.h
%{_includedir}/systemd/sd-id128.h
%{_includedir}/systemd/sd-messages.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libsystemd-daemon.pc
%{_libdir}/pkgconfig/libsystemd-login.pc
%{_libdir}/pkgconfig/libsystemd-journal.pc
%{_libdir}/pkgconfig/libsystemd-id128.pc
%{_libdir}/pkgconfig/libsystemd.pc
%{_libdir}/pkgconfig/libudev.pc
%{_datadir}/pkgconfig/systemd.pc
%{_datadir}/pkgconfig/udev.pc

%files -n libgudev1
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgudev-1.0.so.*

%files -n libgudev1-devel
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgudev-1.0.so
%dir %attr(0755,root,root) %{_includedir}/gudev-1.0
%dir %attr(0755,root,root) %{_includedir}/gudev-1.0/gudev
%attr(0644,root,root) %{_includedir}/gudev-1.0/gudev/*.h
%attr(0644,root,root) %{_libdir}/pkgconfig/gudev-1.0.pc
