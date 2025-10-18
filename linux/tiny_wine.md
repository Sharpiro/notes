# Tiny Wine

## Linux Notes

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
- intermittent `malloc` memory bugs
    - In the loader I'm using `mmap` for `malloc`
    - In `tinyc`  I'm using `brk` for `malloc`
    - Because `brk` returns a random address and my loader `mmap` uses a static address, `mmap` will overwrite the `brk` less than 1% of the time, causing `tinyc` `malloc` to fail later on
- Alignment
    - pre-main
        - 16 byte aligned at start
        - NOT 16 byte aligned at `call`
    - post-main
        - NOT 16 byte aligned at start
        - 16 byte aligned at `call`
- relocation types
    - function
        - supported
            - R_X86_64_JUMP_SLOT
    - variable
        - supported
            - R_X86_64_COPY
            - R_X86_64_GLOB_DAT
        - unsupported
            - R_X86_64_RELATIVE
                - file pointer to static var in file
            - R_X86_64_64
                - file pointer to non-static var in file
- Static vs Dynamic binaries
    - `-nostdlib -static`
        - `elf: Type: 2 - EXEC`
        - `ldd: not a dynamic executable`
    - `-nostdlib`
        - `elf: Type: 3 - DYN - PIE`
        - `ldd: statically linked`

## Windows Notes

- `ntdll.dll` seems to be an implicit dependency for all windows programs
    - wine builds both a `ntdll.so` and `ntdll.dll`
    - almost everything else seems to be built as a `dll`
- Unlike Linux dynamic linking which uses the stack and/or registers to prepare for the linking function, windows just jumps to a function.  The only way I see how to get the linking information to the function is to create glue-code assembly dynamically for each function.
    - The reason for this awkwardness is because Windows by default handles the linking on program start, whereas linux defaults to linking on first function call
- When calling from Windows to Linux, after dynamic linking a function once, subsequent calls still need glue-code to swap the calling convention
    - It's simpler to just re-link the function every time since we would have to duplicate much of the original linking work.
- Multiple types of dynamic linking need to be supported
    - Windows -> Windows (msvcrt.dll)
    - Windows -> Linux (ntdll.dll)
        - Linux -> Windows (returning to Windows)
    - Linux -> Linux (libntdll.so)
- trampoline compiler-specific bug
    - originally i was using the compiler to generate trampoline assembly for ease of use
    - I had to convert this to creating the byte code manually b/c different compilers/versions were generating different assembly of different sizes
- `.bss` and `.data` initialization
    - the entire `.bss` section can be set to `0`
    - the `.data` section is just mapped into memory w/ no modification
        - this explains why the PE format doesn't understand how large imported/exported variables are
- possible clang linker target options
    - `x86_64-w64-mingw32`
    - `i686-w64-mingw32`
    - `x86_64-w64-windows-gnu`
- Thread-local storage
    - Would be super easy if we could override `__tmainCRTStartup` function with our own, but for some reason, the linker duplicates our implementation rather than replacing it like it does with many of the other functions called in the runtime startup.
    - We need to 'initialize' thread-local storage.  But we don't actually want to support it, we just want to set it up enough so that the program doesn't crash before we reach our `main` function.  Because we're skipping some initialization code, undoubtedly some things will not work, but we just want some basic functionality.
    - We need to initialize the `gs` segment register to some address to avoid segfaults.  Right now i'm just going to give it the top of the winloader's stack.
    - Windows C standard library used an `initialized` variable to check if certain things have been initialized.  If we set it to `true` from the start we can skip some of the initialization code.
        - `intialized` is checked in `__main`, so if we override that function in our own runtime, we can bypass checking `initialized` directly
        - After implementing more MS functions in `msvrt.dll` like `_onexit`, stdlib's `__main` will return without error
    - Also uses `.refptr.__imp__acmdln` which we an setup to bypass a good chunk of TLS initialization.
        - only needed in docker version likely due to older Clang version
        - can override `__p__acmdln` function instead
        - I was originally exporting `_acmdln` as a function, but if it is instead exported as `EXPORTABLE char *_acmdln = NULL`, `__p__acmdln` can also be removed
- Structs vs variables with inline assembly
    - When using "=m" in assmebly to output to C variables, only outputing to variables in the function worked, trying to output to fields of a struct variable in the function failed due to registers clobbering
- Stack is 16 byte aligned **before** a function call due to pushed return address
    - At function call `stack_pointer % 16 == 0`
    - At first function instruction `stack_pointer % 16 == 8`
- Alignment
    - pre-main
        - NOT 16 byte aligned at start
        - NOT 16 byte aligned at `call`
    - post-main
        - NOT 16 byte aligned at start
        - 16 byte aligned at `call`
- `stdlib` setup
    - `mainCRTStartup` (static)
    - `__tmainCRTStartup` (static)
    - `_initterm` (dynamic)
    - `pre_cpp_init` (static)
    - `__getmainargs` (dynamic)
- 2025-08-24 Stack bug
    - During the swap stack from Windows to Linux I was removing stack data for parameters 5 and 6.
    - The problem is that only works if the function call has that many parameters, otherwise it's just overwriting used data on the stack.
    - I didn't notice this b/c I had a 'proxy' function being called prior to the swap, which means it was likely overwriting space on the stack that wasn't being used again.

| Address | Value | Description |
| ------- | ----- | ----------- |
| 0x00    | 0x00  | Shadow      |
| 0x04    | 0x00  | Shadow      |
| 0x08    | 0x00  | Shadow      |
| 0x0c    | 0x00  | Shadow      |
| 0x10    | 0x00  | Stack Data  |

| Address | Value | Description |
| ------- | ----- | ----------- |
| 0x00    | 0x00  | Shadow      |
| 0x04    | 0x00  | Shadow      |
| 0x08    | 0x00  | Shadow      |
| 0x0c    | 0x00  | Shadow      |
| 0x10    | 0x00  | Parameter 5 |
| 0x14    | 0x00  | Parameter 6 |
| 0x18    | 0x00  | Parameter 7 |
| 0x1c    | 0x00  | Parameter 8 |
| 0x20    | 0x00  | Parameter 9 |
| 0x24    | 0x00  | Stack Data  |

| Address | Value | Description |
| ------- | ----- | ----------- |
| 0x00    | 0x00  | Parameter 7 |
| 0x04    | 0x00  | Parameter 8 |
| 0x08    | 0x00  | Parameter 9 |
| 0x24    | 0x00  | Stack Data  |
- 2025-09-01 `fopen` bug
    - I couldn't figure out why in the middle of my buffer I had random bytes disspearing
    - `fopen` with mode `r` on Linux is identical to `rb`
    - `fopen` with mode `r` is text mode on Windows which translated `\r\n` into `\n`
