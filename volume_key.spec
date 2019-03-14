Summary:	An utility for manipulating storage encryption keys and passphrases
Name:		volume_key
Version:	0.3.10
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	https://releases.pagure.org/volume_key/%{name}-%{version}.tar.xz
# Source0-md5:	605fd99a6e42916728020562a6edee78
URL:		https://pagure.io/volume_key/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
BuildRequires:	cryptsetup-devel
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel
BuildRequires:	gnupg
BuildRequires:	libblkid-devel
BuildRequires:	libtool
BuildRequires:	nss-devel
BuildRequires:	pkgconfig
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a command-line tool for manipulating storage
volume encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an
encrypted hard drive if the primary user forgets the passphrase. The
encryption key back up can also be useful for extracting data after a
hardware or software failure that corrupts the header of the encrypted
volume, or to access the company data after an employee leaves
abruptly.

%package libs
Summary:	A library for manipulating storage encryption keys and passphrases
Group:		Libraries

%description libs
This package provides libvolume_key, a library for manipulating
storage volume encryption keys and storing them separately from
volumes.

%package devel
Summary:	Header files for volume_key library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki volume_key
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for volume_key library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki volume_key.

%package -n python-%{name}
Summary:	Python bindings for volume_key library
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-%{name}
This package provides Python bindings for libvolume_key, a library for
manipulating storage volume encryption keys and storing them
separately from volumes.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -f $RPM_BUILD_ROOT%{py_sitedir}/*.la

%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/volume_key
%{_mandir}/man8/volume_key.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvolume_key.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvolume_key.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvolume_key.so
%{_libdir}/libvolume_key.la
%{_includedir}/volume_key

%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_volume_key.so
%{py_sitedir}/*.py[co]
