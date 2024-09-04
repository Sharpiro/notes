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
