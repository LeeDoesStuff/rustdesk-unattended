<p align="center">
  <img src="res/logo-header.svg" alt="BurgerTop - Your remote desktop"><br>
  <a href="#raw-steps-to-build">Build</a> •
  <a href="#how-to-build-with-docker">Docker</a> •
  <a href="#file-structure">Structure</a>
</p>

> [!Caution]
> **Misuse Disclaimer:** <br>
> The developers of BurgerTop do not condone or support any unethical or illegal use of this software. Misuse, such as unauthorized access, control, or invasion of privacy, is strictly against our guidelines. The authors are not responsible for any misuse of the application.

Yet another remote desktop solution, written in Rust. Works out of the box with no configuration required. You have full control of your data, with no concerns about security.

BurgerTop is a customized fork of [RustDesk](https://github.com/rustdesk/rustdesk). Upstream contributions and issues that are not BurgerTop-specific belong there. Credit for the underlying protocol, capture pipeline, and UI framework goes to the RustDesk authors.

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

## File Structure

- **libs/hbb_common** — video codec, config, TCP/UDP wrapper, protobuf, filesystem helpers for file transfer, and other shared utilities (upstream submodule)
- **libs/scrap** — screen capture
- **libs/enigo** — platform-specific keyboard/mouse control
- **libs/clipboard** — file copy and paste implementation for Windows, Linux, macOS
- **src/ui** — obsolete Sciter UI (deprecated)
- **src/server** — audio, clipboard, input, and video services, plus network connections
- **src/client.rs** — start a peer connection
- **src/rendezvous_mediator.rs** — communicates with a rendezvous/relay server, waits for a direct (TCP hole-punched) or relayed connection
- **src/platform** — platform-specific code
- **flutter** — Flutter code for desktop and mobile

## License

BurgerTop inherits its license from RustDesk. See [LICENCE](LICENCE).
