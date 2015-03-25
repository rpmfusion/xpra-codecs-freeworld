# This package provides H.264 and swscale support for Xpra.
# 

# Remove private provides from .so files in the python_sitearch directory
%global __provides_exclude_from ^%{python_sitearch}/.*\\.so$

Name:           xpra-codecs-freeworld
Version:        0.14.21
Release:        2%{?dist}
Summary:        Additional codecs for xpra using x264 and ffmpeg

License:        GPLv2+
URL:            http://www.xpra.org/
Source0:        http://xpra.org/src/xpra-%{version}.tar.xz


BuildRequires:  python2-devel pygobject2-devel pygtk2-devel
BuildRequires:  libXtst-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  Cython
BuildRequires:  desktop-file-utils
BuildRequires:  libvpx-devel
BuildRequires:  libwebp-devel
BuildRequires:  x264-devel
BuildRequires:  ffmpeg-devel

Requires:       xpra = %{version}
Requires:       gstreamer-plugins-ugly

%description
Provides support for H.264 encoding and swscale support in xpra using
x264 and ffmpeg.

%prep
%setup -q -n xpra-%{version}

%build
CFLAGS="%{optflags}" %{__python} setup.py build \
    --with-vpx \
    --with-webp \
    --with-enc_x264 \
    --with-dec_avcodec \
    --with-csc_swscale \
    --with-Xdummy \
    --with-Xdummy_wrapper

%install
mkdir destdir
%{__python} setup.py install --skip-build --root destdir

mkdir -p %{buildroot}%{python_sitearch}/xpra/codecs/
pushd destdir%{python_sitearch}/xpra/codecs/
cp -pr csc_swscale dec_avcodec enc_x264 \
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
%doc COPYING

%changelog
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
