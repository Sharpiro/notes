## install from source

```sh
sudo apt install python3-dev
./configure --with-python
make
sudo make install
```

- additional raspbian steps
    - install `libgmp-dev`
    - install `libmpfr-dev`
    - ensure `/usr/bin/python -> /usr/bin/python3`

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

- show as register in gdb dashboard

```py
# fetch_register_list:2108
return names + ["fs_base", "gs_base", "orig_rax"]
```
## signals

- `handle all ignore`
    - prevents all signals from being sent to inferior
- `handle all nostop noprint pass`
    - don't stop, don't print, pass to inferior

## run command when breakpoint hit

```sh
define hook-stop
    if $pc == (void(*)())run_asm
        b *0x427e52
        continue
    end
end
```

## dynamically add symbol file

```sh
# add-symbol file <program> <.text start>
add-symbol-file ./test_program_c_linux/test.exe 0x401000
```

## register watchpoint

- break whenever register changes

```sh
watch $sp
```