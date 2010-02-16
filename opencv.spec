%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define tar_name OpenCV

Name:           opencv
Version:        2.0.0
Release:        5%{?dist}
Summary:        Collection of algorithms for computer vision

Group:          Development/Libraries
# This is normal three clause BSD.
License:        BSD
URL:            http://opencv.willowgarage.com/wiki/
Source0:        http://prdownloads.sourceforge.net/opencvlibrary/%{tar_name}-%{version}.tar.bz2
Source1:        opencv-samples-Makefile
Patch0:         opencv-2.0.0-data-automake.patch
Patch1:         opencv-2.0.0-apps-automake.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool

BuildRequires:  gtk2-devel
BuildRequires:  unicap-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel
BuildRequires:  libdc1394-devel
%endif
BuildRequires:  jasper-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libtool
BuildRequires:  swig >= 1.3.24, zlib-devel, pkgconfig
BuildRequires:  python-devel
BuildRequires:  python-imaging, numpy
%{?_with_ffmpeg:BuildRequires:  ffmpeg-devel >= 0.4.9}
%{!?_without_gstreamer:BuildRequires:  gstreamer-devel}
%{?_with_xine:BuildRequires:  xine-lib-devel}

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package devel
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries
Requires:       opencv = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library.


%package python
Summary:        Python bindings for apps which use OpenCV
Group:          Development/Libraries
Requires:       opencv = %{version}-%{release}
Requires:       python-imaging
Requires:       numpy

%description python
This package contains Python bindings for the OpenCV library.


%prep
%setup -q -n %{tar_name}-%{version}
%patch0 -p1 -b .automake
%patch1 -p1 -b .automake
#Renew the autotools (and remove rpath).
autoreconf -vif

%build

%ifarch i386
export CXXFLAGS="%{__global_cflags} -m32 -fasynchronous-unwind-tables"
%endif

export SWIG_PYTHON_LIBS=%{_libdir}
%configure --disable-static --enable-apps \
  %{?_with_ffmpeg:--with-ffmpeg}%{!?_with_ffmpeg:--without-ffmpeg} \
  %{!?_without_gstreamer:--with-gstreamer} \
  %{?_with_xine:--with-xine --without-quicktime} \
  --with-unicap \
  --with-1394libs --without-quicktime \
%ifarch i386 i586
  --disable-sse2 \
%endif

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" CPPROG="cp -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/samples/c/build_all.sh \
      $RPM_BUILD_ROOT%{_datadir}/%{name}/samples/c/cvsample.dsp \
      $RPM_BUILD_ROOT%{_datadir}/%{name}/samples/c/cvsample.vcproj \
      $RPM_BUILD_ROOT%{_datadir}/%{name}/samples/c/facedetect.cmd
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/samples/c/GNUmakefile
install -m644 cvconfig.h $RPM_BUILD_ROOT%{_includedir}/%{name}/cvconfig.h

#Remove unversioned documentation
rm -rf $RPM_BUILD_ROOT%{_docdir}/opencv
#And Octave since we don't build against it yet
rm -rf $RPM_BUILD_ROOT%{_datadir}/opencv/{samples/octave/,ChangeLog,THANKS}


%check
#Check fails since we don't support most video
#read/write capability and we don't provide a display
%ifnarch ppc64
    make check || :
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig



%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING THANKS TODO
%{_bindir}/opencv-*
%{_libdir}/lib*.so.*
%dir %{_datadir}/opencv
%{_datadir}/opencv/haarcascades
%{_datadir}/opencv/lbpcascades
%{_datadir}/opencv/readme.txt


%files devel
%defattr(-,root,root,-)
%{_includedir}/opencv
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/opencv.pc
%doc %{_datadir}/doc/opencv-2.0.0/
%doc %dir %{_datadir}/opencv/samples
%doc %{_datadir}/opencv/samples/c
%doc %{_datadir}/opencv/samples/CMake


%files python
%defattr(-,root,root,-)
%{python_sitearch}/opencv
%doc %dir %{_datadir}/opencv/samples
%doc %{_datadir}/opencv/samples/python


%changelog
* Tue Feb 16 2010 Karel Klic <kklic@redhat.com> - 2.0.0-5
- Set CXXFLAXS without -match=i386 for i386 architecture #565074

* Sat Jan 09 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 2.0.0-4
- Updated opencv-samples-Makefile (Thanks Scott Tsai) #553697

* Wed Jan 06 2010 Karel Klic <kklic@redhat.com> - 2.0.0-3
- Fixed spec file issues detected by rpmlint

* Sun Dec 06 2009 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-2
- Fix autotools scripts (missing LBP features) - #544167 

* Fri Nov 27 2009 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-1
- Updated to 2.0.0
- Removed upstream-ed patches
- Ugly hack (added cvconfig.h)
- Disable %%check on ppc64

* Thu Sep 10 2009 Karsten Hopp <karsten@redhat.com> - 1.1.0-0.7.pre1
- fix build on s390x where we don't have libraw1394 and devel

* Fri Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.6.pre1
- Fix typo I introduced that prevented build on i386/i586

* Fri Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.5.pre1
- Added 1394 libs and unicap support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.4.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.3.pre1
- Build with gstreamer support - #491223
- Backport gcc43 fix from trunk

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.2.pre1
- Fix FTBFS #511705

* Fri Apr 24 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.1.pre1
- Update to 1.1pre1
- Disable CXXFLAGS hardcoded optimization
- Add BR: python-imaging, numpy
- Disable make check failure for now

* Wed Apr 22 2009 kwizart < kwizart at gmail.com > - 1.0.0-14
- Fix for gcc44
- Enable BR jasper-devel
- Disable ldconfig run on python modules (uneeded)
- Prevent timestamp change on install

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 1.0.0-12
- fix URL field

* Fri Dec 19 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.0.0-11
- Adopt latest python spec rules.
- Rebuild for Python 2.6 once again.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.0-10
- Rebuild for Python 2.6

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.0-9
- fix license tag

* Sun May 11 2008 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-8
- Adjust library order in opencv.pc.in (BZ 445937).

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-7
- Autorebuild for GCC 4.3

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-6
- Rebuild for gcc43.

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.0.0-5
- Rebuild for selinux ppc32 issue.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-4
- Mass rebuild.

* Thu Mar 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-3
- Fix %%{_datadir}/opencv/samples ownership.
- Adjust timestamp of cvconfig.h.in to avoid re-running autoheader.

* Thu Mar 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-2
- Move all of the python module to pyexecdir (BZ 233128).
- Activate the testsuite.

* Mon Dec 11 2006 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-1
- Upstream update.

* Mon Dec 11 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-4
- Remove python-abi.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.9-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-2
- Stop configure.in from hacking CXXFLAGS.
- Activate testsuite.
- Let *-devel require pkgconfig.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-1
- Upstream update.
- Don't BR: autotools.
- Install samples' Makefile as GNUmakefile.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.7-18
- Un'%%ghost *.pyo.
- Separate %%{pythondir} from %%{pyexecdir}.

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
