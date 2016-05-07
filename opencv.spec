%global optflags %(echo %{optflags} -Wl,--as-needed )
#global indice   a
%bcond_with    ffmpeg
%bcond_without gstreamer
%bcond_with    eigen2
%bcond_with    eigen3
%bcond_with    openni
%bcond_with    tbb
%bcond_with    sse3
%bcond_with    cuda
%bcond_with    xine

Name:           opencv
Version:        3.1.0
Release:        4%{?dist}
Summary:        Collection of algorithms for computer vision
Group:          Development/Libraries
# This is normal three clause BSD.
License:        BSD
URL:            http://opencv.org
#Source0:	%{version}.zip
Source0:        https://github.com/Itseez/opencv/archive/%{version}/opencv-%{version}.tar.gz
#Source1:        opencv-samples-Makefile
# 
# Need to remove SIFT/SURF from source tarball, due to legal concerns
# export VERSION=3.1.0
# cd opencv_contrib-${VERSION}/
# rm -rf modules/xfeatures2d/
# cd ..; tar zcf opencv_contrib-clean-${VERSION}.tar.gz opencv_contrib-${VERSION}/
Source2:        opencv_contrib-clean-%{version}.tar.gz
#Source2:       https://github.com/Itseez/opencv_contrib/archive/%%{version}/opencv_contrib-%%{version}.tar.gz
#http://code.opencv.org/issues/2720
Patch2:         OpenCV-2.4.4-pillow.patch
#Patch3:         opencv-2.4.9-ts_static.patch
# fix/simplify cmake config install location (upstreamable)
# https://bugzilla.redhat.com/1031312
Patch4:         opencv-2.4.7-cmake_paths.patch
Patch5:         opencv-3.1.0-cmake_example.patch
Patch6:         OpenCV-3.1-pillow.patch

BuildRequires:  libtool
BuildRequires:  cmake >= 2.6.3
BuildRequires:  chrpath

%{?with_eigen2:BuildRequires:  eigen2-devel}
%{?with_eigen3:BuildRequires:  eigen3-devel}
BuildRequires:  gtk3-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
%if 0%{?fedora}
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel
BuildRequires:  libdc1394-devel
%endif
%endif
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libGL-devel
BuildRequires:  libv4l-devel
BuildRequires:  gtkglext-devel
BuildRequires:  OpenEXR-devel
%ifarch %{ix86} x86_64
%{?with_openni:
BuildRequires:  openni-devel
BuildRequires:  openni-primesense
}
%endif
%ifarch %{ix86} x86_64 ia64 ppc %{power64} aarch64
%{?with_tbb: 
BuildRequires:  tbb-devel
}
%endif
BuildRequires:  zlib-devel pkgconfig
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  numpy, swig >= 1.3.24
BuildRequires:  python3-numpy
BuildRequires:  python-sphinx
%{?with_ffmpeg:BuildRequires:  ffmpeg-devel >= 0.4.9}
%if 0%{?fedora} > 20
%{?with_gstreamer:BuildRequires:  gstreamer1-devel gstreamer1-plugins-base-devel}
%else
%{?with_gstreamer:BuildRequires:  gstreamer-devel gstreamer-plugins-base-devel}
%endif
%{?with_xine:BuildRequires:  xine-lib-devel}
BuildRequires:  opencl-headers
BuildRequires:  libgphoto2-devel
BuildRequires:  libwebp-devel
BuildRequires:  tesseract-devel
BuildRequires:  protobuf-devel
BuildRequires:  gdal-devel
BuildRequires:  glog-devel
BuildRequires:  doxygen
BuildRequires:  gflags-devel
BuildRequires:  SFML-devel
BuildRequires:  libucil-devel 
#BuildRequires:  libunicap-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  hdf5-devel
#ceres-solver-devel push eigen3-devel and tbb-devel, maybe we should enable all
#by default.
#BuildRequires:  ceres-solver-devel
#BuildRequires:  plantuml

Requires:       opencv-core%{_isa} = %{version}-%{release}


%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package        core
Summary:        OpenCV core libraries
Group:          Development/Libraries

%description    core
This package contains the OpenCV C/C++ core libraries.

%package        devel
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       %{name}-contrib%{_isa} = %{version}-%{release}

%description    devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library. You should consider installing opencv-devel-docs
package.

%package        devel-docs
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries
Requires:       opencv-devel = %{version}-%{release}
BuildArch:      noarch

%description    devel-docs
This package contains the OpenCV documentation and examples programs.

%package        python
Summary:        Python bindings for apps which use OpenCV
Group:          Development/Libraries
Requires:       opencv%{_isa} = %{version}-%{release}
Requires:       numpy
%{?python_provide:%python_provide python2-%{srcname}}

%description    python
This package contains Python bindings for the OpenCV library.

%package        python3
Summary:        Python3 bindings for apps which use OpenCV
Group:          Development/Libraries
Requires:       opencv%{_isa} = %{version}-%{release}
Requires:       numpy
%{?python_provide:%python_provide python3-%{srcname}}

%description    python3
This package contains Python3 bindings for the OpenCV library.


%package        contrib
Summary:        OpenCV contributed functionality
Group:          Development/Libraries

%description    contrib
This package is intended for development of so-called "extra" modules, contributed
functionality. New modules quite often do not have stable API, and they are not
well-tested. Thus, they shouldn't be released as a part of official OpenCV
distribution, since the library maintains binary compatibility, and tries
to provide decent performance and stability.

%prep
%setup -q -a2
# we don't use pre-built contribs
rm -rf 3rdparty/
%patch2 -p1 -b .pillow
#patch3 breaks build, need investigation
#patch3 -p1 -b .ts_static
%patch4 -p1 -b .cmake_paths
%patch5 -p1 -b .cmake_example
pushd opencv_contrib-%{version}
%patch6 -p1 -b .pillow
popd

# fix dos end of lines
#sed -i 's|\r||g'  samples/c/adaptiveskindetector.cpp


%build
# enabled by default if libraries are presents at build time:
# GTK, GSTREAMER, 1394, V4L, eigen3
# non available on Fedora: FFMPEG, XINE
mkdir -p build
pushd build

# disabling IPP because it is closed source library from intel

%cmake CMAKE_VERBOSE=1 \
 -DWITH_IPP=OFF \
 -DWITH_QT=ON \
 -DWITH_OPENGL=ON \
 -DWITH_GDAL=ON \
 -DWITH_UNICAP=ON \
 -DPYTHON_PACKAGES_PATH=%{python_sitearch} \
 -DCMAKE_SKIP_RPATH=ON \
 -DENABLE_PRECOMPILED_HEADERS:BOOL=OFF \
%ifnarch x86_64 ia64
 -DENABLE_SSE=OFF \
 -DENABLE_SSE2=OFF \
%endif
 %{!?with_sse3:-DENABLE_SSE3=OFF} \
 -DCMAKE_BUILD_TYPE=ReleaseWithDebInfo \
 -DBUILD_opencv_java=OFF \
%ifarch %{ix86} x86_64 ia64 ppc %{power64} aarch64
%{?with_tbb: -DWITH_TBB=ON } \
%endif
 %{!?with_gstreamer:-DWITH_GSTREAMER=OFF} \
 %{!?with_ffmpeg:-DWITH_FFMPEG=OFF} \
%{?with_cuda: \
 -DWITH_CUDA=ON \
 -DCUDA_TOOLKIT_ROOT_DIR=%{?_cuda_topdir} \
 -DCUDA_VERBOSE_BUILD=ON \
 -DCUDA_PROPAGATE_HOST_FLAGS=OFF \
} \
%ifarch %{ix86} x86_64
%{?with_openni: -DWITH_OPENNI=ON } \
%endif
 %{!?with_xine:-DWITH_XINE=OFF} \
 -DBUILD_EXAMPLES=ON \
 -DINSTALL_C_EXAMPLES=ON \
 -DINSTALL_PYTHON_EXAMPLES=ON \
 -DOPENCL_INCLUDE_DIR=${_includedir}/CL \
 -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-%{version}/modules \
 ..

make VERBOSE=1 %{?_smp_mflags}

#make html_docs

# We may build html_docs with: make html_docs
# we also got 234 rst files that are valid documentation.
# find opencv-2.4.11/ -name *rst | wc -l
# 234
# but make install does not install any doc (except OpenCV/samples), so I just added
# README.md index.rst with references to online documentation.
# Conclusion I think we miss one sub-package opencv-docs.noarch , but we got opencv-devel-docs.noarch

popd


%install
pushd build
make install DESTDIR=%{buildroot} INSTALL="install -p" CPPROG="cp -p"
find %{buildroot} -name '*.la' -delete

# install -pm644 %{SOURCE1} %{buildroot}%{_datadir}/OpenCV/samples/GNUmakefile

# remove unnecessary documentation
#rm -rf %{buildroot}%{_datadir}/OpenCV/doc

popd

%check
# Check fails since we don't support most video
# read/write capability and we don't provide a display
# ARGS=-V increases output verbosity
# Make test is unavailble as of 2.3.1
#ifnarch ppc64
#pushd build
#    LD_LIBRARY_PATH=%{_builddir}/%{tar_name}-%{version}/lib:$LD_LIBARY_PATH make test ARGS=-V || :
#popd
#endif

%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%license LICENSE
%{_bindir}/opencv_*
%{_libdir}/libopencv_ts*
%dir %{_datadir}/OpenCV
%{_datadir}/OpenCV/haarcascades
%{_datadir}/OpenCV/lbpcascades

%files core
%{_libdir}/libopencv_core.so.3.1*
%{_libdir}/libopencv_features2d.so.3.1*
%{_libdir}/libopencv_flann.so.3.1*
%{_libdir}/libopencv_highgui.so.3.1*
%{_libdir}/libopencv_imgcodecs.so.3.1*
%{_libdir}/libopencv_imgproc.so.3.1*
%{_libdir}/libopencv_ml.so.3.1*
%{_libdir}/libopencv_objdetect.so.3.1*
%{_libdir}/libopencv_photo.so.3.1*
%{_libdir}/libopencv_shape.so.3.1*
%{_libdir}/libopencv_stitching.so.3.1*
%{_libdir}/libopencv_superres.so.3.1*
%{_libdir}/libopencv_video.so.3.1*
%{_libdir}/libopencv_videoio.so.3.1*
%{_libdir}/libopencv_videostab.so.3.1*
%{_libdir}/libopencv_cvv.so.3.1*
#{_libdir}/libopencv_viz.so.3.1*

%files devel
%{_includedir}/opencv
%{_includedir}/opencv2
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/opencv.pc
%{_libdir}/OpenCV/*.cmake

%files devel-docs
%doc %{_datadir}/OpenCV/samples

%files python
%{python2_sitearch}/cv2.so

%files python3
%{python3_sitearch}/cv2.cpython-3*.so


%files contrib
%{_libdir}/libopencv_aruco.so.3.1*
%{_libdir}/libopencv_bgsegm.so.3.1*
%{_libdir}/libopencv_bioinspired.so.3.1*
%{_libdir}/libopencv_calib3d.so.3.1*
%{_libdir}/libopencv_ccalib.so.3.1*
%{_libdir}/libopencv_datasets.so.3.1*
%{_libdir}/libopencv_dnn.so.3.1*
%{_libdir}/libopencv_dpm.so.3.1*
%{_libdir}/libopencv_face.so.3.1*
%{_libdir}/libopencv_fuzzy.so.3.1*
%{_libdir}/libopencv_hdf.so.3.1*
%{_libdir}/libopencv_line_descriptor.so.3.1*
%{_libdir}/libopencv_optflow.so.3.1*
%{_libdir}/libopencv_plot.so.3.1*
%{_libdir}/libopencv_reg.so.3.1*
%{_libdir}/libopencv_rgbd.so.3.1*
%{_libdir}/libopencv_saliency.so.3.1*
%{_libdir}/libopencv_stereo.so.3.1*
%{_libdir}/libopencv_structured_light.so.3.1*
%{_libdir}/libopencv_surface_matching.so.3.1*
%{_libdir}/libopencv_text.so.3.1*
%{_libdir}/libopencv_tracking.so.3.1*
%{_libdir}/libopencv_ximgproc.so.3.1*
%{_libdir}/libopencv_xobjdetect.so.3.1*
%{_libdir}/libopencv_xphoto.so.3.1*

%changelog
* Sat May 07 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-4
- Put all idefs and ifarchs outside the scope of rpm conditional builds, rather
than vice versa, as had organized some time ago, it seems to me more correct.
- Remove SIFT/SURF from source tarball in opencv_contrib, due to legal concerns
- Redo and readd OpenCV-2.4.4-pillow.patch .
- Add OpenCV-3.1-pillow.patch to apply only opencv_contrib .
- Add the %python_provide macro (Packaging:Python guidelines). 

* Fri Apr 22 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-3
- Use always ON and OFF instead 0 and 1 in cmake command.
- Remove BUILD_TEST and TBB_LIB_DIR variables not used by cmake.
- Add BRs: tesseract-devel, protobuf-devel, glog-devel, doxygen,
  gflags-devel, SFML-devel, libucil-devel, qt5-qtbase-devel, mesa-libGL-devel,
  mesa-libGLU-devel and hdf5-devel.
- Remove BR: vtk-devel because VTK support is disabled. Incompatible 
  combination: OpenCV + Qt5 and VTK ver.6.2.0 + Qt4
- Enable build with Qt5.
- Enable build with OpenGL.
- Enable build with UniCap.
- Also requires opencv-contrib when install opencv-devel (#1329790).

* Wed Apr 20 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-2
- Add BR:libwebp-devel .
- Merge from 2.4.12.3 package: 
  Add aarch64 and ppc64le to list of architectures where TBB is supported (#1262788).
  Use bcond tags to easily enable or disable modules.
  Fix unused-direct-shlib-dependency in cmake with global optflags.
  Added README.md with references to online documentation.
  Investigation on the documentation, added a few notes.
- Update to 3.1.0 (Fri Mar 25 2016 Pavel Kajaba <pkajaba@redhat.com> - 3.1.0-1)
- Added opencv_contrib (Thu Jul 09 2015 Sérgio Basto <sergio@serjux.com> -
  3.0.0-2)
- Update to 3.0.0 (Fri Jun 05 2015 Jozef Mlich <jmlich@redhat.com> - 3.0.0-1)

* Tue Mar 01 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.12.3-3
- Fix FTBFS with GCC 6 (#1307821)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Sérgio Basto <sergio@serjux.com> - 2.4.12.3-1
- Update opencv to 2.4.12.3 (#1271460).
- Add aarch64 and ppc64le to list of architectures where TBB is supported (#1262788).

* Tue Jul 14 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-5
- Use bcond tags to easily enable or disable modules.
- Package review, more cleaning in the spec file.
- Fixed unused-direct-shlib-dependency in cmake with global optflags.
- Added README.md index.rst with references to online documentation.
- Investigation on the documentation, added a few notes.

* Mon Jul 06 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-4
- Enable-gpu-module, rhbz #1236417, thanks to Rich Mattes.
- Deleted the global gst1 because it is no longer needed.

* Thu Jun 25 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-3
- Fix license tag

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-1
- Update to 2.4.11 .
- Dropped patches 0, 10, 11, 12, 13 and 14 .

* Sat Apr 11 2015 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-6
- rebuild (gcc5)

* Mon Feb 23 2015 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-5
- rebuild (gcc5)

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-4
- rebuild (openexr)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-2
- backport support for GStreamer 1 (#1123078)

* Thu Jul 03 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4.9-1
- Update to 2.4.9

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Rex Dieter <rdieter@fedoraproject.org> 2.4.7-6
- revert pkgcmake2 patch (#1070428)

* Fri Jan 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4.7-5
- Fix opencv_ocl isn't part of -core

* Thu Jan 16 2014 Christopher Meng <rpm@cicku.me> - 2.4.7-4
- Enable OpenCL support.
- SPEC small cleanup.

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.7-3
- rebuild (openexr)

* Mon Nov 18 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.7-2
- OpenCV cmake configuration broken (#1031312)

* Wed Nov 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.7-1
- Update to 2.4.7

* Sun Sep 08 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.6.1-2
- rebuild (openexr)

* Wed Jul 24 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.6.1-1
- Update to 2.4.6.1

* Thu May 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.5-1
- Update to 2.4.5-clean
- Spec file clean-up
- Split core libraries into a sub-package

* Sat May 11 2013 François Cami <fcami@fedoraproject.org> - 2.4.4-3
- change project URL.

* Tue Apr 02 2013 Tom Callaway <spot@fedoraproject.org> - 2.4.4-2
- make clean source without SIFT/SURF

* Sat Mar 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.4-1
- Update to 2.4.4a
- Fix tbb-devel architecture conditionals

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.4-0.2.beta
- rebuild (OpenEXR)

* Mon Feb 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.4-0.1.beta
- Update to 2.4.4 beta
- Drop python-imaging also from requires
- Drop merged patch for additionals codecs
- Disable the java binding for now (untested)

* Fri Jan 25 2013 Honza Horak <hhorak@redhat.com> - 2.4.3-7
- Do not build with 1394 libs in rhel

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 2.4.3-6
- rebuild due to "jpeg8-ABI" feature drop

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-5
- Add more FourCC for gstreamer - rhbz#812628
- Allow to use python-pillow - rhbz#895767

* Mon Nov 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-3
- Switch Build Type to ReleaseWithDebInfo to avoid -03

* Sun Nov 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-2
- Disable SSE3 and allow --with sse3 build conditional.
- Disable gpu module as we don't build cuda
- Update to 2.4.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Honza Horak <hhorak@redhat.com> - 2.4.2-1
- Update to 2.4.2

* Fri Jun 29 2012 Honza Horak <hhorak@redhat.com> - 2.4.1-2
- Fixed cmake script for generating opencv.pc file
- Fixed OpenCVConfig script file

* Mon Jun 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-1
- Update to 2.4.1
- Rework dependencies - rhbz#828087
  Re-enable using --with tbb,openni,eigen2,eigen3

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-8
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-7
- Update gcc46 patch for ARM FTBFS

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 2.3.1-5
- Rebuild for new libpng

* Thu Oct 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-4
- Rebuilt for tbb silent ABI change

* Mon Oct 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-3
- Update to 2.3.1a

* Mon Sep 26 2011 Dan Horák <dan[at]danny.cz> - 2.3.1-2
- openni is exclusive for x86/x86_64

* Fri Aug 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-1
- Update to 2.3.1
- Add BR openni-devel python-sphinx
- Remove deprecated cmake options
- Add --with cuda conditional (wip)
- Disable make test (unavailable)

* Thu May 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-6
- Backport fixes from branch 2.2 to date

* Tue May 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-5
- Re-enable v4l on f15
- Remove unused cmake options

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-2
- Fix with gcc46
- Disable V4L as V4L1 is disabled for Fedora 15

* Thu Jan 06 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-1
- Update to 2.2.0
- Disable -msse and -msse2 on x86_32

* Wed Aug 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.1.0-5
- -devel: include OpenCVConfig.cmake (#627359)

* Thu Jul 22 2010 Dan Horák <dan[at]danny.cz> - 2.1.0-4
- TBB is available only on x86/x86_64 and ia64

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 25 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-2
- Move samples from main to -devel
- Fix spurious permission
- Add BR tbb-devel
- Fix CFLAGS

* Fri Apr 23 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- Update libdir patch

* Tue Apr 13 2010 Karel Klic <kklic@redhat.com> - 2.0.0-10
- Fix nonstandard executable permissions

* Tue Mar 09 2010 Karel Klic <kklic@redhat.com> - 2.0.0-9
- apply the previously added patch

* Mon Mar 08 2010 Karel Klic <kklic@redhat.com> - 2.0.0-8
- re-enable testing on CMake build system
- fix memory corruption in the gaussian random number generator

* Sat Feb 27 2010 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-7
- replaced BR unicap-devel by libucil-devel (unicap split)

* Thu Feb 25 2010 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-6
- use cmake build system
- applications renamed to opencv_xxx instead of opencv-xxx
- add devel-docs subpackage #546605
- add OpenCVConfig.cmake
- enable openmp build
- enable old SWIG based python wrappers
- opencv package is a good boy and use global instead of define

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

* Thu Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.6.pre1
- Fix typo I introduced that prevented build on i386/i586

* Thu Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.5.pre1
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
