#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Qt GUI component toolkit library for Coin
Summary(pl.UTF-8):	Biblioteka komponentu graficznego interfejsu Qt dla biblioteki Coin
Name:		SoQt
Version:	1.5.0
Release:	2
License:	GPL v2 or Coin PEL
Group:		X11/Libraries
Source0:	https://bitbucket.org/Coin3D/coin/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	9f1e582373d66f556b1db113a93ac68e
Patch0:		%{name}-pc.patch
URL:		http://www.coin3d.org/lib/soqt/
BuildRequires:	Coin-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	QtOpenGL-devel >= 4
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRequires:	pkgconfig
BuildRequires:	qt4-build >= 4
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SoQt is a Qt GUI component toolkit library for Coin. It is also
compatible with SGI and TGS Open Inventor, and the API is based on the
API of the InventorXt GUI component toolkit.

%description -l pl.UTF-8
SoQt to biblioteka toolkitu komponentu graficznego interfejsu
użytkownika (GUI) Qt dla biblioteki Coin. Jest zgodna także z
biblioteką SGI i TGS Open Inventor, a API jest oparte na API toolkitu
komponentu graficznego interfejsu użytkownika InventorXt.

%package devel
Summary:	Header files for SoQt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SoQt
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Coin-devel
Requires:	QtCore-devel >= 4
Requires:	OpenGL-GLX-devel

%description devel
Header files for SoQt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SoQt.

%package static
Summary:	Static SoQt library
Summary(pl.UTF-8):	Statyczna biblioteka SoQt
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static SoQt library.

%description static -l pl.UTF-8
Statyczna biblioteka SoQt.

%prep
%setup -q
%patch0 -p1

%build
# -DHAVE_GLX is not passed properly from configure
CXXFLAGS="%{rpmcxxflags} -DHAVE_GLX"
%configure \
	%{?with_static_libs:--enable-static}

# GL is missing; cannot rebuild auto* because of missing m4 files
%{__sed} -i -e '/^LIBS =/s/$/ -lGL/' src/Inventor/Qt/Makefile

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libSoQt.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS.txt COPYING ChangeLog FAQ NEWS README
%attr(755,root,root) %{_libdir}/libSoQt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSoQt.so.20

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSoQt.so
%attr(755,root,root) %{_bindir}/soqt-config
%{_includedir}/Inventor/Qt
%{_pkgconfigdir}/SoQt.pc
%{_aclocaldir}/soqt.m4
%{_datadir}/Coin/conf/soqt-default.cfg
%{_mandir}/man1/soqt-config.1*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libSoQt.a
%endif
