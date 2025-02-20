## install from source

### Prerequisites

- `python3-dev`
- `texinfo bison`
    - required due to a bug when using git sources (non-tarball)

```sh
git clone --depth 1 --branch gdb-15-branch https://github.com/bminor/binutils-gdb.git
mkdir binutils-gdb/build
cd binutils-gdb.git/build
./configure \
    --prefix=/opt/gdb-15.x \
    --with-python \
    --enable-targets=x86_64-linux-gnu,arm-linux-gnueabihf \
    --target="arm-linux-gnueabihf" \
    --build="arm-linux-gnueabihf" \
    --host="arm-linux-gnueabihf"
time make -j6
sudo make install
```

- `--enable-targets`
    - enables cross debugging like in `gdb-multiarch`
    - still requires a gdb server for alternative architectures
- additional Raspbian/RPiOS steps
    - install `libgmp-dev`
    - install `libmpfr-dev`
    - ensure `/usr/bin/python -> /usr/bin/python3`
    - On the latest Raspberry Pi OS 32 bit, gdb incorrectly detects 64 bit, so we need to force 32 in the configure script
        - `--target="arm-unknown-linux-gnu" --build="arm-unknown-linux-gnu" --host="arm-unknown-linux-gnu"`

## config

```sh
set auto-load safe-path / # allow local .gdbinit files
set disassembly-flavor intel
```
## break at address

```sh
break *0xaddress
```

- gdb can become unstable if you set breakpoints on memory that is re-mapped
    - e.g. `b _start` and then that symbol is unloaded
## view address as string

```sh
x/1s 0xdeadbeef
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

## Run command when breakpoint hit

### Hook-Stop

- runs commands on every breakpoint

```sh
define hook-stop
    if $pc == (void(*)())run_asm
        b *0x427e52
        continue
    end
end
```

### Breakpoint Commands

- runs commands on specific breakpoint

```sh
b *run_asm+88
commands
b main
add-symbol-file ./tinyfetch
add-symbol-file ./libtinyc.so 0x5056b0 # address of .text start
end
```

## dynamically add symbol file

```sh
# add-symbol file <program> <.text start>
add-symbol-file ./test_program_c_linux/test.exe 0x401000
```

## register and memory watchpoint (hardware breakpoint)

- break whenever register or memory changes
- breaks **after** the change, and shows value before and after

```sh
watch $sp
watch *0xdeadbeef
```

## Tracing

- `strace` - trace syscall
    - Make `read` show buffer pointer instead of data
        - `strace -e raw=read`
- `ltrace`: trace library/function calls
    - can pass a config file with `-F` to modify function declarations
    - E.g. make `read` show buffer pointer instead of data
        - `int read(int, void *, ulong);`
- Disable `ASLR`
    - easier to trace when addresses aren't changing
    - `setarch $(uname -m) -R ltrace ...`

## Better array printing

```sh
# p/x *arr@5
set print array-indexes off
```

## Shared Lib of Symbol

```sh
info symbol $pc
info line *$pc
```

## Arm32 display bug

```asm
.global _start

_start:
    // gdb sees: tst	r10, #204, 22	@ 0x33000
    mov r3, #0xabcc
    // uncomment this to fix
    // movw r3, #0xabcc
```

## Builtin functions

```sh
`$_strlen(str)` # get length of string
```

## Breakpoint in Source

```c
# arm32, usually infinite loops in gdb
__asm__("bkpt #0");

# generic, crashes program
__builtin_trap();
```

## Break on Syscalls

```sh
# breaks right before mmap2 is executed
catch syscall mmap2
```
