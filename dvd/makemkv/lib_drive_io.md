# LibDriveIO

## Building

- `CFLAGS="-g -O0" ./configure --enable-debug`
- `make clean && make out/libdriveio.so.0 && cp out/libdriveio.so.0 ~/temp/drive_info`

## SDF Tool

- `sdftool --list`
    - `makemkvcon` acquires drive info from OS locations like `/sys/bus/scsi/devices`
    - `makemkvcon` calls `libdriveio::DriveIoGetDriveId` to get more detail
    - `libdriveio` calls callback back into `makemkvcon` to actually communicate with drive

## Glossary

- Command Descriptor Block (CDB)
    - defines the command the drive should execute

## Tools

- `sg3_utils` [fedora](https://packages.fedoraproject.org/pkgs/sg3_utils/sg3_utils/) [mirror](https://github.com/hreinecke/sg3_utils)
    - `sg_inq -v /dev/sr0`
    - `sg_get_config -v /dev/sr0`
