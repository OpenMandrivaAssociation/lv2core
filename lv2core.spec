%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:    The core LV2 specification
Name:       lv2core
Version:    4.0
Release:    %mkrel 1
Group:      System/Libraries
License:    LGPL
URL:        http://lv2plug.in/
Source0:    http://lv2plug.in/spec/%{name}-%{version}.tar.bz2
BuildRequires:  pkgconfig
BuildRequires:  python
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
LV2 is a standard for plugins and matching host applications, primarily
targeted at audio processing and generation.

LV2 is a successor to LADSPA, created to address the limitations of LADSPA
which many applications have outgrown.  Compared to LADSPA, all plugin data
is moved from the code to a separate data file, and the code has been made as
generic as possible.  As a result, LV2 can be independently extended
(retaining compatibility wherever possible), and virtually any feasible
plugin features can be implemented in an LV2 plugin.

The major version of this package refers to the LV2 specification revision
contained, while the minor version refers only to this package.

%package    devel
Summary:    Development files for the core LV2 specification
Group:      Development/C
Requires:   %{name} = %{version}

%description    devel
This package contains development files for the core LV2 specification.

%prep

%setup -q -n %{name}-%{version}

%build
perl -pi -e "s|/lib\b|/%{_lib}|g" lv2config.c
python ./waf configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir}

python ./waf build

%install
rm -rf %{buildroot}

DESTDIR=%{buildroot} python ./waf install

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" %{buildroot}%{_libdir}/pkgconfig/lv2core.pc

%clean
rm -rf %{buildroot}

%post
%{_bindir}/lv2config


%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README
%dir %{_libdir}/lv2/lv2core.lv2
%{_libdir}/lv2/lv2core.lv2/lv2.ttl
%{_libdir}/lv2/lv2core.lv2/manifest.ttl
%{_bindir}/lv2config

%files devel
%defattr(-,root,root)
%{_includedir}/lv2.h
%{_libdir}/pkgconfig/lv2core.pc
%{_libdir}/lv2/lv2core.lv2/lv2.h
