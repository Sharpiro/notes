## Electron

### Permissions

- `!nodeIntegration && contextIsolation`
    - The default, no Node APIs allowed in preload or renderer
    - Renderer sends to preload via `contextBridge` which then sends to Main via `ipcRenderer`
- `nodeIntegration && contextIsolation`
    - Node APIs allowed in preload only
    - Renderer sends to preload via `contextBridge`
- `nodeIntegration && !contextIsolation`
    - Node APIs allowed in preload and renderer