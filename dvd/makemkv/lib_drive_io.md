# LibDriveIO

## Building

- `CFLAGS="-g -O0" ./configure --enable-debug`
- `make clean && make out/libdriveio.so.0 && cp out/libdriveio.so.0 ~/temp/drive_info`

## SDF Tool

- `sdftool --list`
    - `makemkvcon` acquires drive info from OS locations like `/sys/bus/scsi/devices`
    - `makemkvcon` calls `libdriveio::DriveIoGetDriveId` to get more detail
    - `libdriveio` calls callback back into `makemkvcon` to actually communicate with drive
- `sdftool --drive <drive> --info`
    - `makemkvcon` acquires drive info **NOT** using `libdriveio`
    - `sha1` hashes first 24 bytes of drive descriptor for lookup in `sdf.bin`
        - e.g. `HL-DT-STDVDRAM GP55EX70 ` -> `f77293ce4d7dca116d20b307f71229453afb12eb`
    - Checks `sdf.bin` to see if drive is supported
    - @todo

## SDF.bin

- Binary blob containing information about how to translate a requested action (like reading a disc structure), called an `Entrypoint` into a set of firmware-specific SCSI commands
- Contains SDF blobs for each firmware
- Contains a master SDF blob that exports an API (another `Entrypoint`) to uniquely fingerprint a drive firmware version (`Firmware Hash`), which is used by the library to select the SDF blob for the specific firmware
- Hashed
    - Any modification will cause `makemkvcon` to return an error
- Encrypted
    - Portions of the file may be encrypted, possibly with a 0'd out key
- Compressed
    - Portions of the file may be compressed

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
- `lsscsi`
    - list SCSI devices (or hosts), list NVMe devices
    - `lsscsi --generic`
