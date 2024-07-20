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

## Info

```sh
makemkvcon info --minlength=5400 file:$HOME/makemkv_dump/my_movie/backup
```

## Backup DVD

```sh
makemkvcon backup --decrypt --cache=128 --noscan -r --progress=-same disc:0 $HOME/makemkv_dump/my_movie/backup
```

- @todo: way too many logs
## Create MKV

```sh
makemkvcon mkv --minlength=5400 file:$HOME/makemkv_dump/my_movie/backup all $HOME/makemkv_dump/my_movie/mkv
```
