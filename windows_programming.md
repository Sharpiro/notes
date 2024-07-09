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

## API Overview

- Listing Windows
    - `EnumWindows`
- List Process `pids`
    - `EnumProcesses`
    - Weak because it only returns ids and you can only get more information from `pid` via `OpenProcess` if it is the same user
- List Process details
    - `NtQuerySystemInformation`
    - `SYSTEM_PROCESS_INFORMATION = 5`
    - `next` property provides offset to next process in variable length response buffer
- Get `pid` from `window handle`
    - `GetWindowThreadProcessId`
- Get `handle` from `pid`
    - `OpenProcess`
- Get `name` from `handle`
    - `QueryFullProcessImageNameA`
- Get foreground window
    - `GetForegroundWindow`
    - `wmic process where ProcessId={pid} get commandline`
- Get last input info
    - `GetLastInputInfo`

## Track process creation events

- `Register-CimIndicationEvent`
- `__InstanceCreationEvent`
- `Win32_Process`
- Allegedly replaces powershell "wmi" queries
