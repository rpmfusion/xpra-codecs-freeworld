Name:           xpra-codecs-freeworld
Version:        0.17.5
Release:        1%{?dist}
Summary:        Additional codecs for xpra using x264 and ffmpeg

License:        GPLv2+
URL:            http://www.xpra.org/
Source0:        http://xpra.org/src/xpra-%{version}.tar.xz

BuildRequires:  python2-devel pygobject2-devel pygtk2-devel
BuildRequires:  libXtst-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  Cython
BuildRequires:  desktop-file-utils
BuildRequires:  libwebp-devel
BuildRequires:  x264-devel
BuildRequires:  ffmpeg-devel

Requires:       xpra = %{version}
Requires:       gstreamer1-plugins-ugly

%description
Provides support for H.264 encoding and swscale support in xpra using
x264 and ffmpeg.

%prep
%setup -q -n xpra-%{version}


%build
CFLAGS="%{optflags}" %{__python} setup.py build \
    --with-enc_x264 \
    --with-dec_avcodec2 \
    --with-csc_swscale \
    --with-Xdummy \
    --with-Xdummy_wrapper

%install
mkdir destdir
%{__python} setup.py install --skip-build --root destdir

mkdir -p %{buildroot}%{python_sitearch}/xpra/codecs/
pushd destdir%{python_sitearch}/xpra/codecs/
cp -pr csc_swscale dec_avcodec2 enc_x264 libav_common \
        %{buildroot}%{python_sitearch}/xpra/codecs/
popd

#drop shebangs from python_sitearch
find %{buildroot}%{python_sitearch}/xpra -name '*.py' \
    -exec sed -i '1{\@^#!/usr/bin/env python@d}' {} \;
    
#fix permissions on shared objects
find %{buildroot}%{python_sitearch}/xpra -name '*.so' \
    -exec chmod 0755 {} \;

%files
%{python_sitearch}/xpra/codecs/*
%license COPYING

%changelog
* Sun Sep 11 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.17.5-1
- Update to 0.17.5
- Remove xpra-0.17.x-12944.patch

* Sun Jul 31 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.17.4-2
- Add xpra-0.17.x-12944.patch to fix build failure with latest ffmpeg
- Fix bogus changelog date in spec file

* Sun Jul 31 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.17.4-1
- Update to 0.17.4

* Sat Apr  2 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.16.3-2
- Remove macro definition stripping provides from .so files in
  the python_sitearch directory - no longer needed

* Sat Apr  2 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.16.3-1
- Update to 0.16.3

* Fri Feb 19 2016 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.16.2-1
- Update to 0.16.2
- Change Requires from gstreamer-plugins-ugly to gstreamer1-plugins-ugly
- Add codecs/libav_common

* Sat Dec 19 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.15.10-1
- Update to 0.15.10

* Wed Dec  2 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.15.9-1
- Update to 0.15.9

* Tue Nov 24 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.15.8-1
- Update to 0.15.8

* Thu Sep 17 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.15.6-1
- Update to 0.15.6

* Wed Sep  2 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.15.5-2
- Remove --with-webp build option

* Wed Sep  2 2015 Jonathan Underwood <jonathan.underwood@gmail.com> - 0.15.5-1
- Update to 0.15.5

* Wed Aug  5 2015 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.15.4-2
- Remove --with-vpx from setup options
- Remove BuildRequires:  libvpx-devel
- Use %%license tag for COPYING file

* Wed Aug  5 2015 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.15.4-1
- Update to 0.15.4

* Tue Mar 24 2015 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.14.21-2
- Remove vpx codec - that's now packaged with the main xpra package

* Mon Mar 23 2015 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.14.21-1
- Update to 0.14.21
- Update summary and description
- Tighten xpra requirement to be same version
- Remove out of date comment about libvpx

* Fri Oct 18 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.6-1
- new upstream release 0.10.6
  http://lists.devloop.org.uk/pipermail/shifter-users/2013-October/000726.html

* Tue Oct 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.4-2
- ship webp support in Fedora package (it is actually useful there)
- include explanation from upstream as to why libswscale is required
- require gstreamer-plugins-ugly (for MP3 audio streams)

* Mon Oct 07 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.10.4-1
- rebase to 0.10.4
- loosen dependency on main xpra package
- add comment explaining libvpx situation

* Thu Mar 28 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.8-2
- split off plugins that can't be in Fedora proper

* Thu Mar 14 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.8-1
- initial package
