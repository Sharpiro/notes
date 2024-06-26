# Linux Programming

## user_dispatch

- [kernel org](https://www.kernel.org/doc/Documentation/admin-guide/syscall-user-dispatch.rst)
- [elixir.bootlin.com tests](https://elixir.bootlin.com/linux/latest/source/tools/testing/selftests/syscall_user_dispatch/sud_benchmark.c)

```c
#include <sys/prctl.h>
prctl(PR_SET_SYSCALL_USER_DISPATCH, <op>, <offset>, <length>, [selector])
```

## Signals

- `sigaction` struct
    - `sa_handler` is the simple handler for a signal
    - `sa_sigaction` is the more detailed handler
        - requires: `.sa_flags = SA_SIGINFO`

## Apis

- `dl_iterate_phdr` - "dynamic linker iterate program headers"
    - parse ELF headers of shared objects loaded into the program
- `open` #fnctl - syscall to open file low-level descriptor
- `fopen` #stdio - high-level file operations

## Elf Format

- [[2023-11-30_A Whirlwind Tutorial on Creating Really Teensy ELF Executables for Linux.pdf|A Whirlwind Tutorial on Creating Really Teensy ELF Executables for Linux]]
