```c
#include <stdio.h>
#include <windows.h>
// #include <wine/windows/windows.h>

int main() {
  int pid = GetCurrentProcessId();
  printf("%#06x\n", pid);
  MessageBox(NULL, "Hello, World!", "Greetings", MB_OK);
}
```

`zig cc -target x86_64-windows main.c`
`wine ./a.exe`
