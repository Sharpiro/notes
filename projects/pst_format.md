## PST minimum physical organization

- `0x0000 Header`
- `0x4200..0x4400 Density List` - optional
- `Data`
    - `0x4400..0x4600 AMap` (Allocation Map)
    - `0x4600..0x4800 PMap` - deprecated, but still takes up space
    - `0x4800..~0x4_2400` Allocation data

## Sections

### AMap (Allocation Map)

- Block indexes in the AMap have no correlation to NDB block ids or indexes

## Glossary

- Node
    - Logical storage of data
    - Can contain subnodes
- Block
    - Physical storage of data