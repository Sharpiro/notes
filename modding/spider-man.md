## Modify texture

```sh
SpideyTextureScaler extract source.texture
texconv -ft png source.dds
texconv -f BC1_UNORM_SRGB -dx10 modded.png
SpideyTextureScaler.exe replace source.texture modded.dds
```
## Tools

- [Spider-Man PC Modding Tool](https://www.nexusmods.com/marvelsspidermanremastered/mods/51?tab=description)
    - [SMPC source decomp](https://github.com/Phew/SMPCTool-src)
- [Improved SMPC Tool](https://www.nexusmods.com/marvelsspidermanremastered/mods/2875)
- [textconv (DirectXTex)](https://github.com/microsoft/DirectXTex/releases)
- [Spidey Texture Scaler (conversion tool)](https://www.nexusmods.com/marvelsspidermanremastered/mods/1313?tab=description)
- [Marvel's Spider-Man Texture Tool (never used)](https://www.nexusmods.com/marvelsspidermanremastered/mods/536?tab=description)

## Tutorials

- [Spider-Man Modding Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2990048873)
- [Marvels Spider-Man How to create texture mods](https://www.youtube.com/watch?v=vSPDp1acjDc)
