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

Not permanent

```sh
# enable/disable binfmt_misc for all apps
echo 1 > /proc/sys/fs/binfmt_misc/status
echo 0 > /proc/sys/fs/binfmt_misc/status

# disable binfmt_misc registered program
echo -1 | sudo tee /proc/sys/fs/binfmt_misc/windows
echo -1 | sudo tee /proc/sys/fs/binfmt_misc/windowsPE
```

Permanent

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
