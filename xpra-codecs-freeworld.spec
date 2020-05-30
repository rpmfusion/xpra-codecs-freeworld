%bcond_without enc_x264
%bcond_without dec_avcodec2
%bcond_without csc_swscale

# For debugging only
%bcond_with debug
%if !%{without debug}
%global _with_debug --with-debug
%endif
#

# These are nececessary as the _with_foo is *not* defined if the
# --with flag isn't specifed, and we need to have the --without
# specified option in that case.
%if %{without enc_x264}
%global _with_enc_x264 --without-enc_x264
%endif

%if %{without dec_avcodec2}
%global _with_dec_avcodec2 --without-dec_avcodec2
%endif

%if %{without csc_swscale}
%global _with_csc_swscale --without-csc_swscale
%endif

Name:           xpra-codecs-freeworld
Version:        4.0.1
Release:        2%{?dist}
Summary:        Additional codecs for xpra using x264 and ffmpeg
License:        GPLv2+
URL:            http://www.xpra.org/
Source0:        http://xpra.org/src/xpra-%{version}.tar.xz

BuildRequires:  python3-devel
BuildRequires:  python3-gobject-devel
BuildRequires:  python3-cairo-devel
BuildRequires:  pygtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  libXtst-devel
BuildRequires:  libxkbfile-devel, libvpx-devel
BuildRequires:  xvidcore-devel, x265-devel
BuildRequires:  python3-Cython, ack
BuildRequires:  gcc
BuildRequires:  libwebp-devel
BuildRequires:  libXdamage-devel
%if %{with debug}
BuildRequires: libasan
%endif

%if %{with enc_x264}
BuildRequires:  x264-devel
%endif
%if %{with dec_avcodec2} || %{with csc_swscale}
BuildRequires:  ffmpeg-devel
%endif

Requires:       xpra%{?_isa} = %{version}
Requires:       gstreamer1-plugins-ugly%{?_isa}

%description
Provides support for H.264 encoding and swscale support in xpra using
x264 and ffmpeg.

%prep
%autosetup -n xpra-%{version}

# cc1: error: unrecognized compiler option ‘-mfpmath=387’
%ifarch %{arm}
sed -i 's|-mfpmath=387|-mfloat-abi=hard|' setup.py
%endif

%build
%py3_build -- %{?_with_enc_x264} \
 %{?_with_dec_avcodec2} \
 %{?_with_csc_swscale} \
 %{?_with_debug} \
 --with-Xdummy \
 --with-Xdummy_wrapper \
 --with-enc_ffmpeg \
 --without-html5 \
 --without-tests \
 --with-verbose \
 --without-strict \
 --without-html5_gzip --without-html5_brotli

%install
%py3_install -- --root destdir --without-html5_gzip --without-html5_brotli

## We are interested to additional codecs only
mkdir -p %{buildroot}%{python3_sitearch}/xpra/codecs/
pushd destdir%{python3_sitearch}/xpra/codecs/
cp -pr \
%if %{with csc_swscale}
 csc_swscale \
%endif
%if %{with dec_avcodec2}
 dec_avcodec2 \
%endif
%if %{with enc_x264}
 enc_x264 \
%endif
 libav_common enc_ffmpeg enc_x265 %{buildroot}%{python3_sitearch}/xpra/codecs/
popd

#fix shebangs from python3_sitearch
find %{buildroot}%{python3_sitearch}/xpra -name '*.py' | xargs pathfix.py -pn -i "%{__python3}"
for i in `ack -rl '^#!/.*python' %{buildroot}%{python3_sitearch}/xpra`; do
    chmod 0755 $i
done
    
#fix permissions on shared objects
find %{buildroot}%{python3_sitearch}/xpra -name '*.so' \
    -exec chmod 0755 {} \;

%files
%dir %{python3_sitearch}/xpra
%dir %{python3_sitearch}/xpra/codecs
%{python3_sitearch}/xpra/codecs/*
%doc README NEWS
%license COPYING

%changelog
* Sat May 30 2020 Leigh Scott <leigh123linux@gmail.com> - 4.0.1-2
- Rebuild for python-3.9

* Sun May 17 2020 Antonio Trande <sagitter@fedoraproject.org> - 4.0.1-1
- Release 4.0.1

* Fri May 15 2020 Antonio Trande <sagitter@fedoraproject.org> - 4.0-2
- Remove uglify-js

* Sun May 10 2020 Antonio Trande <sagitter@fedoraproject.org> - 4.0-1
- Release 4.0

* Tue Apr 14 2020 Antonio Trande <sagitter@fedoraproject.org> - 3.0.9-1
- Release 3.0.9

* Thu Apr 02 2020 Antonio Trande <sagitter@fedoraproject.org> - 3.0.8-1
- Release 3.0.8

* Sat Mar 14 2020 Antonio Trande <sagitter@fedoraproject.org> - 3.0.7-1
- Release 3.0.7

* Sun Feb 23 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 3.0.6-3
- Rebuild for x265

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 3.0.6-2
- Rebuild for ffmpeg-4.3 git

* Sat Feb 08 2020 Antonio Trande <sagitter@fedoraproject.org> - 3.0.6-1
- Release 3.0.6

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Antonio Trande <sagitter@fedoraproject.org> - 3.0.5-1
- Release 3.0.5

* Tue Dec 17 2019 Leigh Scott <leigh123linux@gmail.com> - 3.0.3-2
- Mass rebuild for x264

* Thu Dec 12 2019 Antonio Trande <sagitter@fedoraproject.org> - 3.0.3-1
- Release 3.0.3

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 3.0.2-2
- Rebuild for new x265

* Tue Nov 05 2019 Antonio Trande <sagitter@fedoraproject.org> - 3.0.2-1
- Release 3.0.2
- Replace unrecognized compiler option on ARM

* Mon Oct 28 2019 Antonio Trande <sagitter@fedoraproject.org> - 3.0.1-1
- Release 3.0.1

* Wed Oct 02 2019 Antonio Trande <sagitter@fedoraproject.org> - 3.0-1
- Release 3.0

* Sat Aug 24 2019 Leigh Scott <leigh123linux@gmail.com> - 2.5.3-3
- Rebuild for python-3.8

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 2.5.3-2
- Rebuild for new ffmpeg version

* Thu Jul 25 2019 Antonio Trande <sagitter@fedoraproject.org> - 2.5.3-1
- Release to 2.5.3
- Switch to Python3 definitively

* Tue Jul 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.5.2-2
- Rebuilt for x265

* Sat Jun 08 2019 Antonio Trande <sagitter@fedoraproject.org> - 2.5.2-1
- Release to 2.5.2

* Thu Apr 18 2019 Antonio Trande <sagitter@fedoraproject.org> - 2.5.1-1
- Release to 2.5.1

* Wed Mar 20 2019 Antonio Trande <sagitter@fedoraproject.org> - 2.5.0-1
- Release to 2.5.0
- Switch to Python3 on Fedora 29+

* Tue Mar 12 2019 Sérgio Basto <sergio@serjux.com> - 2.4.3-4
- Mass rebuild for x264

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 2.4.3-2
- Rebuild for new x265

* Thu Jan 17 2019 Antonio Trande <sagitter@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3

* Sat Nov 24 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2

* Sun Nov 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-2
- Rebuild for new x265

* Wed Oct 31 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1
- Add Python Cairo library BR

* Mon Oct 15 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.4-1
- Update to 2.4

* Thu Oct 04 2018 Sérgio Basto <sergio@serjux.com> - 2.3.4-2
- Mass rebuild for x264 and/or x265

* Sun Sep 23 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.3.4-1
- Update to 2.3.4

* Sun Aug 19 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.3.2-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2

* Sun Jun 24 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.3.1-2
- Define build conditions for debugging
- Switch back to Python2 (see xpra.org/trac/ticket/1885) (bz#1583319)

* Wed May 30 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1

* Thu May 10 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.3-1
- Update to 2.3
- Switch to Python3
- Drop obsolete patch

* Tue Apr 03 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.2.6-1
- Update to 2.2.6

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.2.5-2
- Rebuilt for new ffmpeg snapshot

* Wed Mar 07 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.2.5-1
- Update to 2.2.5

* Wed Feb 28 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.2.4-4
- Rebuilt for x265

* Fri Feb 23 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.2.4-3
- Use --without-strict option (upstream bug #1772)

* Thu Feb 22 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.2.4-2
- Fix ?_isa macro
- Add gcc BR
- Use python2-Cython BR
- Disable Werror=deprecated-declarations on fedora > 27

* Fri Feb 09 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.2.4-1
- Update to 2.2.4
- Modify patch for ffmpeg-3.5

* Sun Jan 21 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3
- Patched for ffmpeg-3.5

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.2.2-2
- Rebuilt for ffmpeg-3.5 git

* Wed Jan 17 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

-* Sun Dec 31 2017 Sérgio Basto <sergio@serjux.com> - 2.2.1-2
- Mass rebuild for x264 and x265

* Thu Dec 21 2017 Antonio Trande <sagitter@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Tue Dec 12 2017 Antonio Trande <sagitter@fedoraproject.org> - 2.2-1
- Update to 2.2
- Drop old ffmpeg-3.1 patch

* Thu Oct 26 2017 Antonio Trande <sagitter@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Tue Oct 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.1.2-2
- Rebuild for ffmpeg update

* Mon Sep 18 2017 Antonio Trande <sagitter@fedoraproject.org.com> - 2.1.2-1
- Update to 2.1.2

* Sat Aug 19 2017 Antonio Trande <sagitter@fedoraproject.org.com> - 2.1.1-1
- Update to 2.1.1

* Wed Jul 26 2017 Antonio Trande <sagitter@fedoraproject.org.com> - 2.1-1
- Update to 2.1

* Tue Jul 04 2017 Antonio Trande <sagitter@fedoraproject.org.com> - 2.0.3-1
- Update to 2.0.3

* Wed May 10 2017 Antonio Trande <sagitter@fedoraproject.org.com> - 2.0.2-2
- Patched for building against ffmpeg-3.1 (f25)

* Tue May 09 2017 Antonio Trande <sagitter@fedoraproject.org.com> - 2.0.2-1
- Update to 2.0.2
- webp option deprecated
- xvid option deprecated

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-2
- Rebuild for ffmpeg update

* Thu Apr 20 2017 Antonio Trande <sagitter@fedoraproject.org.com> - 1.0.2-1
- Update to 1.0.2
- Include x265 and xvid encoders

* Tue Mar 21 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.17.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

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
