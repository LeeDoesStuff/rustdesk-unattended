Name:       burgertop
Version:    1.4.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://github.com/LeeDoesStuff/BurgerTop
Vendor:     BurgerTop <clam@clamshampc.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva2 gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
BurgerTop remote desktop (a customized fork of RustDesk).

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/burgertop/
mkdir -p %{buildroot}/usr/share/burgertop/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/rustdesk %{buildroot}/usr/bin/burgertop
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/burgertop/libsciter-gtk.so
install $HBB/res/burgertop.service %{buildroot}/usr/share/burgertop/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/burgertop.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/burgertop.svg
install $HBB/res/burgertop.desktop %{buildroot}/usr/share/burgertop/files/
install $HBB/res/burgertop-link.desktop %{buildroot}/usr/share/burgertop/files/

%files
/usr/bin/burgertop
/usr/share/burgertop/libsciter-gtk.so
/usr/share/burgertop/files/burgertop.service
/usr/share/icons/hicolor/256x256/apps/burgertop.png
/usr/share/icons/hicolor/scalable/apps/burgertop.svg
/usr/share/burgertop/files/burgertop.desktop
/usr/share/burgertop/files/burgertop-link.desktop
/usr/share/burgertop/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop burgertop || true
  ;;
esac

%post
cp /usr/share/burgertop/files/burgertop.service /etc/systemd/system/burgertop.service
cp /usr/share/burgertop/files/burgertop.desktop /usr/share/applications/
cp /usr/share/burgertop/files/burgertop-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable burgertop
systemctl start burgertop
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop burgertop || true
    systemctl disable burgertop || true
    rm /etc/systemd/system/burgertop.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/burgertop.desktop || true
    rm /usr/share/applications/burgertop-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
