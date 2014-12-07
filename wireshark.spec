%define blurb Wireshark is a fork of Ethereal(tm)

%define major 5
%define wiretap_major 4
%define wsutil_major 4
%define filetap_major 0
%define libname %mklibname %{name} %{major}
%define libwiretap %mklibname wiretap %{wiretap_major}
%define libwsutil %mklibname wsutil %{wsutil_major}
%define libfiletap %mklibname filetap %{filetap_major}
%define devname %mklibname -d %{name}

Summary:	Network traffic analyzer
Name:		wireshark
Version:	1.12.1
Release:	2
License:	GPLv2+ and GPLv3
Group: 		Monitoring
Url: 		http://www.wireshark.org
Source0:	http://www.wireshark.org/download/src/%{name}-%{version}.tar.bz2
Source1:	http://www.wireshark.org/download/src/all-versions/SIGNATURES-%{version}.txt
Patch0:		wireshark_help_browser.patch
Patch1:		wireshark-plugindir.patch
Requires:	usermode-consoleonly
Requires:	dumpcap
BuildRequires:	autoconf automake libtool
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	cap-devel
BuildRequires:	elfutils-devel
BuildRequires:	krb5-devel
BuildRequires:	pcap-devel >= 0.7.2
BuildRequires:	pkgconfig(geoip)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	qt5-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libgcrypt) >= 1.1.92
BuildRequires:	pkgconfig(libsmi)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(zlib)

%track
prog %{name} = {
	url = http://www.wireshark.org/download/src/all-versions
	version = %{version}
	regex = %{name}-(__VER__)\.tar\.bz2
}

%description
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on QT5, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%{blurb}

%files
%{_bindir}/%{name}-qt
%{_bindir}/%{name}-root
%{_sbindir}/%{name}-root
%{_sysconfdir}/pam.d/%{name}-root
%{_sysconfdir}/security/console.apps/%{name}-root
# plugins
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/docsis.so
%{_libdir}/%{name}/ethercat.so
%{_libdir}/%{name}/gryphon.so
%{_libdir}/%{name}/irda.so
%{_libdir}/%{name}/m2m.so
%{_libdir}/%{name}/mate.so
%{_libdir}/%{name}/opcua.so
%{_libdir}/%{name}/profinet.so
%{_libdir}/%{name}/stats_tree.so
%{_libdir}/%{name}/unistim.so
%{_libdir}/%{name}/wimaxasncp.so
%{_libdir}/%{name}/wimax.so
%{_libdir}/%{name}/wimaxmacphy.so
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/diameter
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/diameter/*
%dir %{_datadir}/%{name}/dtds
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/dtds/*
%dir %{_datadir}/%{name}/help
%attr(0644,root,root) %{_datadir}/%{name}/help/*
%{_datadir}/%{name}/profiles
%dir %{_datadir}/%{name}/radius
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/radius/dictionary*
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/radius/custom.includes
%attr(0644,root,root) %{_datadir}/%{name}/radius/README.radius_dictionary
%dir %{_datadir}/%{name}/tpncp
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/tpncp/*
%dir %{_datadir}/%{name}/wimaxasncp
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/wimaxasncp/dictionary.*
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/cfilters
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/colorfilters
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/dfilters
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/manuf
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/pdml2html.xsl
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/services
%config(noreplace) %attr(0644,root,root) %{_datadir}/%{name}/smi_modules
%attr(0644,root,root) %{_datadir}/%{name}/console.lua
%attr(0644,root,root) %{_datadir}/%{name}/dtd_gen.lua
%attr(0644,root,root) %{_datadir}/%{name}/init.lua
%attr(0644,root,root) %{_datadir}/%{name}/ws.css
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_mandir}/man1/%{name}.1*
%{_mandir}/man4/%{name}-filter.4*
%{_datadir}/%{name}/*.html
%{_datadir}/%{name}/AUTHORS-SHORT
%{_datadir}/%{name}/COPYING
%{_datadir}/applications/*.desktop

#------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Network traffic and protocol analyzer libraries
Group:		System/Libraries
Obsoletes:	%{_lib}wireshark3 < 1.10.1

%description -n	%{libname}
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on QT5, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%{blurb}

%files -n %{libname}
%doc AUTHORS NEWS README{,.[lv]*} doc/{randpkt.txt,README.*}
%{_libdir}/libwireshark.so.%{major}*

#------------------------------------------------------------------------

%package -n	%{libwiretap}
Summary:	Network traffic and protocol analyzer libraries
Group:		System/Libraries
Conflicts:	%{_lib}wireshark3 < 1.10.1

%description -n	%{libwiretap}
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on QT5, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%{blurb}

%files -n %{libwiretap}
%doc AUTHORS NEWS README{,.[lv]*} doc/{randpkt.txt,README.*}
%{_libdir}/libwiretap.so.%{wiretap_major}*

#------------------------------------------------------------------------

%package -n	%{libwsutil}
Summary:	Network traffic and protocol analyzer libraries
Group:		System/Libraries
Conflicts:	%{_lib}wireshark3 < 1.10.1

%description -n	%{libwsutil}
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on QT5, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%{blurb}

%files -n %{libwsutil}
%doc AUTHORS NEWS README{,.[lv]*} doc/{randpkt.txt,README.*}
%{_libdir}/libwsutil.so.%{wsutil_major}*

#------------------------------------------------------------------------

%package -n     %{libfiletap}
Summary:        Network traffic and protocol analyzer libraries
Group:          System/Libraries
Conflicts:      %{_lib}wireshark3 < 1.10.1

%description -n %{libfiletap}
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on QT5, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%{blurb}

%files -n %{libfiletap}
%doc AUTHORS NEWS README{,.[lv]*} doc/{randpkt.txt,README.*}
%{_libdir}/libfiletap.so.%{filetap_major}*

#------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Development files for Wireshark
Group:		Development/Other
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{libwiretap} = %{EVRD}
Requires:	%{libwsutil} = %{EVRD}
Requires:	%{libfiletap} = %{EVRD}

%description -n	%{devname}
This package contains files used for development with Wireshark.

%files -n %{devname}
%doc ChangeLog
%{_includedir}/wireshark
%{_libdir}/libwireshark.so
%{_libdir}/libwiretap.so
%{_libdir}/libwsutil.so
%{_libdir}/libfiletap.so

#------------------------------------------------------------------------

%package	tools
Summary:	Tools for manipulating capture files
Group:		Monitoring

%description	tools
Set of tools for manipulating capture files. Contains:

- editcap - Edit and/or translate the format of capture files
- mergecap - Merges two capture files into one
- text2cap - Generate a capture file from an ASCII hexdump of packets

%{blurb}

%files tools
%{_bindir}/captype
%{_bindir}/capinfos
%{_bindir}/dftest
%{_bindir}/editcap
%{_bindir}/mergecap
%{_bindir}/randpkt
%{_bindir}/reordercap
%{_bindir}/text2pcap
%{_mandir}/man1/capinfo*
%{_mandir}/man1/dftest*
%{_mandir}/man1/editcap*
%{_mandir}/man1/mergecap*
%{_mandir}/man1/randpkt*
%{_mandir}/man1/reordercap*
%{_mandir}/man1/text2pcap*

#------------------------------------------------------------------------

%package -n	tshark
Summary:	Text-mode network traffic and protocol analyzer
Group:		Monitoring
Requires:	dumpcap

%description -n	tshark
Tshark is a network protocol analyzer. It lets you capture packet data from a
live network, or read packets from a previously saved capture file, either
printing a decoded form of those packets to the standard output or writing the
packets to a file. Twireshark's native capture file format is libpcap format,
which is also the format used by tcpdump and various other tools.

%{blurb}

%files -n tshark
%{_bindir}/tshark
%{_mandir}/man1/tshark*

#------------------------------------------------------------------------

%package -n	rawshark
Summary:	Dump and analyze raw libpcap data
Group:		Monitoring
Conflicts:	wireshark-tools <= 0.99.8-1mdv2008.1

%description -n rawshark
Rawshark reads a stream of packets from a file or pipe, and prints a line
describing its output, followed by a set of matching fields for each packet on
stdout.

%{blurb}

%files -n rawshark
%{_bindir}/rawshark
%{_mandir}/man1/rawshark.1*

#------------------------------------------------------------------------

%package -n	dumpcap
Summary:	Network traffic dump tool
Group:		Monitoring

%description -n dumpcap
Dumpcap is a network traffic dump tool. It lets you capture packet data from a
live network and write the packets to a file. Many wireshark utilities require
it.

%{blurb}

%files -n dumpcap
%{_bindir}/dumpcap
%{_sbindir}/dumpcap
%{_mandir}/man1/dumpcap.1*

#------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p1

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" *

%build
autoreconf -fi
%serverbuild
export PATH=$PATH:%_qt5_bindir
%configure2_5x \
    --disable-static \
    --disable-warnings-as-errors --enable-warnings-as-errors=no \
    --disable-usr-local \
    --enable-wireshark \
    --enable-packet-editor \
    --enable-tshark \
    --enable-editcap \
    --enable-capinfos \
    --enable-mergecap \
    --enable-text2pcap \
    --enable-dftest \
    --enable-randpkt \
    --enable-airpcap \
    --enable-dumpcap \
    --enable-rawshark \
    --enable-ipv6 \
    --with-gnutls=yes \
    --with-gcrypt=yes \
    --with-qt=yes \
    --with-libsmi=%{_prefix} \
    --with-pcap=%{_prefix} \
    --with-zlib=%{_prefix} \
    --with-lua=%{_prefix} \
    --with-portaudio=%{_prefix} \
    --with-libcap=%{_prefix} \
    --with-ssl=%{_prefix} \
    --with-krb5 \
    --with-adns=no \
    --with-geoip=yes \
    --with-plugins=%{_libdir}/%{name}

# try to fix the build...
find -name "Makefile" | xargs perl -pi -e "s|/usr/lib\b|%{_libdir}|g"

%make MOC=%_qt5_bindir/moc UIC=%_qt5_bindir/uic

%install
%makeinstall_std

# helpers to make sure we can start wireshark-root from user with root password
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cat > %{buildroot}%{_sysconfdir}/pam.d/%{name}-root << EOF
#%PAM-1.0
auth		include		config-util
account		include		config-util
session		include		config-util
EOF

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name}-root << EOF
USER=root
PROGRAM=/usr/sbin/wireshark-root
FALLBACK=false
SESSION=true
EOF

# setup links for consolehelpper support to allow root access
install -d %{buildroot}%{_sbindir}
pushd %{buildroot}%{_bindir}
    ln -sf consolehelper %{name}-root
cd %{buildroot}%{_sbindir}
    ln -s ../bin/%{name} %{name}-root
popd

# icon
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_liconsdir}

install -m0644 image/wsicon16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m0644 image/wsicon32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 image/wsicon48.png %{buildroot}%{_liconsdir}/%{name}.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications
install -m0644 wireshark.desktop %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Wireshark
Comment=Network traffic analyzer
Exec=%{name}-qt
Icon=%{name}
Terminal=false
Type=Application
Categories=Qt;X-MandrivaLinux-System-Monitoring;System;Monitor;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-root.desktop << EOF
[Desktop Entry]
Name=Wireshark (root user)
Comment=Network traffic analyzer (root user)
Exec=%{name}-root
Icon=%{name}
Terminal=false
Type=Application
Categories=Qt;System;Monitor;
EOF

# move this one to /usr/sbin
mv %{buildroot}%{_bindir}/dumpcap %{buildroot}%{_sbindir}/dumpcap

# fix one odd bug...
pushd %{buildroot}%{_bindir}
    ln -s ../sbin/dumpcap dumpcap
popd

# remove uneeded files
rm -f %{buildroot}%{_libdir}/wireshark/*.la

# install includes
mkdir -p %{buildroot}%{_includedir}/wireshark
for include in `find epan -type f -name '*.h'`; do
        mkdir -p %{buildroot}%{_includedir}/wireshark/`dirname $include`
        install -m 0644 $include %{buildroot}%{_includedir}/wireshark/`dirname $include`
done
# remaining include files
install -m 0644 *.h %{buildroot}%{_includedir}/wireshark
mkdir -p %{buildroot}%{_includedir}/wireshark/wiretap
install -m 0644 wiretap/*.h %{buildroot}%{_includedir}/wireshark/wiretap


