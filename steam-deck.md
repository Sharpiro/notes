## shortcuts

- [[linux#desktop shortcut]]

### lock screen shortcut

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

### script shortcut

```sh
[Desktop Entry]
Exec=/home/deck/scripts/sync.sh
Icon=steamdeck-gaming-return
Name=Sync
Path=/home/deck/Desktop
Terminal=true
Type=Application
```

## firefox won't save
  
```sh
systemctl restart --user xdg-desktop-portal
```

## sync files

- [[bash#if statement|bash if statement]]

```sh
#! /bin/bash

pwd
echo syncing...
echo downloading huge files, this could take a while...
scp pi@192.168.1.222:/home/pi/roms/gba/* /run/media/mmcblk0p1/Emulation/roms/gba
if [[ $? == 0 ]]; then
  echo -----SUCCESS-----
  sha1sum /run/media/mmcblk0p1/Emulation/roms/gba/*
else
  echo -----FAILURE-----
fi
sleep 10
```
