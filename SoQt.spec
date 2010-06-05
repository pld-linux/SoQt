
Summary:	Toolkit for multiplatform development of 2D user interfaces
Summary(pl.UTF-8):	Wieloplatformowe narzędzia do rozwoju interfejsów urzytkownika 2D.
Name:		SoQt
Version:	1.5.0
Release:	0.1
License:	GPL
Group:		X11/Libraries
# http://ftp.coin3d.org/coin/src/all/SoQt-1.5.0.tar.gz
Source0:	http://ftp.coin3d.org/coin/src/all/%{name}-%{version}.tar.gz
# Source0-md5:	9f1e582373d66f556b1db113a93ac68e
URL:		http://www.coin3d.org/lib/soqt/
BuildRequires:	Coin-devel
#BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	intltool
#BuildRequires:	libtool
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
#Provides:	-
#Provides:	group(foo)
#Provides:	user(foo)
#Obsoletes:	-
#Conflicts:	-
#BuildArch:	noarch
#ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# HAVE_GLX detection is broken in autocrap
%define specflags -DHAVE_GLX

%description
Library which provides the glue between Systems in Motion's Coin
high-level 3D visualization library and Troll Tech's Qt 2D user
interface library

%description -l pl.UTF-8
Biblioteka łącząca bibliotekę 3D wysokiego poziomu Coin z interfejsem
Qt.

%package devel
Summary:	Header files for ... library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ...
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for SoQt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SoQt


%prep
%setup -q
#%setup -q -c -T
#%setup -q -n %{name}
#%setup -q -n %{name}-%{version}.orig -a 1
#%patch0 -p1

# undos the source
#find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

# remove CVS control files
#find -name CVS -print0 | xargs -0 rm -rf

# you'll need this if you cp -a complete dir in source
# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
# if ac/am/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
#%%{__intltoolize}
#%%{__gettextize}
#%%{__libtoolize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
# if not running libtool or automake, but config.sub is too old:
#cp -f /usr/share/automake/config.sub .
%configure
%{__make} \
  LIBS="-lGL -lCoin -lQtGui -lQtCore -lQtOpenGL"

#%{__make} \
#	CFLAGS="%{rpmcflags}" \
#	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig


%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/soqt-config
%attr(755,root,root) %{_libdir}/libSoQt.so.*.*.*
# %{_datadir}/%{name}
%{_datadir}/Coin/conf/soqt-default.cfg
%{_mandir}/man1/soqt-config.1*

%doc AUTHORS ChangeLog NEWS README

%files devel
%defattr(644,root,root,755)
# %doc devel-doc/*
%{_libdir}/libSoQt.so
%{_libdir}/libSoQt.la
%{_includedir}/Inventor/Qt
%{_aclocaldir}/*.m4
%{_pkgconfigdir}/*.pc
