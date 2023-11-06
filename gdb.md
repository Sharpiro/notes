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