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
- Sense Data
    - Data or error messages that may exist when a command fails
- SG - SCSI Generic driver

## Tools

- `sg3_utils` [fedora](https://packages.fedoraproject.org/pkgs/sg3_utils/sg3_utils/) [mirror](https://github.com/hreinecke/sg3_utils)
    - send scsi commands 
    - `sg_inq -v /dev/sr0`
    - `sg_get_config -v /dev/sr0`
    - `sg_raw -Rv -r 1k /dev/sr0 12 00 00 00 60 00`
