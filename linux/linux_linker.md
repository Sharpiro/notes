## calling a dynamically linked function

- for function `do_something`
- call `do_something@plt` entry in `PLT`
- if `do_something` has not been initialized, get function address from `GOT`
- `jmp` to it

## glossary

- `PLT` - Procedure Linkage Table
    - a `PLT` entry is a bit of code that loads dynamic function address and jumps to it
- `GOT` - Global Offset Table
    - where dynamic function addresses are stored
