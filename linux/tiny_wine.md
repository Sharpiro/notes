# Tiny Wine

## Notes

- Discovered an interesting `gdb` `arm32` instruction display bug that threw me for a loop and lead me down all sorts of bad paths regarding how instructions are parsed
    - [[gdb#Arm32 display bug|Arm32 display bug]]
- Found an issue in `qemu` where additional flags were required to get `mmap` working
- Found a bug in `qemu` where `brk` syscall was failing to extend the program break
    - `e282010b2e`
        - adds support for `info proc mappings`
        - `brk` works
    - `brk` breaks somewhere in v8-v8.1
- `binfmt` works THROUGH docker!
- When using [[gdb#Breakpoint in Source|Breakpoint in Source]] it only allows you to step past if a breakpoint has been set previously
    - infinite loops though unless you setup custom handling
- [[gdb#Hook-Stop|hook-stop]] doesn't work at all in gdb 15.1 arm32
- [[gdb#Breakpoint Commands|Breakpoint Commands]] crashes when you try to `continue` in gdb 15.1 in arm32
- PIE - Position Independent Executable
    - statically linked are by default not PIE
    - dynamically linked are by default PIE
    - can specify options to force PIE/no-PIE
- PIC - Position Independent Code
    - `clang 17 x64` requires `-fPIC` to create a statically linked shared object
- `$fp` is incorrectly showing `$sp` in gdb after jumping to inferior
- custom `malloc` functions must handle address alignment or you will receive `bus error`
- `qemu` was loading the loader's `rw` memory at the same point where I was mapping shared libraries, causing bus errors and segmentation faults due to memory corruption
    - Using hard-coded `0x500000` for now
    - Would be nice to detect what is in use prior
- invalid arm relocation type `R_ARM_REL32` in shared object
    - When creating an arm32 static shared object that contains a function that references a `.data` variable, it by default created a variable relocation of type `R_ARM_REL32`, which is a static relocation that is not even allowed in shared objects and fails on startup.
    - Adding `-fPIC` option changed the relocation type to the usual `R_ARM_GLOB_DAT`.
    - I thought shared libraries were already position-independent code, so what did `-fPIC` actually do?
- `.got` vs `.got.plt`
    - `arm32` has a `.got` section for global offset table, used by variables and functions
    - `amd64` uses `.got` for variables, but `.got.plt` for functions
