%define with_ffmpeg 0

Name:           opencv
Version:        0.9.7
Release:        3
Summary:        Collection of algorithms for computer vision

Group:          Development/Libraries
License:        Intel Open Source License
URL:            http://www.intel.com/technology/computing/opencv/index.htm
Source0:        http://prdownloads.sourceforge.net/opencvlibrary/opencv-%{version}.tar.gz
Source1:        opencv-samples-Makefile
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
Requires:       %{_libdir}/python%(echo `python -c "import sys; print sys.version[0:3]"`)

%description python
This package contains Python bindings for the OpenCV library.


%prep
%setup -q
%{__sed} -i 's/\r//' interfaces/swig/python/*.py \
                     samples/python/*.py
%{__sed} -i 's/^#!.*//' interfaces/swig/python/adaptors.py \
                        interfaces/swig/python/__init__.py


%build
%configure --disable-static --enable-python --with-apps
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la \
      $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/opencv/*.la \
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
%{_libdir}/python*/site-packages/opencv
%doc %{_datadir}/opencv/samples/python


%changelog
* Sun Oct 16 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-3
- Removed useless sample compilation makefiles/project files and replaced them
  with one that works on Fedora Core.
- Removed shellbang from Python modules.

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-2
- Made FFMPEG dependency optional (needs to be disabled for inclusion in FE).

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-1
- Initial package.
