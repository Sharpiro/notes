# Ripping

- [libdvdcss](https://www.videolan.org/developers/libdvdcss.html)
    - open source library from VLC for ripping DVDs
- makemkv
    - the most popular and go to ripping solution

## MakeMKV

### LibreDrive

> [!warning] 
> This is for reference only as every device can be different.

Setup your drive in "Libre" mode to allow it to circumvent firmware restrictions.
This process *allegedly* can flash an encrypted firmware, the end result being the drive no longer has encrypted firmware and can be used unlocked.

- Find a compatible drive that is Libre-capable
- Download [All You Need Firmware Pack (MartyMcNuts)](https://forum.makemkv.com/forum/viewtopic.php?t=22896)
- List drives
    - `sdftool --list`
- Get drive info
    - `sdftool --drive /dev/<drive> --info`
- Dump drive firmware as backup
    - `sdftool --drive <drive> dump auto -o ./firmware_dumps`
- Encrypt modded firmware and flash
    - `sdftool --all-yes --drive <drive> rawflash enc -i modded_firmware.bin`

#### LibreDrive encryption detection

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
