## Electron

### General

- `Electron Forge Vite TS` template is currently the best
    - provides auto-restart of electron backend
    - Need to create a seperate `Vite React TS` project and point backend to it
    - They use a bunch of custom scripts but they can largely be ignored
- Many other options and user templates, but they all lack something and Forge looks to be the go forward solution

### Permissions

- `!nodeIntegration && contextIsolation`
    - The default, no Node APIs allowed in preload or renderer
    - Renderer sends to preload via `contextBridge` which then sends to Main via `ipcRenderer`
- `nodeIntegration && contextIsolation`
    - Node APIs allowed in preload only
    - Renderer sends to preload via `contextBridge`
- `nodeIntegration && !contextIsolation`
    - Node APIs allowed in preload and renderer

### Renderer

- Imports in renderer require plugin `vite-plugin-electron-renderer`

### Plugins

- `vite-plugin-electron-renderer`
    - allows Vite to correctly build ES imports inside the renderer
    - requires `nodeIntegration` and `!contextIsolation`

### Electron Misc

- `vite.config.ts` build modern
    - `build: { target: "ES2022" },`

## Wasm

### Serialization Crate

- `wasm-bindgen`
    - pro: types
    - con: serializes as classes
- `wasm-bindgen` + `serde_wasm_bindgen`
    - pro: serializes as objects
    - pro: can return Rust structures w/o `wasm-bindgen` recursive attribute albeit w/o types
    - con: no types
- `wasm-bindgen` + `tsify-next`
    - pro: types
    - pro: serializes as objects
    - con: can't automatically serialize `Vec<T>`

### Wasm Misc

#### Content Security Policy

```html
<meta http-equiv="Content-Security-Policy" content="script-src 'self' 'wasm-unsafe-eval'" />
```

## Convert Class `getters` to Object

```js
function getObject<T extends object>(objClass: T): PickProps<T> {
  const protoObj = Reflect.getPrototypeOf(objClass);
  const propNames = Object.entries(Object.getOwnPropertyDescriptors(protoObj))
    .filter(([, p]) => p.get)
    .map(([k]) => k);

  const obj: Record<string, unknown> = {};
  for (const propName of propNames) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const value = (objClass as any)[propName];
    obj[propName] = value;
  }

  return obj as PickProps<T>;
}

type PickProps<T> = Pick<
  T,
  {
    // eslint-disable-next-line @typescript-eslint/ban-types
    [K in keyof T]: T[K] extends Function ? never : K;
  }[keyof T]
>;
```
