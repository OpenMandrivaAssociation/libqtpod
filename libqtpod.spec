%define lib_major       0
%define lib_name_orig   %mklibname qtpod
%define lib_name        %{lib_name_orig}%{lib_major}

Summary:        Provides access to the contents of an Apple iPod
Name:           libqtpod
Version:        0.3
Release:        %mkrel 3
Epoch:          0
URL:            http://sourceforge.net/projects/kpod/
Source0:        http://umn.dl.sourceforge.net/sourceforge/kpod/libqtpod-%{version}.tar.bz2
License:        LGPL
Group:          System/Libraries
BuildRequires:  doxygen
BuildRequires:  qt3-devel
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
LibQtPod provides access to the contents of an Apple iPod. The code was
formerly part of the kio ipodslave, but is now a separate Qt-based library. 
The library features reading and writing of the iTunesDB music database and
provides access to hardware specific information like disc space statistics.

%package -n %{lib_name}
Summary:        Main library for the libqtpod library
Group:          System/Libraries

%description -n %{lib_name}
The %{name} package contains the libraries needed to run programs dynamically 
linked with the libqtpod library.

%package -n %{lib_name}-devel
Group:           Development/C++
Summary:         Shared libraries and header files for the libqtpod library
Provides:        %{name}-devel
Provides:        %{lib_name_orig}-devel
Requires:        %{lib_name} = %{epoch}:%{version}

%description -n %{lib_name}-devel
The %{name} package contains the shared libraries and header files 
needed for developing libqtpod applications.

%prep
%setup -q
%{__perl} -pi -e 's/^target\.path = .*$/target.path = \$(libdir)/' src/src.pro
%{__perl} -pi -e 's/^OUTPUT_DIRECTORY.*=.*$/OUTPUT_DIRECTORY = docs/;' -e 's/^INPUT.*=.*$/INPUT = src/' Doxyfile

%build
export QTDIR=%{_prefix}/lib/qt3
%{_bindir}/qmake
%{__make} CXXFLAGS="%{optflags} -fPIC"
%{_bindir}/doxygen

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot} libdir=%{_libdir}
%{__mkdir_p} %{buildroot}%{_includedir}
%{__mv} %{buildroot}/libqtpod %{buildroot}%{_includedir}

%clean
%{__rm} -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root)
%doc Changelog COPYING INSTALL README
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc docs
%{_includedir}/%{name}
%{_libdir}/*.so


