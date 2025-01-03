#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_with	qt4		# Qt4 instead of Qt6
%bcond_with	qt5		# Qt5 instead of Qt6
%bcond_without	qt6		# Qt6 (default)

%if %{with qt4} || %{with qt5}
%undefine	with_qt6
%endif
%if %{without qt4} && %{without qt5} && %{without qt6}
%{error: at least one Qt version must be enabled}
%endif

Summary:	Qt GUI component toolkit library for Coin
Summary(pl.UTF-8):	Biblioteka komponentu graficznego interfejsu Qt dla biblioteki Coin
Name:		SoQt
Version:	1.6.3
Release:	1
License:	BSD
Group:		X11/Libraries
#Source0Download: https://github.com/coin3d/soqt/releases
Source0:	https://github.com/coin3d/soqt/releases/download/v%{version}/soqt-%{version}-src.tar.gz
# Source0-md5:	412a0de593fd336659faf73e7f96036f
Patch0:		%{name}-pc.patch
URL:		https://github.com/coin3d/soqt
BuildRequires:	Coin-devel >= 4.0.0
BuildRequires:	OpenGL-GLX-devel
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	QtOpenGL-devel >= 4
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5OpenGL-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
%endif
%if %{with qt6}
BuildRequires:	Qt6Core-devel >= 6
BuildRequires:	Qt6Gui-devel >= 6
BuildRequires:	Qt6OpenGL-devel >= 6
BuildRequires:	Qt6Widgets-devel >= 6
%endif
BuildRequires:	cmake >= 3.0
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
%if %{with qt4}
BuildRequires:	qt4-build >= 4
%endif
%if %{with qt5}
BuildRequires:	qt5-build >= 5
%endif
%if %{with qt6}
BuildRequires:	qt6-build >= 6
%endif
BuildRequires:	rpmbuild(macros) >= 1.752
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
Requires:	Coin-devel >= 4.0.0
%if %{with qt4}
Requires:	QtCore-devel >= 4
Requires:	QtGui-devel >= 4
Requires:	QtOpenGL-devel >= 4
%endif
%if %{with qt5}
Requires:	Qt5Core-devel >= 5
Requires:	Qt5Gui-devel >= 5
Requires:	Qt5OpenGL-devel >= 5
Requires:	Qt5Widgets-devel >= 5
%endif
%if %{with qt6}
Requires:	Qt6Core-devel >= 6
Requires:	Qt6Gui-devel >= 6
Requires:	Qt6OpenGL-devel >= 6
Requires:	Qt6Widgets-devel >= 6
%endif

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

%package apidocs
Summary:	API documentation for SoQt library
Summary(pl.UTF-8):	Dokumentacja API biblioteki SoQt
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for SoQt library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SoQt.

%prep
%setup -q -n soqt
%patch -P 0 -p1

%build
install -d builddir
cd builddir
%cmake .. \
%if %{with apidocs}
	-DSOQT_BUILD_DOCUMENTATION=ON \
	-DSOQT_BUILD_DOC_MAN=ON \
%endif
	%{!?with_qt5:-DSOQT_USE_QT5=OFF} \
	%{!?with_qt6:-DSOQT_USE_QT6=OFF}

%{__make}
cd ..

%if %{with static_libs}
install -d builddir-static
cd builddir-static
%cmake .. \
	-DSOQT_BUILD_SHARED_LIBS=OFF \
	%{!?with_qt5:-DSOQT_USE_QT5=OFF} \
	%{!?with_qt6:-DSOQT_USE_QT6=OFF}

%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with apidocs}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/html
# to common names etc.
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{_*_,components,devices,misc,viewers}.3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS.txt COPYING ChangeLog FAQ NEWS README
%attr(755,root,root) %{_libdir}/libSoQt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSoQt.so.20
%{_datadir}/SoQt

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSoQt.so
%{_includedir}/Inventor/Qt
%{_pkgconfigdir}/SoQt.pc
%{_libdir}/cmake/SoQt-%{version}
%if %{with apidocs}
%{_mandir}/man3/SoQt*.3*
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libSoQt.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc builddir/html/*.{css,html,js,png}
%endif
