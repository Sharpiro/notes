# LibreDrive

> [!warning] 
> This is for reference only as every device can be different.
> 
> Tested on MakeMKV v1.17.7 / SDFtool Flasher v1.3.5

## Linux Flashing

Setup your drive in "Libre" mode to allow it to circumvent firmware restrictions.

I'm still not sure, but as far as I know, after flashing the modded firmware in encrypted form, the drive *may* no longer have encrypted firmware installed, and can then be flashed with any firmware.

- Find a compatible drive that is Libre-capable
- Download [All You Need Firmware Pack (MartyMcNuts)](https://forum.makemkv.com/forum/viewtopic.php?t=22896)
- List drives
    - `sdftool --list`
- Get drive info
    - `sdftool --drive <drive> --info`
- Dump drive firmware as backup
    - `sdftool --drive <drive> dump auto -o ./firmware_dumps`
- Encrypt modded firmware and flash
    - `sdftool --all-yes --drive <drive> rawflash enc -i modded_firmware.bin`

## Encryption detection

```python
def is_encrypted(drive_listing: str, drive_info: str) -> bool:
    fw = int(drive_listing.split("_")[3][:4])
    modded = drive_info.split(":")[-2][1:2]
    if fw >= 2120 and modded != "M":
        return True

    return False

assert is_encrypted(
    "ASUS_BW-16D1HT_3.11_212012011759_00000000000",
    "mtk:19:59:JB8 :ASUS    :BW-16D1HT       3.11:W000600:-",
)
assert not is_encrypted(
    "ASUS_BW-16D1HT_3.10_211901041014_00000000000",
    "mtk:19:59:JB8 :ASUS    :BW-16D1HT       3.10:WM01601:-",
)
```
