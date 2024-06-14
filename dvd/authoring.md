# Authoring

## Tools

- [DVD Audio Tools](https://dvd-audio.sourceforge.io/) #linux #foss
- [Brasero](https://github.com/GNOME/brasero) #linux #foss
- [dvdauthor](https://github.com/ldo/dvdauthor) #linux #foss 
- [libdvd-audio](https://github.com/tuffy/libdvd-audio) #linux #foss
- [devedeng](https://gitlab.com/rastersoft/devedeng/-/tags)
    - simple ui
    - better for quick import
    - menus look bad
    - potentially script-able if you can extract the python
- [dvd-slideshow](https://sourceforge.net/projects/dvd-slideshow/files)
    - not in fedora package manager
    - the `dvd-menu` sub-tool can create dvd menus from shell
    - no "play all" option
    - [possibly add play all manually](https://forum.videohelp.com/threads/193620-Q-Multiple-titles-chapter-menus-in-dvdauthorgui-dvdauthor)
- `dvdstyler`
    - prettier ui
    - better for custom ui
- [qvdvauthor](http://qdvdauthor.sourceforge.net/)
    - not in package manager
    - not tested
- `imagination`
    - slide show

## DVD-Audio

- [DVD-Audio](https://en.wikipedia.org/wiki/DVD-Audio) is an alternative standard to DVD Video for playing more/higher quality audio files

## Examples

### Encode Audio with black video

```sh
ffmpeg -f lavfi -i color=c=black:s=720x480:d=10 -i src.wav -target ntsc-dvd -aspect 16:9 -c:v mpeg2video dest.mpg
```

### Burn file to DVD w/ auto-play

All tools are available via Linux distro.

```shell
# make file dvd compatable
ffmpeg -i input.mov -target ntsc-dvd -aspect 16:9 dvd_out.mpg
# make appropriate DVD folders
dvdauthor -o dvdauthor_export/ -t dvd_out.mpg
# setup DVD folders & data to be in North America DVD format with autoplay
export VIDEO_FORMAT=NTSC && dvdauthor -o dvdauthor_export/ -T
# create an ISO image from the DVD folders
genisoimage -dvd-video -V "video_title" -o output.iso dvdauthor_export/
# burn the ISO image to a DVD writer device (check devices)
growisofs -dvd-compat -Z /dev/sr0=output.iso
```

## References

- [How to create a video DVD with command line tools](https://evilshit.wordpress.com/2015/08/10/how-to-create-a-video-dvd-with-command-line-tools)
- [Extracting DVD-Audio on Linux, the modern(ish) way](https://shkspr.mobi/blog/2019/01/extracting-dvd-audio-on-linux-the-modernish-way/)
