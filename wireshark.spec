%define Werror_cflags %{nil}
%define _disable_rebuild_configure %nil
%bcond_with lua

%define	major		10
%define wiretapmajor	8
%define wscodecsmajor	2
%define wsutilmajor	9
%define libname		%mklibname wireshark %{major}
%define libwiretap	%mklibname wiretap %{wiretapmajor}
%define libwscodecs	%mklibname wscodecs %{wscodecsmajor}
%define libwsutil	%mklibname wsutil %{wsutilmajor}
%define libname_devel	%mklibname -d wireshark

Summary:	Network traffic analyzer
Name:		wireshark
Version:	2.6.5
Release:	%mkrel 1
License:	GPLv2+ and GPLv3
Group:		Monitoring
URL:		http://www.wireshark.org
Source0:	http://www.wireshark.org/download/src/%{name}-%{version}.tar.xz
Source10:	README.urpmi
Patch0:		wireshark-1.12.0-do-not-fail-on-chgrp-chmod.patch
Requires:	dumpcap
Requires:	xdg-utils
BuildRequires:	doxygen
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5MultimediaWidgets)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	krb5-devel
BuildRequires:	qt5-qtchooser
BuildRequires:	qt5-linguist-tools
BuildRequires:	libcap-devel
BuildRequires:	pkgconfig(libelf)
BuildRequires:	libpcap-devel >= 0.7.2
BuildRequires:	libsmi-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
%if %{with lua}
BuildRequires:	lua-devel
%endif
BuildRequires:	portaudio-devel
BuildRequires:	libgcrypt-devel >= 1.1.92
BuildRequires:	gnutls-devel >= 1.2.0
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	zlib-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(libmaxminddb)
BuildRequires:	libtool
BuildRequires:	perl-Pod-Html
Obsoletes:	wireshark-gtk < 2.0.0
Obsoletes:	wireshark-common < 2.0.0
Conflicts:	wireshark-common < 2.0.0

%description
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on Qt, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%package -n	%{libname}
Summary:	Network traffic and protocol analyzer libraries
Group:		System/Libraries
Conflicts:	%{_lib}wireshark3 < 1.10.1

%description -n	%{libname}
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on Qt, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%package -n	%{libwiretap}
Summary:	Packet-capture library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}wireshark3 < 1.10.1

%description -n	%{libwiretap}
The wiretap library is a packet-capture library currently under development
parallel to wireshark.

Wiretap is used in wireshark for its ability to read multiple file types.

%package -n	%{libwscodecs}
Summary:	Network packet dissection codecs library
Group:		System/Libraries

%description -n	%{libwscodecs}
The libwscodecs library provides a codecs interface for wireshark.

%package -n	%{libwsutil}
Summary:	Network packet dissection utilities library
Group:		System/Libraries
Conflicts:	%{_lib}wireshark3 < 1.10.1

%description -n	%{libwsutil}
The libwsutil library provides utility functions for wireshark.

%package -n	%{libname_devel}
Summary:	Development files for %{name}
Group:		Development/Other
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	wireshark-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libwiretap} = %{version}-%{release}
Requires:	%{libwscodecs} = %{version}-%{release}
Requires:	%{libwsutil} = %{version}-%{release}

%description -n	%{libname_devel}
This package contains files used for development with %{name}.

%package	tools
Summary:	Tools for manipulating capture files
Group:		Monitoring

%description	tools
Set of tools for manipulating capture files. Contains:

- editcap - Edit and/or translate the format of capture files
- mergecap - Merges two capture files into one
- text2cap - Generate a capture file from an ASCII hexdump of packets

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

%package -n	rawshark
Summary:	Dump and analyze raw libpcap data
Group:		Monitoring

%description -n	rawshark
Rawshark reads a stream of packets from a file or pipe, and prints a line
describing its output, followed by a set of matching fields for each packet on
stdout.

%package -n	dumpcap
Summary:	Network traffic dump tool
Group:		Monitoring

%description -n	dumpcap
Dumpcap is a network traffic dump tool. It lets you capture packet data from a
live network and write the packets to a file. Many wireshark utilities require it.

%prep
%setup -q
%autopatch -p1

# README.urpmi
install -Dm644 %{SOURCE10} .

%build
./autogen.sh
export PATH=$PATH:%{_qt5_bindir}
export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
touch config.h.in
%configure \
    --disable-static \
    --disable-warnings-as-errors \
    --disable-silent-rules \
    --enable-warnings-as-errors=no \
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
    --enable-setuid-install \
    --enable-plugins \
    --with-gnutls=yes \
    --with-gcrypt=yes \
    --with-maxminddb \
    --with-krb5 \
    --with-adns=no \
    --with-gtk3=no \
    --with-qt=yes \
    --with-libnl=3 \
    --with-libsmi=%{_prefix} \
    --with-pcap=%{_prefix} \
    --with-zlib=%{_prefix} \
%if %{with lua}
    --with-lua=%{_prefix} \
%endif
    --with-portaudio=%{_prefix} \
    --with-libcap=%{_prefix}

%make_build

%install
%make_install

# link to main executable
mv %{buildroot}%{_bindir}/wireshark %{buildroot}%{_bindir}/wireshark-qt
ln -s wireshark-qt %{buildroot}%{_bindir}/wireshark

# icons
install -Dpm0644 image/wsicon16.png %{buildroot}%{_miconsdir}/%{name}.png
install -Dpm0644 image/wsicon32.png %{buildroot}%{_iconsdir}/%{name}.png
install -Dpm0644 image/wsicon48.png %{buildroot}%{_liconsdir}/%{name}.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications/
install -m 644 %{name}.desktop %{buildroot}%{_datadir}/applications/

# remove uneeded files
find %{buildroot} -name "*.la" -delete

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
mkdir -p %{buildroot}%{_includedir}/wireshark/codecs
install -m 0644 codecs/*.h %{buildroot}%{_includedir}/wireshark/codecs
mkdir -p %{buildroot}%{_includedir}/wireshark/wsutil
install -m 0644 wsutil/*.h %{buildroot}%{_includedir}/wireshark/wsutil

chmod a+r %{buildroot}%{_bindir}/dumpcap

# pkg-config support
install -d %{buildroot}%{_libdir}/pkgconfig/
cat > %{buildroot}%{_libdir}/pkgconfig/wireshark.pc << EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/wireshark
plugindir=%{_libdir}/wireshark

Name: wireshark
Description: wireshark network packet dissection library
Version: %{version}

Requires:
Libs: -L\${libdir} -lwireshark
Cflags: -I\${includedir}
EOF

%pre -n dumpcap
if ! getent group wireshark > /dev/null ;then
	%{_sbindir}/groupadd -r -f wireshark
fi

%files -n dumpcap
%attr(4750, root, wireshark) %{_bindir}/dumpcap
%{_mandir}/man1/dumpcap.1*

%files
%doc README.urpmi
%{_bindir}/%{name}
%{_bindir}/%{name}-qt
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/plugins/
%{_datadir}/%{name}
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_mandir}/man1/%{name}.1*
%{_mandir}/man4/%{name}-filter.4*
%{_datadir}/applications/*.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/mime/packages/%{name}.xml

%files tools
%{_bindir}/capinfos
%{_bindir}/captype
%{_bindir}/editcap
%{_bindir}/idl2wrs
%{_bindir}/mergecap
%{_bindir}/mmdbresolve
%{_bindir}/randpkt
%{_bindir}/reordercap
%{_bindir}/text2pcap
%{_bindir}/sharkd
%{_libdir}/%{name}/extcap/androiddump
%{_libdir}/%{name}/extcap/randpktdump
%{_libdir}/%{name}/extcap/udpdump
%{_mandir}/man1/androiddump*
%{_mandir}/man1/capinfo*
%{_mandir}/man1/captype*
%{_mandir}/man1/dftest*
%{_mandir}/man1/editcap*
%{_mandir}/man1/mergecap*
%{_mandir}/man1/mmdbresolve*
%{_mandir}/man1/randpkt*
%{_mandir}/man1/reordercap*
%{_mandir}/man1/text2pcap*
%{_mandir}/man1/udpdump*
%{_mandir}/man4/extcap*

%files -n tshark
%doc README.urpmi
%{_bindir}/tshark
%{_mandir}/man1/tshark*

%files -n rawshark
%{_bindir}/rawshark
%{_mandir}/man1/rawshark.1*

%files -n %{libname}
%doc AUTHORS NEWS README{,.[lv]*} doc/{randpkt.txt,README.*}
%{_libdir}/libwireshark.so.%{major}*

%files -n %{libwiretap}
%{_libdir}/libwiretap.so.%{wiretapmajor}*

%files -n %{libwscodecs}
%{_libdir}/libwscodecs.so.%{wscodecsmajor}*

%files -n %{libwsutil}
%{_libdir}/libwsutil.so.%{wsutilmajor}*

%files -n %{libname_devel}
%doc ChangeLog
%{_includedir}/wireshark
%{_libdir}/libwireshark.so
%{_libdir}/libwiretap.so
%{_libdir}/libwscodecs.so
%{_libdir}/libwsutil.so
%{_libdir}/pkgconfig/*.pc
