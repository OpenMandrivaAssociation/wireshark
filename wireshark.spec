%if %mdkversion >= 200810
%define _disable_ld_as_needed 1
%define _disable_ld_no_undefined 1
%endif

%if %mdkversion >= 200910
%define Werror_cflags %{nil}
%endif

%if %mdkversion < 200900
%define ldflags %{nil}
%endif

%define	blurb Wireshark is a fork of Ethereal(tm)

%define	major 0
%define libname %mklibname wireshark %{major}
%define libname_devel %mklibname -d wireshark

Summary:	Network traffic analyzer
Name:		wireshark
Version:	1.2.0
%if %mdkversion < 200910
%define subrel	1
%endif
%if %mdkversion >= 200800
# this is for Cooker
Release:	%mkrel 1
%else
# this is for -0 CS4 updates: mkrel is decremented when subrel is set
Release:	%mkrel 1
%endif
License:	GPL
Group: 		Monitoring
URL: 		http://www.wireshark.org
Source0:	http://www.wireshark.org/download/src/%{name}-%{version}.tar.bz2
Source1:	http://www.wireshark.org/download/src/all-versions/SIGNATURES-%{version}.txt
Patch0:		wireshark_help_browser.patch
Patch1:		wireshark-plugindir.patch
Patch2:		wireshark_pipe.patch
Patch3:		wireshark-1.0.8-gnutls-2.8.patch
Requires:	usermode-consoleonly
Requires:	dumpcap
BuildRequires:	adns-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.9
BuildRequires:	doxygen
BuildRequires:	glib2-devel
BuildRequires:	gtk+2-devel
BuildRequires:	krb5-devel
BuildRequires:	libcap-devel
BuildRequires:	libelf-devel
BuildRequires:	libpcap-devel >= 0.7.2
BuildRequires:	libsmi-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
%if %mdkversion >= 200810
BuildRequires:	lua-devel
BuildRequires:	portaudio-devel
BuildRequires:	libgcrypt-devel >= 1.1.92
BuildRequires:	libgnutls-devel >= 1.2.0
%endif
BuildRequires:	zlib-devel
BuildRequires:	bison
BuildRequires:	flex
Provides:	ethereal = %{version}
Obsoletes:	ethereal
#Conflicts:	ethereal
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on GTK+, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%{blurb}

%package -n	%{libname}
Summary:	Network traffic and protocol analyzer libraries
Group:		System/Libraries
Conflicts:	ethereal <= 0.10.5
Provides:	%{mklibname ethereal 0} = %{version}
Obsoletes:	%{mklibname ethereal 0}
#Conflicts:	%{mklibname ethereal 0}

%description -n	%{libname}
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on GTK+, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%{blurb}

%package -n	%{libname_devel}
Summary:	Development files for %{name}
Group:		Development/Other
Provides:	libwireshark-devel = %{version}
Provides:	wireshark-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname_devel}
This package contains files used for development with %{name}.


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
Requires:	dumpcap
#Conflicts:	tethereal

%description -n	tshark
Tshark is a network protocol analyzer. It lets you capture packet data from a
live network, or read packets from a previously saved capture file, either
printing a decoded form of those packets to the standard output or writing the
packets to a file. Twireshark's native capture file format is libpcap format,
which is also the format used by tcpdump and various other tools.

%{blurb}

%package -n	rawshark
Summary:	Dump and analyze raw libpcap data
Group:		Monitoring
Conflicts:	wireshark-tools <= 0.99.8-1mdv2008.1

%description -n rawshark
Rawshark reads a stream of packets from a file or pipe, and prints a line
describing its output, followed by a set of matching fields for each packet on
stdout.

%{blurb}

%package -n	dumpcap
Summary:	Network traffic dump tool
Group:		Monitoring
# earlier dumpcap was part of the wireshark package
Conflicts:	wireshark <= 0.99.8-2mdv2008.1

%description -n dumpcap
Dumpcap is a network traffic dump tool. It lets you capture packet data from a
live network and write the packets to a file. Many wireshark utilities require it.

%{blurb}

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p0
#%patch2 -p1
%patch3 -p0

%build
%serverbuild

export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal-1.9 -I aclocal-fallback; autoconf; automake-1.9 --add-missing --copy

export LIBS="-L%{_libdir}"
export LDFLAGS="%{ldflags} -L%{_libdir}"

%configure2_5x \
    --disable-static \
    --disable-warnings-as-errors --enable-warnings-as-errors=no \
    --disable-usr-local \
    --enable-gtk2 \
    --enable-threads \
    --enable-tshark \
    --enable-editcap \
    --enable-capinfos \
    --enable-mergecap \
    --enable-text2pcap \
    --enable-idl2wrs \
    --enable-dftest \
    --enable-randpkt \
    --enable-dumpcap \
    --enable-ipv6 \
    --with-libsmi=%{_prefix} \
    --with-pcap=%{_prefix} \
    --with-zlib=%{_prefix} \
    --with-pcre=%{_prefix} \
%if %mdkversion >= 200810
    --with-lua=%{_prefix} \
    --with-portaudio=%{_prefix} \
    --with-gnutls=yes \
    --with-gcrypt=yes \
%endif
    --with-libcap=%{_prefix} \
    --with-ssl=%{_prefix} \
    --with-krb5 \
    --with-adns=%{_prefix} \
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
%if %mdkversion <= 200700
install -d %{buildroot}%{_menudir} 	 
cat > %{buildroot}%{_menudir}/%{name} <<EOF 	 
?package(%{name}): \ 	 
command="%{name}" \ 	 
title="Wireshark" \ 	 
longtitle="Network traffic analyzer" \ 	 
needs="x11" \ 	 
icon="%{name}.png" \ 	 
section="System/Monitoring" \ 	 
xdg=true \

?package(%{name}): \ 	 
command="%{name}-root" \ 	 
title="Wireshark (root user)" \ 	 
longtitle="Network traffic analyzer (root user)" \ 	 
needs="x11" \ 	 
icon="%{name}.png" \ 	 
section="System/Monitoring" \ 	 
xdg=true
EOF
%endif

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

# fix @SHELL@
perl -pi -e "s|\@SHELL\@|/bin/sh|g" %{buildroot}%{_bindir}/idl2wrs

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n dumpcap
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/dumpcap
%attr(755,root,root) %{_sbindir}/dumpcap
%{_mandir}/man1/dumpcap.1*

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-root
%attr(755,root,root) %{_sbindir}/%{name}-root
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/diameter
%dir %{_datadir}/%{name}/help
%dir %{_datadir}/%{name}/radius
%dir %{_datadir}/%{name}/tpncp
%dir %{_datadir}/%{name}/wimaxasncp
%if %mdkversion <= 200700
%{_menudir}/%{name}
%endif
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/cfilters
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/colorfilters
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/dfilters
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/diameter/*
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/manuf
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/radius/dictionary*
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/services
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/smi_modules
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/tpncp/*
%config(noreplace) %attr(644,root,root) %{_datadir}/%{name}/wimaxasncp/dictionary.*
%if %mdkversion >= 200810
%attr(644,root,root) %{_datadir}/%{name}/console.lua
%attr(644,root,root) %{_datadir}/%{name}/dtd_gen.lua
%attr(644,root,root) %{_datadir}/%{name}/init.lua
%endif
%attr(644,root,root) %{_datadir}/%{name}/help/*
%attr(644,root,root) %{_datadir}/%{name}/ws.css
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
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

%files -n rawshark
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rawshark
%{_mandir}/man1/rawshark.1*

%files -n %{libname}
%defattr(644,root,root,755)
%doc AUTHORS NEWS README{,.[lv]*} doc/{randpkt.txt,README.*}
%attr(755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname_devel}
%defattr(-,root,root)
%doc ChangeLog
%{_includedir}/wireshark
%{_libdir}/libwireshark.la
%{_libdir}/libwireshark.so
%{_libdir}/libwiretap.la
%{_libdir}/libwiretap.so
%{_libdir}/libwsutil.la
%{_libdir}/libwsutil.so
