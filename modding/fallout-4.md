## Enable Modding Manually

- add to `%USERPROFILE%\Documents\My Games\Fallout4\Fallout4Prefs.ini`

```ini
[Launcher]
bEnableFileSelection=1
```

- add to `%USERPROFILE%\Documents\My Games\Fallout4/Fallout4Custom.ini`

```ini
[Archive]
bInvalidateOlderFiles=1
sResourceDataDirsFinal=
```

- move `.esp` mods to `%GAME_INSTALL_DIR%\Fallout 4\Data`
- add mod names to `%LOCALAPPDATA%\Fallout4\plugins.txt`
    - asterisks are now a required prefix for mods in text file

```txt
Fallout4.esm
*EasyLockpicking.esp
*my_test_mod.esp
```

