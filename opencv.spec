%define with_ffmpeg 0

%define pythondir %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib()')
%define pyexecdir %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')

Name:           opencv
Version:        0.9.7
Release:        17%{?dist}
Summary:        Collection of algorithms for computer vision

Group:          Development/Libraries
License:        Intel Open Source License
URL:            http://www.intel.com/technology/computing/opencv/index.htm
Source0:        http://prdownloads.sourceforge.net/opencvlibrary/opencv-%{version}.tar.gz
Source1:        opencv-samples-Makefile
Patch0:         opencv-0.9.7-intrinsics-simple.patch
Patch1:         opencv-0.9.7-pythondir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf, automake, libtool
BuildRequires:  gtk2-devel, libpng-devel, libjpeg-devel, libtiff-devel
BuildRequires:  swig >= 1.3.24, zlib-devel, pkgconfig
BuildRequires:  python-devel
%if %{with_ffmpeg}
BuildRequires:  ffmpeg-devel >= 0.4.9
%endif

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package devel
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries
Requires:       opencv = %{version}-%{release}

%description devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library.


%package python
Summary:        Python bindings for apps which use OpenCV
Group:          Development/Libraries
Requires:       opencv = %{version}-%{release}
Requires:       python-abi = %(%{__python} -c "import sys ; print sys.version[:3]")

%description python
This package contains Python bindings for the OpenCV library.


%prep
%setup -q
%patch0 -p1 -b .intrinsics
%patch1 -p1 -b .pythondir
%{__sed} -i 's/\r//' interfaces/swig/python/*.py \
                     samples/python/*.py
%{__sed} -i 's/^#!.*//' interfaces/swig/python/adaptors.py \
                        interfaces/swig/python/__init__.py
autoreconf -vif


%build
%configure --disable-static --enable-python --with-apps
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la \
      $RPM_BUILD_ROOT%{pyexecdir}/opencv/*.la \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/build_all.sh \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/cvsample.dsp \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/cvsample.vcproj \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/facedetect.cmd \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/makefile.gcc \
      $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/makefile.gen
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/opencv/samples/c/Makefile


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%post python -p /sbin/ldconfig
%postun python -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING THANKS TODO
%{_bindir}/opencv-*
%{_libdir}/lib*.so.*
%dir %{_datadir}/opencv
%{_datadir}/opencv/haarcascades
%{_datadir}/opencv/readme.txt


%files devel
%defattr(-,root,root,-)
%{_includedir}/opencv
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/opencv.pc
%doc %{_datadir}/opencv/doc
%doc %{_datadir}/opencv/samples/c


%files python
%dir %{pythondir}/opencv
%{pythondir}/opencv/*.py
%{pythondir}/opencv/*.pyc
%ghost %{pythondir}/opencv/*.pyo
%{pyexecdir}/opencv
%doc %{_datadir}/opencv/samples/python


%changelog
* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.7-17
- Rebuild for FC6.
- BR: libtool.

* Fri Mar 17 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-16
- Rebuild.

* Wed Mar  8 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-15
- Force a re-run of Autotools by calling autoreconf.

* Wed Mar  8 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-14
- Added build dependency on Autotools.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-13
- Changed intrinsics patch so that it matches upstream.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-12
- More intrinsics patch fixing.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-11
- Don't do "make check" because it doesn't run any tests anyway.
- Back to main intrinsics patch.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-10
- Using simple intrinsincs patch.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-9
- Still more fixing of intrinsics patch for Python bindings on x86_64.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-8
- Again fixed intrinsics patch so that Python modules build on x86_64.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-7
- Fixed intrinsics patch so that it works.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-6
- Fixed Python bindings location on x86_64.

* Mon Mar  6 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-5
- SSE2 support on x86_64.

* Mon Mar  6 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-4
- Rebuild

* Sun Oct 16 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-3
- Removed useless sample compilation makefiles/project files and replaced them
  with one that works on Fedora Core.
- Removed shellbang from Python modules.

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-2
- Made FFMPEG dependency optional (needs to be disabled for inclusion in FE).

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-1
- Initial package.
