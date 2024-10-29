## Addresses

| Address | Description  |
| ------- | ------------ |
| 0x0100  | header start |
| 0x0150  | entry point  |
| 0x9000  | tiles        |

## Assembling

```sh
rm -f *.o *.gb
rgbasm main.asm -o main.o -Wall
rgblink -o main.gb --map output.map main.o
rgbfix -v -p 0xff main.gb
```


## References

- [Assembler](https://rgbds.gbdev.io/install/linux)
- [Compiler](https://github.com/gbdk-2020/gbdk-2020)
- [Disassembler](https://github.com/mattcurrie/mgbdis)
