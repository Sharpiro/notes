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
- Specifying a `sdf.bin` path via `--sdf-file` skips archive reading from program home folder
- Process for `sdf_00000098.bin`
    - Find drive via `scsi` calls
    - Hash 24 byte drive descriptor
    - Read `sdf.bin`
    - Hash `sdf[:-0x230]` hash
        - Unknown where validation hash is stored
    - `base_key1 = [0] * 16`
    - Decrypt initial 4176 byte `chunk1`
        - get firmware platform string `platform = 'mtk:19:'`
    - Try to find `base_key2` by hashing smaller portions of:
        - `auto = sha1("auto")[:15]`
        - `base_key2 = sha1([\x00|\x01]<auto><platform><device_info[:x]>)`
            - in my case starts with `\x01`
        - Unclear why it does so many, but it ends up using `x = 22` which is only the `platform`
    - Unknown how `chunk2_key_enc` is located
    - Decrypt `chunk2_key` with `base_key2`
    - Decrypt `chunk2` key `chunk2_key`
    - In order to decompress some chunks, prior chunk buffers are required as input

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
