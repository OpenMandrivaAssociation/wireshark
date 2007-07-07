%define	blurb Wireshark is a fork of Ethereal(tm)

%define	major 0
%define libname %mklibname wireshark %{major}
%define main_version 0.99.6

Summary:	Network traffic analyzer
Name:		wireshark
Version:	%{main_version}
Release:	%mkrel 1
License:	GPL
Group: 		Monitoring
URL: 		http://www.wireshark.org
Source0:	http://www.wireshark.org/download/src/%{name}-%{version}.tar.bz2
Source1:	http://www.wireshark.org/download/src/all-versions/SIGNATURES-%{main_version}.txt
Patch0:		wireshark_help_browser.patch.bz2
Requires:	net-snmp-mibs
Requires:	net-snmp-utils
Requires:	usermode-consoleonly
BuildRequires:	doxygen
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	libtool
BuildRequires:	glib2-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libelf-devel
BuildRequires:	openssl-devel
BuildRequires:	libpcap-devel >= 0.7.2
BuildRequires:	net-snmp-devel
BuildRequires:	pcre-devel
BuildRequires:	adns-devel
BuildRequires:	krb5-devel
BuildRequires:	libgnutls-devel
Provides:	ethereal = %{version}
Obsoletes:	ethereal
#Conflicts:	ethereal
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Wireshark is a network traffic analyzer for Unix-ish operating
systems. It is based on GTK+, a graphical user interface library,
and libpcap, a packet capture and filtering library.

%{blurb}

%package -n	%{libname}
Summary:	Network traffic and protocol analyzer libraries
Group:         	System/Libraries
Conflicts:      ethereal <= 0.10.5
Provides:	%{mklibname ethereal 0} = %{version}
Obsoletes:	%{mklibname ethereal 0}
#Conflicts:	%{mklibname ethereal 0}

%description -n	%{libname}
Wireshark is a network traffic analyzer for Unix-ish operating
systems. It is based on GTK+, a graphical user interface library,
and libpcap, a packet capture and filtering library.

%{blurb}

%package	tools
Summary:	Tools for manipulating capture files
Group:		Monitoring
Provides:	ethereal-tools = %{version}
Obsoletes:	ethereal-tools
#Conflicts:	ethereal-tools

%description	tools
Set of tools for manipulating capture files. Contains:
- editcap - Edit and/or translate the format of capture files
- mergecap - Merges two capture files into one
- text2cap - Generate a capture file from an ASCII hexdump of packets

%{blurb}

%package -n	tshark
Summary:	Text-mode network traffic and protocol analyzer
Group:		Monitoring
Provides:	tethereal = %{version}
Obsoletes:	tethereal
#Conflicts:	tethereal

%description -n tshark
Twireshark is a network protocol analyzer. It lets you capture packet
data from a live network, or read packets from a previously saved
capture file, either printing a decoded form of those packets to the
standard output or writing the packets to a file. Twireshark's native
capture file format is libpcap format, which is also the format used
by tcpdump and various other tools.

%{blurb}

%prep

%setup -q -n %{name}-%{version}

%patch0 -p1

%build
%serverbuild

export WANT_AUTOCONF_2_5=1
rm -f configure wiretap/configure
libtoolize --copy --force; aclocal-1.7 -I aclocal-fallback; autoconf; automake-1.7 --add-missing --copy
pushd wiretap
    aclocal-1.7 -I ../aclocal-fallback; autoconf; automake-1.7 --add-missing --copy
popd
    
export LIBS="-L%{_libdir}"
export LDFLAGS="-L%{_libdir}"

%configure2_5x \
    --disable-warnings-as-errors --enable-warnings-as-errors=no \
    --disable-usr-local \
    --disable-static \
    --enable-gtk2 \
    --enable-tshark \
    --enable-editcap \
    --enable-dumpcap \
    --enable-capinfos \
    --enable-mergecap \
    --enable-text2pcap \
    --enable-idl2wrs \
    --enable-dftest \
    --enable-randpkt \
    --enable-ipv6 \
    --with-pcap=%{_prefix} \
    --with-zlib=%{_prefix} \
    --with-pcre=%{_prefix} \
    --with-ssl=%{_prefix} \
    --with-net-snmp=%{_prefix} \
    --with-plugins=%{_libdir}/%{name}

%make

# duh?
make %{name}.1

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std transform=""

# duh?
install -m0644 %{name}.1 %{buildroot}%{_mandir}/man1/

# menu
install -d %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF

?package(%{name}): \
command="%{name}" \
title="Wireshark" \
longtitle="Network traffic analyzer" \
needs="x11" \
icon="%{name}.png" \
section="System/Monitoring" \
xdg="true"

?package(%{name}): \
command="%{name}-root" \
title="Wireshark (root user)" \
longtitle="Network traffic analyzer (root user)" \
needs="x11" \
icon="%{name}.png" \
section="System/Monitoring" \
xdg="true"
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
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;X-MandrivaLinux-System-Monitoring;System;Monitor;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-root.desktop << EOF
[Desktop Entry]
Name=Wireshark (root user)
Comment=Network traffic analyzer (root user)
Exec=%{name}-root
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;X-MandrivaLinux-System-Monitoring;System;Monitor;
EOF

# move this one to /usr/sbin
mv %{buildroot}%{_bindir}/dumpcap %{buildroot}%{_sbindir}/dumpcap

# fix one odd bug...
pushd %{buildroot}%{_bindir}
    ln -s ../sbin/dumpcap dumpcap
popd

# do we need a development package?
rm -f %{buildroot}%{_libdir}/*.so
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/%{name}/*.la

# fix @SHELL@
perl -pi -e "s|\@SHELL\@|/bin/sh|g" %{buildroot}%{_bindir}/idl2wrs

%post
%update_menus

%postun
%clean_menus

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-root
%attr(755,root,root) %{_bindir}/dumpcap
%attr(755,root,root) %{_sbindir}/%{name}-root
%attr(755,root,root) %{_sbindir}/dumpcap
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/manuf
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/cfilters
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/colorfilters
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/dfilters
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/diameter/*
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/radius/dictionary*
%attr(644,root,root) %{_datadir}/%{name}/help/*
%dir %{_datadir}/%{name}
%{_menudir}/%{name}
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_mandir}/man1/dumpcap.1*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man4/%{name}-filter.4*
%{_datadir}/%{name}/*.html
%{_datadir}/%{name}/AUTHORS-SHORT
%{_datadir}/%{name}/COPYING
%dir %{_datadir}/%{name}/dtds
%{_datadir}/%{name}/dtds/*
%{_datadir}/applications/*.desktop

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/capinfos
%attr(755,root,root) %{_bindir}/dftest
%attr(755,root,root) %{_bindir}/editcap
%attr(755,root,root) %{_bindir}/idl2wrs
%attr(755,root,root) %{_bindir}/mergecap
%attr(755,root,root) %{_bindir}/randpkt
%attr(755,root,root) %{_bindir}/text2pcap
%{_mandir}/man1/capinfo*
%{_mandir}/man1/editcap*
%{_mandir}/man1/idl2wrs*
%{_mandir}/man1/mergecap*
%{_mandir}/man1/text2pcap*

%files -n tshark
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tshark
%{_mandir}/man1/tshark*

%files -n %{libname}
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ NEWS README{,.[lv]*} doc/{randpkt.txt,README.*}
%attr(755,root,root) %{_libdir}/lib*.so.*
