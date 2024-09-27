## General

- Shared libraries have their own relocations and global offset tables as well
- Only exported functions will have relocations
## Syscalls

- `mmap2`
    - Sometimes the address you request will not be granted, using `MAP_FIXED` can make it more likely to be granted
        - Only seen in qemu

## Sections

- `.data`
    - initialized data
- `.bss`
    - uninitialized data
    - initialized at app start by OS or loader
    - takes less file space than `.data` section
- `.dynsm` - dynamic symbols
- `.dynstr` - dynamic string table
    - names for dynamic symbols
- `.strtab` - string table
    - names for functions, variables, etc.
- `.shstrtab` - section header string table
    - names for section headers

## Dynamic Loading

- recursively map shared libraries into memory
- compute runtime locations using memory region offset for:
    - symbols
    - relocations
    - global offset table
- set `.got` to call back into dynamic loader
- set `.got` non-zero values with their memory region offset
### Dynamic Variable Loading

- loader
    - for each variable relocation:
        - resolve respective symbol
        - update `.got` with symbol value

### Dynamic Function Loading

#### Calling `printf`

- 1st call
    - call `printf@plt`
    - load `printf@got` address into `r12` from `.got`
    - get `printf` address from `.got` (`.plt`)
    - jump to `.plt`
    - setup registers and stack
    - jump to dynamic loader
    - find `printf` address
    - store `printf` address in the called `.got` entry
    - setup registers and stack
    - jump to `printf`
- 2nd call
    - call `printf@plt`
    - get `printf` address from `.got` (`printf`)
    - jump to `printf`

## Misc

- Large arrays in `.bss`
    - A large global array can be partially allocated on the heap by the OS before start, despite all sources saying this doesn't happen
- `malloc` creates heap
    - `malloc` creates heap segment even if one already exists from something like a large global array

## glossary

- `PLT` - Procedure Linkage Table
    - a `PLT` entry is a bit of code that loads dynamic function address and jumps to it
- `GOT` - Global Offset Table
    - where dynamic function addresses are stored

