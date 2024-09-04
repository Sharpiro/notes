# MakeMKV Usage

## Settings

- MakeMKV uses default profiles which reference variables.
- `makemkvcon` seems to automatically look for variables in `~/.MakeMKV/settings.conf`

```shell
# default
# app_DefaultSelectionString = "-sel:all,+sel:(favlang|nolang),-sel:mvcvideo,=100:all,-10:favlang"
app_DefaultSelectionString = "-sel:all,+sel:(favlang|nolang),+sel:forced&favlang,-sel:mvcvideo,=100:all,-10:favlang"
app_PreferredLanguage = "eng"
```

- @todo: forced subs
    - tested this with hulk, forced subs worked but seemed like they were burned in
- @todo: pull image art into mkv

## Backup DVD

```sh
makemkvcon backup \
    --decrypt \
    --cache=128 \
    --noscan \
    -r \
    --progress=-same \
    disc:0 \
    ./backup
```

- @todo: way too many logs
## Info

```sh
makemkvcon info \
    --minlength=5400 \
    file:backup
```

## Create MKV

```sh
makemkvcon mkv \
    --minlength=5400 \
    file:backup \
    all \
    mkv
```

## References

- [developer doc](https://www.makemkv.com/developers/usage.txt)
- [track selection](https://forum.makemkv.com/forum/viewtopic.php?f=10&t=4386)
