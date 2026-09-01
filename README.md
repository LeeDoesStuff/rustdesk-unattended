<p align="center">
  <img src="res/logo-header.svg" alt="BurgerTop - Your remote desktop"><br>
  <a href="#whats-different-from-rustdesk">What's different</a> •
  <a href="#raw-steps-to-build">Build</a> •
  <a href="#how-to-build-with-docker">Docker</a> •
  <a href="#packaging">Packaging</a> •
  <a href="#file-structure">Structure</a>
</p>

> [!Caution]
> **Misuse Disclaimer:** <br>
> The developers of BurgerTop do not condone or support any unethical or illegal use of this software. Misuse, such as unauthorized access, control, or invasion of privacy, is strictly against our guidelines. The authors are not responsible for any misuse of the application.

Yet another remote desktop solution, written in Rust. Works out of the box with no configuration required. You have full control of your data, with no concerns about security.

BurgerTop is a customized fork of [RustDesk](https://github.com/rustdesk/rustdesk). Upstream contributions and issues that are not BurgerTop-specific belong there. Credit for the underlying protocol, capture pipeline, and UI framework goes to the RustDesk authors.

## What's different from RustDesk

BurgerTop is a rebrand + coexistence fork; the underlying remote-desktop code is upstream RustDesk. The intentional deltas:

- **Identity.** The running app announces itself as **BurgerTop** (`APP_NAME` / `ORG` are overridden in `common::global_init()`, so every downstream config path, IPC socket, log directory, and tmp dir picks up the new name without forking `hbb_common`). User-visible strings in `src/lang/en.rs` that were self-references to RustDesk are now BurgerTop; references to external RustDesk products (the public rendezvous network, RustDesk Server Pro) are left factual.
- **Icon.** New flat burger source at `res/logo.svg`, with regenerated `res/icon.{png,ico}`, size PNGs, macOS icon, Windows Flutter runner `.ico`, and monochrome tray silhouettes for `mac-tray-{light,dark}-x2.png`. `res/logo-header.svg` carries the BurgerTop wordmark.
- **Palette.** `MyTheme` in `flutter/lib/common.dart` uses a Modern-BK-adjacent scheme: deep red `#B4141B` primary, mustard `#F5B316` accent, warm cream `#F5EBDC` surface. The two `Colors.blue` slots in `ColorScheme.primary` that were meant to carry brand color now route through the accent.
- **Packaging identity (Linux).** `res/burgertop.desktop`, `res/burgertop-link.desktop`, `res/burgertop.service`, `res/rpm.spec`, and `res/PKGBUILD` install under `/usr/share/burgertop`, ship a `/usr/bin/burgertop` symlink, and register a `burgertop.service` systemd unit — so the packages coexist with a stock RustDesk install on the same machine.
- **Packaging identity (macOS / Windows / Android).** macOS `PRODUCT_NAME=BurgerTop`, bundle id `com.burgertop.app`, both `burgertop://` and `rustdesk://` schemes registered; the Swift `PRODUCT_MODULE_NAME` stays `RustDesk` so `MainMenu.xib` still links. Windows `Runner.rc` carries BurgerTop company / product / description strings. Android `android:label` is BurgerTop, accessibility service label is `BurgerTop Input`.

What is **not** changed and is unlikely to change without a reason:
- The Cargo crate name (`rustdesk`) and Rust lib name (`librustdesk`). Renaming them touches ~15 files (CMake, Xcode projects, GitHub workflows, C++ / Kotlin entry points) for zero user-visible benefit — the on-disk binary is still `rustdesk`, the visible app is BurgerTop.
- The Kotlin package `com.carriez.flutter_hbb` (renaming moves ~40 files).
- `libs/hbb_common` — kept as an upstream submodule; the runtime `APP_NAME` override sidesteps needing to fork it.
- `build.py`, the MSI package, `libdrmtap` install path, and the alternate rpm specs (Fedora / Flutter / SUSE variants). These still emit the upstream layout — the rebranded Linux packaging above targets the plain `rpm.spec`, `PKGBUILD`, and DEBIAN paths. Cutting a signed installer needs its own pass.

## Dependencies

Desktop versions use Flutter or Sciter (deprecated) for GUI. The steps below cover the Sciter path, which is easier to bring up locally. For the Flutter build, follow the CI workflow in `.github/workflows/flutter-build.yml`.

Please download the Sciter dynamic library yourself:

[Windows](https://raw.githubusercontent.com/c-smile/sciter-sdk/master/bin.win/x64/sciter.dll) |
[Linux](https://raw.githubusercontent.com/c-smile/sciter-sdk/master/bin.lnx/x64/libsciter-gtk.so) |
[macOS](https://raw.githubusercontent.com/c-smile/sciter-sdk/master/bin.osx/libsciter.dylib)

## Raw Steps to Build

- Prepare your Rust development env and C++ build env

- Install [vcpkg](https://github.com/microsoft/vcpkg), and set `VCPKG_ROOT` env variable correctly

  - Windows: `vcpkg install libvpx:x64-windows-static libyuv:x64-windows-static opus:x64-windows-static aom:x64-windows-static`
  - Linux/macOS: `vcpkg install libvpx libyuv opus aom`

- run `cargo run`

## How to Build on Linux

### Ubuntu 18 (Debian 10)

```sh
sudo apt install -y zip g++ gcc git curl wget nasm yasm libgtk-3-dev clang libxcb-randr0-dev libxdo-dev \
        libxfixes-dev libxcb-shape0-dev libxcb-xfixes0-dev libasound2-dev libpulse-dev cmake make \
        libclang-dev ninja-build libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

### openSUSE Tumbleweed

```sh
sudo zypper install gcc-c++ git curl wget nasm yasm gcc gtk3-devel clang libxcb-devel libXfixes-devel cmake alsa-lib-devel gstreamer-devel gstreamer-plugins-base-devel xdotool-devel
```

### Fedora 28 (CentOS 8)

```sh
sudo yum -y install gcc-c++ git curl wget nasm yasm gcc gtk3-devel clang libxcb-devel libxdo-devel libXfixes-devel pulseaudio-libs-devel cmake alsa-lib-devel gstreamer1-devel gstreamer1-plugins-base-devel
```

### Arch (Manjaro)

```sh
sudo pacman -Syu --needed unzip git cmake gcc curl wget yasm nasm zip make pkg-config clang gtk3 xdotool libxcb libxfixes alsa-lib pipewire
```

### Install vcpkg

```sh
git clone https://github.com/microsoft/vcpkg
cd vcpkg
git checkout 2023.04.15
cd ..
vcpkg/bootstrap-vcpkg.sh
export VCPKG_ROOT=$HOME/vcpkg
vcpkg/vcpkg install libvpx libyuv opus aom
```

### Fix libvpx (For Fedora)

```sh
cd vcpkg/buildtrees/libvpx/src
cd *
./configure
sed -i 's/CFLAGS+=-I/CFLAGS+=-fPIC -I/g' Makefile
sed -i 's/CXXFLAGS+=-I/CXXFLAGS+=-fPIC -I/g' Makefile
make
cp libvpx.a $HOME/vcpkg/installed/x64-linux/lib/
cd
```

### Build

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
git clone --recurse-submodules https://github.com/LeeDoesStuff/BurgerTop
cd BurgerTop
mkdir -p target/debug
wget https://raw.githubusercontent.com/c-smile/sciter-sdk/master/bin.lnx/x64/libsciter-gtk.so
mv libsciter-gtk.so target/debug
VCPKG_ROOT=$HOME/vcpkg cargo run
```

## How to Build with Docker

Begin by cloning the repository and building the Docker container:

```sh
git clone https://github.com/LeeDoesStuff/BurgerTop
cd BurgerTop
git submodule update --init --recursive
docker build -t "burgertop-builder" .
```

Then, each time you need to build the application, run:

```sh
docker run --rm -it -v $PWD:/home/user/burgertop -v burgertop-git-cache:/home/user/.cargo/git -v burgertop-registry-cache:/home/user/.cargo/registry -e PUID="$(id -u)" -e PGID="$(id -g)" burgertop-builder
```

The first build may take a while before dependencies are cached; subsequent builds are faster. To pass extra arguments to the build command, append them at the end (for example, `--release` for an optimized build). The resulting executable lives in the `target/` folder on the host and can be run with:

```sh
target/debug/rustdesk
```

Or, for a release build:

```sh
target/release/rustdesk
```

The binary is still named `rustdesk` at the Cargo level to keep the fork diff small; the running app identifies itself as BurgerTop at startup. Run these commands from the root of the BurgerTop repository so the app finds its resources. Other cargo subcommands such as `install` or `run` are not supported via the Docker method — they would install or run the program inside the container instead of on the host.

## Packaging

The Linux packaging templates in `res/` produce a `burgertop` package that installs alongside a stock RustDesk install (different install prefix, service name, and desktop entry).

- **Debian / Ubuntu (`.deb`).** Layout comes from `res/DEBIAN/{preinst,postinst,prerm,postrm}` plus the manifests in `res/`. Installs to `/usr/share/burgertop/`, drops `/usr/bin/burgertop` as a symlink to the shipped binary, and enables `burgertop.service` under systemd. Purge cleans `~/.config/BurgerTop`.
- **RHEL / Fedora (`.rpm`).** See `res/rpm.spec`. Same install layout; `%post` copies the desktop entries into `/usr/share/applications/` and enables the systemd unit.
- **Arch (`PKGBUILD`).** See `res/PKGBUILD`. Same idea via `makepkg`.

The Cargo binary itself is still emitted at `target/release/rustdesk` (crate name unchanged); the packaging step renames or symlinks it to `burgertop` at install time.

The upstream orchestration in `build.py` and the MSI files under `res/msi/` still target the RustDesk layout — cutting a rebranded Windows installer, a signed macOS `.app`, or a Flutter Linux build is a separate pass. The `rpm-flutter.spec`, `rpm-flutter-suse.spec`, and `rpm-suse.spec` variants of the RPM spec are not rebranded yet either; use plain `rpm.spec` for now.

## File Structure

- **libs/hbb_common** — video codec, config, TCP/UDP wrapper, protobuf, filesystem helpers for file transfer, and other shared utilities (upstream submodule, unmodified)
- **libs/scrap** — screen capture
- **libs/enigo** — platform-specific keyboard/mouse control
- **libs/clipboard** — file copy and paste implementation for Windows, Linux, macOS
- **src/ui** — obsolete Sciter UI (deprecated)
- **src/server** — audio, clipboard, input, and video services, plus network connections
- **src/client.rs** — start a peer connection
- **src/rendezvous_mediator.rs** — communicates with a rendezvous/relay server, waits for a direct (TCP hole-punched) or relayed connection
- **src/platform** — platform-specific code
- **src/common.rs** — `global_init()` here writes the `APP_NAME` / `ORG` override that gives BurgerTop its runtime identity
- **flutter** — Flutter code for desktop and mobile
- **flutter/lib/common.dart** — `MyTheme` (the BurgerTop palette lives here)
- **res** — icon source (`logo.svg`), rasterized icons, Linux/macOS/Windows packaging manifests

## License

BurgerTop inherits its license from RustDesk. See [LICENCE](LICENCE).
