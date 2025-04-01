# Linux

## desktop shortcut

```sh
#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Name=Screen Locker
Comment=Lock your screen
Exec=/usr/lib/kscreenlocker_greet --immediateLock
Terminal=false
Type=Application
Icon=emblem-locked
Categories=GNOME;System;
StartupNotify=false
```

## Disable `binfmt_misc` program auto runners

- Somehow works through `docker`, maybe via your shell

### Status and Temporary Change

```sh
# enable/disable binfmt_misc for all apps
echo 1 > /proc/sys/fs/binfmt_misc/status
echo 0 > /proc/sys/fs/binfmt_misc/status

# disable binfmt_misc registered program
echo -1 | sudo tee /proc/sys/fs/binfmt_misc/windows
echo -1 | sudo tee /proc/sys/fs/binfmt_misc/windowsPE
```

### Permanent

```sh
# /usr/lib/binfmt.d/wine.conf
# sudo systemctl restart systemd-binfmt.service

# Pre-PE Windows Executables
#:windows:M::MZ::/usr/bin/wine:
```

## raspberry pi

- perf
    - `sudo apt install linux-perf`
- rust install 'triple'
    - `armv7-unknown-linux-gnueabihf`

## direnv

- `XDG_CONFIG_HOME` by default equals `~/.config`

```sh
# ~/.config/direnv/direnv.toml

[whitelist]
exact = [ "~/src/project/.envrc", "/home/user/project-b/subdir-a" ]
```

## Extend Luks Partition

[source](https://unix.stackexchange.com/a/322631)

```sh
# open crypt
crytsetup open /dev/sda2 crypt
# resize partition
parted /dev/sda
    resizepart 2 800GB
#resize crypt
cryptsetup resize /dev/mapper/crypt
# resize physical volume so logical volumes can extend
pvresize /dev/mapper/crypt
# resize home logical volume to 90% of free space
lvresize -l+90%FREE /dev/fedora_localhost-live/home
# force checking of file system, required before fs resize
e2fsck -f /dev/mapper/fedora_localhost--live-home
# extend filesystem to available space
resize2fs /dev/mapper/fedora_localhost--live-home
# resize root logical volume to 100% of free space
lvresize -l+100%FREE /dev/fedora_localhost-live/root
# force checking of file system, required before fs resize
e2fsck -f /dev/mapper/fedora_localhost--live-root
# extend filesystem to available space
resize2fs /dev/mapper/fedora_localhost--live-root
```

## Gaming

### Overview

- **Proton**: Compatibility layer for running Windows games on Linux using Wine + DXVK + vkd3d-proton.
- **DXVK**: Translates Direct3D 9/10/11 → Vulkan.
- **vkd3d-proton**: Translates Direct3D 12 → Vulkan.
- **WineD3D**: Translates all D3D versions (9–12) → OpenGL.
- **Kepler GPUs** (like GTX 780) are too old for full DX12 support in Proton using Vulkan backends.

### Debugging

- opengl
    - `glxgears -info`
    - `glxinfo`
- vulkan
    - `vkcube`
    - `vulkaninfo`
    
### Key Env Vars

| Env Var                      | Purpose                                                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `PROTON_USE_WINED3D=1`       | Force all D3D (including D3D12) → OpenGL via WineD3D (bypasses DXVK and vkd3d)                                     |
| `DXVK_FORCE_D3D11=1`         | Forces a game that supports both D3D12 and D3D11 to use D3D11 with DXVK. Does nothing if game only supports D3D12. |
| `VKD3D_CONFIG=virtual_heaps` | Enables emulated descriptor heaps in vkd3d-proton (for D3D12 → Vulkan, on older drivers)                           |
| `PROTON_USE_DXVK=1`          | Explicitly enables DXVK (usually default)                                                                          |

## Nvidia legacy 470xx driver

### Concepts

- **NVIDIA 470xx driver**: Legacy driver needed for older GPUs like GTX 780.
- **Wayland vs Xorg**: Fedora 41 prefers Wayland, but 470xx only works reliably with Xorg.
- **Secure Boot**: Blocks unsigned kernel modules like NVIDIA’s unless disabled or manually signed.
- **akmod**: Builds kernel modules on demand (via `akmods`).
- **mknod error**: NVIDIA device nodes weren’t being created, blocking GPU access.
- **GDM**: GNOME Display Manager, defaults to Wayland unless configured otherwise.
- **startx**: Manually starts an X session from the command line.
    
### Key Packages Installed

```bash
# Enable RPM Fusion repos
sudo dnf install https://download1.rpmfusion.org/{free,nonfree}/fedora/rpmfusion-{free,nonfree}-release-$(rpm -E %fedora).noarch.rpm

# Install NVIDIA 470xx driver
sudo dnf install akmod-nvidia-470xx xorg-x11-drv-nvidia-470xx-cuda nvidia-modprobe-470xx

# Install Xorg stack and session support
sudo dnf install gnome-session-xsession xorg-x11-server-Xorg xorg-x11-xinit xterm
```

### Start Xorg manually (bypass GDM)

Create an X session launcher:

```bash
echo 'exec gnome-session' > ~/.xinitrc
startx
```

### Diagnostics Used

```bash
# Check if NVIDIA driver loaded
lsmod | grep nvidia
nvidia-smi

# Read logs for crash reasons
journalctl -b -r | grep -iE 'nvidia|xorg|gnome'
```

## Gnome Extensions

- `gnome-tweaks`
    - Additional settings for gnome
- [Hide Top Bar](https://extensions.gnome.org/extension/545/hide-top-bar)
    - hides the top bar when windows are maximized
- [Dash to Dock](https://extensions.gnome.org/extension/307/dash-to-dock)
    - moves dash to bottom of screen for a more windows like experience
    - 24 px
- ~~[TopIcons Plus](https://extensions.gnome.org/extension/1031/topicons/)~~ [AppIndicator](https://extensions.gnome.org/extension/615/appindicator-support/)
    - Adds tray icons for running applications to top bar
