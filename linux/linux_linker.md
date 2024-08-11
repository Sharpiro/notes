## calling a dynamically linked function

- for function `do_something`
- call `do_something@plt` entry in `PLT`
- if `do_something` has not been initialized, get function address from `GOT`
- `jmp` to it

## Syscalls

- `mmap2`
    - Sometimes the address you request will not be granted, using `MAP_FIXED` can make it more likely to be granted
        - Only seen in qemu

## Misc

- Large arrays on heap
    - A large global array can be partially allocated on the heap by the OS before start, despite all sources saying this doesn't happen
- `malloc` creates heap
    - `malloc` creates heap segment even if one already exists from something like a large global array

## glossary

- `PLT` - Procedure Linkage Table
    - a `PLT` entry is a bit of code that loads dynamic function address and jumps to it
- `GOT` - Global Offset Table
    - where dynamic function addresses are stored
