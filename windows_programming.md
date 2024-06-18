# Windows Programming

## DLL injection / hooking

- `SetWindowsHookEx`
    - Allows for monitoring or modifying system events and messages
- `EasyHook`
    - Hook native functions using c#
    - Supports injecting them into processes
- `Microsoft Detours`
    - Another hooking library
    - Does not provide injection
- `CreateRemoteThread`
    - inject a dll into a running program's memory
    - Does not provide hooking
- `Spy++`
    - Allows monitoring of messages, etc.
