%define lib_name_orig   %{mklibname qtpod}
%define lib_name        %{mklibname qtpod 0}
%define lib_name_devel  %{mklibname qtpod -d}

Summary:        Provides access to the contents of an Apple iPod
Name:           libqtpod
Version:        0.4.1
Release:        %mkrel 1
Epoch:          0
License:        LGPL
Group:          System/Libraries
URL:            http://sourceforge.net/projects/kpod/
Source0:        http://downloads.sourceforge.net/sourceforge/kpod/libqtpod-%{version}.tar.bz2
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

%package -n %{lib_name_devel}
Group:           Development/C++
Summary:         Shared libraries and header files for the libqtpod library
Provides:        qtpod-devel = %{epoch}:%{version}-%{release}
Requires:        %{lib_name} = %{epoch}:%{version}-%{release}
Obsoletes:       %{mklibname qtpod 0}-devel < %{epoch}:%{version}-%{release}

%description -n %{lib_name_devel}
The %{name} package contains the shared libraries and header files 
needed for developing libqtpod applications.

%prep
%setup -q
%{__perl} -pi -e 's/^target\.path = .*$/target.path = \$(libdir)/' src/src.pro

%build
export QTDIR=%{qt3dir}
${QTDIR}/bin/qmake
export PATH=${QTDIR}/bin:${PATH}
%{__make} CXXFLAGS="%{optflags} -fPIC"

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot} libdir=%{_libdir}

%{__mkdir_p} %{buildroot}%{_includedir}
%{__mv} %{buildroot}/libqtpod %{buildroot}%{_includedir}

%clean
%{__rm} -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -n %{lib_name}
%defattr(-,root,root,0755)
%doc Changelog COPYING INSTALL README
%{_libdir}/*.so.*

%files -n %{lib_name_devel}
%defattr(-,root,root,0755)
%doc docs
%{_includedir}/%{name}
%{_libdir}/*.so
