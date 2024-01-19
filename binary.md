## endian-ness

- little endian
    -  small bytes come first
    - `0xa4    0x00    0x02    0x00`
- hex view
    - when converted to a hex number it becomes big endian
    - `0x000200a4`

## check if a bit is set

- `and` with a mask of bits set to 1 that you want to check
- check high bit
    - `0b101 & 0b100`