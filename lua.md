
## formatting

- `---@format disable`
- ``---@format disable-next`

## function call implicit this `self` pointer

Each are equivalent

```lua
function Game.getParty(self)
function Game:getParty()
```

```lua
emu.read8(emu, game._partyCount)
emu:read8(game._partyCount)
```

## global typings file for vs code

`globals.lua`

```lua
---@meta

emu = {}
callbacks = {}
console = {}
socket = {}
C = {}

---@param number integer
function emu.read8(self, number)
end

```
