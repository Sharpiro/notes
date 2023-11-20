
## user_dispatch

- [kernel org](https://www.kernel.org/doc/Documentation/admin-guide/syscall-user-dispatch.rst)
- [elixir.bootlin.com tests](https://elixir.bootlin.com/linux/latest/source/tools/testing/selftests/syscall_user_dispatch/sud_benchmark.c)

```c
#include <sys/prctl.h>
prctl(PR_SET_SYSCALL_USER_DISPATCH, <op>, <offset>, <length>, [selector])
```

## signals

- `sigaction` struct
    - `sa_handler` is the simple handler for a signal
    - `sa_sigaction` is the more detailed handler
        - requires: `.sa_flags = SA_SIGINFO`
