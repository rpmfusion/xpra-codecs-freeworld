%bcond_without enc_x264
%bcond_without enc_x265
# Theses settings requires 64bit
%if 0%{?__isa_bits} == 64
%bcond_without dec_avcodec2
%bcond_without csc_swscale
%else
%bcond_with dec_avcodec2
%bcond_with csc_swscale
%endif

# For debugging only
%bcond_with debug
%if %{with debug}
%global _with_debug --with-debug
%endif
#

# These are necessary as the _with_foo is *not* defined if the
# --with flag isn't specifed, and we need to have the --without
# specified option in that case.
%if %{without enc_x264}
%global _with_enc_x264 --without-enc_x264
%endif

%if %{with enc_x265}
%global _with_enc_x265 --with-enc_x265
%endif

%if %{without dec_avcodec2}
%global _with_dec_avcodec2 --without-dec_avcodec2
%endif

%if %{without csc_swscale}
%global _with_csc_swscale --without-csc_swscale
%endif

Name:           xpra-codecs-freeworld
Version:        4.4.5
Release:        %autorelease
Summary:        Additional codecs for xpra using x264 and ffmpeg
License:        GPLv2+
URL:            https://www.xpra.org/
Source0:        https://github.com/Xpra-org/xpra/archive/refs/tags/v%{version}/xpra-%{version}.tar.gz
Patch1:         ignore_assert_pandoc.patch

BuildRequires:  python3-devel
BuildRequires:  gtk3-devel
BuildRequires:  libXtst-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  lz4-devel
BuildRequires:  python3-Cython
BuildRequires:  ack
BuildRequires:  desktop-file-utils
BuildRequires:  libvpx-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXres-devel
BuildRequires:  cups-devel, cups
BuildRequires:  redhat-rpm-config
BuildRequires:  python3-rpm-macros
BuildRequires:  gcc
BuildRequires:  pam-devel
BuildRequires:  pandoc
# needs by setup.py to detect systemd `sd_listen_ENABLED = POSIX and pkg_config_ok("--exists", "libsystemd")`
BuildRequires:  systemd-devel
%if 0%{?fedora}
BuildRequires:  pkgconfig(libprocps)
%endif
BuildRequires:  pkgconfig(libavif)
BuildRequires:  pkgconfig(libqrencode)
BuildRequires:  libdrm-devel
BuildRequires:  pkgconfig(libwebp)
%if 0%{?el8}
#BuildRequires:  xorg-x11-server-Xvfb
#BuildRequires:  cairo-devel
BuildRequires:  pygobject3-devel
%else
BuildRequires:  python3-gobject-devel
%endif
BuildRequires:  libappstream-glib
BuildRequires:  python3-cairo-devel
BuildRequires:  xorg-x11-server-Xorg
BuildRequires:  xorg-x11-drv-dummy
BuildRequires:  xorg-x11-xauth
BuildRequires:  xkbcomp
BuildRequires:  setxkbmap
%if %{with debug}
BuildRequires: libasan
%endif

%if %{with enc_x264}
BuildRequires:  x264-devel
%endif
# While ffmpeg-devel should only be needed in theses conditions, setup.py requires it anyway
#if %%{with dec_avcodec2} || %%{with csc_swscale}
BuildRequires:  ffmpeg-devel
#endif

#BuildRequires:  pygtk2-devel
BuildRequires:  xvidcore-devel
%if %{with enc_x265}
BuildRequires:  x265-devel
%endif

Requires:       xpra%{?_isa} = %{version}
Requires:       gstreamer1-plugins-ugly%{?_isa}

%description
Provides support for H.264 encoding and swscale support in xpra using
x264 and ffmpeg.

%prep
%autosetup -p1 -n xpra-%{version}

# cc1: error: unrecognized compiler option ‘-mfpmath=387’
%ifarch %{arm}
sed -i 's|-mfpmath=387|-mfloat-abi=hard|' setup.py
%endif

%build
%set_build_flags
%{__python3} setup.py build --executable="%{__python3} -s" \
    --with-verbose \
    --with-vpx \
    %{?_with_enc_x264} \
    %{?_with_enc_x265} \
    %{?_with_dec_avcodec2} \
    %{?_with_csc_swscale} \
    %{?_with_debug} \
    --with-Xdummy \
    --with-Xdummy_wrapper \
    --without-strict \
    --with-enc_ffmpeg \
    --without-tests \
    --without-docs

%install
# We are interested to additional codecs only
# so we install it in a custom dir
%py3_install -- --root destdir
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
%if %{with dec_avcodec2} || %{with csc_swscale}
 libav_common \
%endif
 enc_ffmpeg enc_x265 %{buildroot}%{python3_sitearch}/xpra/codecs/
popd

#fix shebangs from python3_sitearch
for i in `ack -rl '^#!/.*python' %{buildroot}%{python3_sitearch}/xpra`; do
    %py3_shebang_fix $i
    chmod 0755 $i
done

#fix permissions on shared objects
find %{buildroot}%{python3_sitearch}/xpra -name '*.so' \
    -exec chmod 0755 {} \;

%files
%dir %{python3_sitearch}/xpra
%dir %{python3_sitearch}/xpra/codecs
%{python3_sitearch}/xpra/codecs/*
%doc README.md
%license COPYING

%changelog
%autochangelog
