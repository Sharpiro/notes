## install from source

```sh
sudo apt install python3-dev
./configure --with-python
make
sudo make install
```

## config

```sh
set auto-load safe-path / # allow local .gdbinit files
set disassembly-flavor intel
```
## break at address

```sh
break *0xaddress
```

## watch address as string

```sh
x/1bs 0xdeadbeef
```

## list memory map

```sh
info proc mappings # i proc m
```

## gdb dashboard memory watch expression

```sh
dash m w $rsp+8 64 # whitespace is significant in an expression
dash m w *(long*)($rsp+8) 64
```

## gdb show actual `fs` register value

- gdb lies and doesn't show `fs` value by default
- value found in `fs_base` pseudo-register

```sh
set radix 16
dash expressions watch $fs_base
```
