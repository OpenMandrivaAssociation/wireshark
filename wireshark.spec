%define Werror_cflags %{nil}

%define	major		0
%define wiretapmajor	0
%define wsutilmajor	0
%define libname		%mklibname wireshark %{major}
%define libwiretap	%mklibname wiretap %{wiretapmajor}
%define libwsutil	%mklibname wsutil %{wsutilmajor}
%define devname		%mklibname -d wireshark

Summary:	Network traffic analyzer
Name:		wireshark
Version:	3.3.0
Release:	1
License:	GPLv2+ and GPLv3
Group:		Monitoring
URL:		https://www.wireshark.org
Source0:	https://www.wireshark.org/download/src/%{name}-%{version}.tar.xz
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	flex
BuildRequires:	elfutils-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	perl-Pod-Html
BuildRequires:	pcre-devel
BuildRequires:	qt5-macros
BuildRequires:	qmake5
BuildRequires:	qt5-linguist-tools
BuildRequires:	tiff-devel
BuildRequires:	perl-open
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Help)
BuildRequires:	cmake(Qt5MultimediaWidgets)
BuildRequires:	cmake(Qt5PrintSupport)
BuildRequires:	cmake(Qt5Svg)
BuildRequires:	cmake(Qt5Widgets)
# Optional BRs
BuildRequires:	doxygen
BuildRequires:	git-core
BuildRequires:	krb5-devel
BuildRequires:	libcap-devel
BuildRequires:	gnutls-devel
BuildRequires:	pcap-devel
BuildRequires:	libsmi-devel
BuildRequires:	lua5.2-devel
#BuildRequires:	pkgconfig(libbcg729)
BuildRequires:	pkgconfig(libcares)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libnghttp2)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libmaxminddb)
BuildRequires:	pkgconfig(libssh)
BuildRequires:	pkgconfig(sbc)
BuildRequires:	pkgconfig(snappy)
BuildRequires:	pkgconfig(spandsp)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(libbrotlienc)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	asciidoc
BuildRequires:	xsltproc
BuildRequires:	zlib-devel

Requires:	dumpcap
Requires:	xdg-utils

%description
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on Qt, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%package -n	%{libname}
Summary:	Network traffic and protocol analyzer libraries
Group:		System/Libraries

%description -n	%{libname}
Wireshark is a network traffic analyzer for Unix-ish operating systems. It is
based on Qt, a graphical user interface library, and libpcap, a packet
capture and filtering library.

%package -n	%{libwiretap}
Summary:	Packet-capture library for %{name}
Group:		System/Libraries

%description -n	%{libwiretap}
The wiretap library is a packet-capture library currently under development
parallel to wireshark.

Wiretap is used in wireshark for its ability to read multiple file types.

%package -n	%{libwsutil}
Summary:	Network packet dissection utilities library
Group:		System/Libraries

%description -n	%{libwsutil}
The libwsutil library provides utility functions for wireshark.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/Other
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	wireshark-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libwiretap} = %{version}-%{release}
Requires:	%{libwsutil} = %{version}-%{release}

%description -n	%{devname}
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

%build
%cmake_qt5 \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DENABLE_EXTRA_COMPILER_WARNINGS:BOOL=ON \
	-DDUMPCAP_INSTALL_OPTION:STRING="suid" \
	-DENABLE_DUMPCAP_GROUP:BOOL=ON \
	-DDUMPCAP_INSTALL_GROUP:STRING="wireshark" \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

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
install -m 0644 *.h build/*.h %{buildroot}%{_includedir}/wireshark
mkdir -p %{buildroot}%{_includedir}/wireshark/wiretap
install -m 0644 wiretap/*.h %{buildroot}%{_includedir}/wireshark/wiretap
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
Version:	%{version}

Requires:
Libs: -L\${libdir} -lwireshark
Cflags: -I\${includedir}
EOF

%pre -n dumpcap
if ! getent group wireshark > /dev/null ;then
	%{_sbindir}/groupadd -r -f wireshark
fi

%files -n dumpcap
%doc %{_docdir}/%{name}/dumpcap.html
%attr(4750, root, wireshark) %{_bindir}/dumpcap
%{_mandir}/man1/dumpcap.1*

%files
%doc %{_docdir}/%{name}/wireshark-filter.html
%doc %{_docdir}/%{name}/wireshark.html
%{_bindir}/%{name}
%{_bindir}/%{name}-qt
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/plugins/
%dir %{_libdir}/%{name}/extcap/
%{_datadir}/%{name}/
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
%doc %{_docdir}/%{name}/androiddump.html
%doc %{_docdir}/%{name}/capinfos.html
%doc %{_docdir}/%{name}/captype.html
%doc %{_docdir}/%{name}/ciscodump.html
%doc %{_docdir}/%{name}/dftest.html
%doc %{_docdir}/%{name}/dpauxmon.html
%doc %{_docdir}/%{name}/editcap.html
%doc %{_docdir}/%{name}/extcap.html
%doc %{_docdir}/%{name}/mergecap.html
%doc %{_docdir}/%{name}/mmdbresolve.html
%doc %{_docdir}/%{name}/randpkt.html
%doc %{_docdir}/%{name}/randpktdump.html
%doc %{_docdir}/%{name}/reordercap.html
%doc %{_docdir}/%{name}/sshdump.html
%doc %{_docdir}/%{name}/text2pcap.html
%doc %{_docdir}/%{name}/udpdump.html
%doc %{_docdir}/%{name}/sdjournal.html
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
%{_libdir}/%{name}/extcap/ciscodump
%{_libdir}/%{name}/extcap/dpauxmon
%{_libdir}/%{name}/extcap/randpktdump
%{_libdir}/%{name}/extcap/sdjournal
%{_libdir}/%{name}/extcap/sshdump
%{_libdir}/%{name}/extcap/udpdump
%{_mandir}/man1/androiddump.1*
%{_mandir}/man1/capinfos.1*
%{_mandir}/man1/captype.1*
%{_mandir}/man1/ciscodump.1*
%{_mandir}/man1/dftest.1*
%{_mandir}/man1/dpauxmon.1*
%{_mandir}/man1/editcap.1*
%{_mandir}/man1/mergecap.1*
%{_mandir}/man1/mmdbresolve.1*
%{_mandir}/man1/randpkt.1*
%{_mandir}/man1/randpktdump.1*
%{_mandir}/man1/reordercap.1*
%{_mandir}/man1/sdjournal.1*
%{_mandir}/man1/sshdump.1*
%{_mandir}/man1/text2pcap.1*
%{_mandir}/man1/udpdump.1*
%{_mandir}/man4/extcap.4*

%files -n tshark
%doc %{_docdir}/%{name}/tshark.html
%{_bindir}/tshark
%{_mandir}/man1/tshark*

%files -n rawshark
%doc %{_docdir}/%{name}/rawshark.html
%{_bindir}/rawshark
%{_mandir}/man1/rawshark.1*

%files -n %{libname}
%doc AUTHORS NEWS README.{md,[lv]*} doc/{randpkt.txt,README.*}
%{_libdir}/libwireshark.so.%{major}*

%files -n %{libwiretap}
%{_libdir}/libwiretap.so.%{wiretapmajor}*

%files -n %{libwsutil}
%{_libdir}/libwsutil.so.%{wsutilmajor}*

%files -n %{devname}
%doc ChangeLog
%{_includedir}/wireshark/
%{_libdir}/libwireshark.so
%{_libdir}/libwiretap.so
%{_libdir}/libwsutil.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/wireshark/cmake/
