#
# Conditional build:
%bcond_without	python2	# CPython 2.x binding
%bcond_without	python3	# CPython 3.x binding

Summary:	An utility for manipulating storage encryption keys and passphrases
Summary(pl.UTF-8):	Narzędzie do operacji na kluczach i hasłach do szyfrowania dysków
Name:		volume_key
Version:	0.3.12
Release:	6
License:	GPL v2
Group:		Applications/System
Source0:	https://releases.pagure.org/volume_key/%{name}-%{version}.tar.xz
# Source0-md5:	200591290173c3ea71528411838f9080
URL:		https://pagure.io/volume_key/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
BuildRequires:	cryptsetup-devel
BuildRequires:	gettext-tools >= 0.18.2
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gpgme-devel
BuildRequires:	libblkid-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	nss-devel
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-devel >= 1:2.4}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.5}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
# gpg2 as /usr/bin/gpg
Requires:	gnupg2 >= 2.2
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

%description -l pl.UTF-8
Ten pakiet zawiera narzędzie linii poleceń do operacji na kluczach do
szyfrowania wolumenów dyskowych oraz przechowywania ich poza
wolumenami.

Głównym celem tego oprogramowania jest umożliwienie przywracania
dostępu do szyfrowanych dysków twardych w sytuacji, kiedy użytkownik
zapomni hasła. Kopia zapasowa klucza szyfrującego może być przydatna
także do wydobywania danych po awarii sprzętu lub oprogramowania,
wiążącej się z uszkodzeniem nagłówka zaszyfrowanego wolumenu, albo
dostępu do danych firmowych po nagłym odejściu pracownika.

%package libs
Summary:	A library for manipulating storage encryption keys and passphrases
Summary(pl.UTF-8):	Biblioteka do operacji na kluczach i hasłach do szyfrowania dysków
Group:		Libraries

%description libs
This package provides libvolume_key, a library for manipulating
storage volume encryption keys and storing them separately from
volumes.

%description libs -l pl.UTF-8
Ten pakiet zawiera bibliotekę libvolume_key, służącą do operacji na
kluczach do szyfrowania wolumenów dyskowych oraz przechowywania ich
poza wolumenami.

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
Summary:	Python 2 bindings for volume_key library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki volume_key
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-%{name}
This package provides Python 2 bindings for libvolume_key, a library
for manipulating storage volume encryption keys and storing them
separately from volumes.

%description -n python-%{name} -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona 2 do biblioteki libvolume_key,
służącej do operacji na kluczach do szyfrowania wolumenów dyskowych
oraz przechowywania ich poza wolumenami.

%package -n python3-%{name}
Summary:	Python 3 bindings for volume_key library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki volume_key
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n python3-%{name}
This package provides Python 3 bindings for libvolume_key, a library
for manipulating storage volume encryption keys and storing them
separately from volumes.

%description -n python3-%{name} -l pl.UTF-8
Ten pakiet zawiera wiązania Pythona 3 do biblioteki libvolume_key,
służącej do operacji na kluczach do szyfrowania wolumenów dyskowych
oraz przechowywania ich poza wolumenami.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	GPG=/usr/bin/gpg \
	%{!?with_python2:--without-python} \
	%{!?with_python3:--without-python3}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python2}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la
%py_postclean
%endif

%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.la
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
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
# TODO: drop when .pc file is introduced
%{_libdir}/libvolume_key.la
%{_includedir}/volume_key

%if %{with python2}
%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_volume_key.so
%{py_sitedir}/volume_key.py[co]
%endif

%if %{with python3}
%files -n python3-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_volume_key.so
%{py3_sitedir}/volume_key.py
%{py3_sitedir}/__pycache__/volume_key.cpython-*.py[co]
%endif
