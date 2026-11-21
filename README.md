# YouTube Playlist Downloader
## Only tested on Visual Studio Code

A small interactive Python script that downloads every video of a YouTube playlist in the best available quality, built on [`pytubefix`](https://github.com/JuanBindez/pytubefix). Optionally merges audio and video into a single MP4, or converts the audio track to MP3, using `ffmpeg`.

## Features

- Downloads a whole playlist into its own folder (named after the playlist)
- Always picks the **best quality**: highest resolution, then highest FPS for video, highest bitrate for audio
- Optional **merge** of audio and video into a single `.mp4` (no video re-encoding)
- Optional **MP3 conversion** of the audio track when not merging
- Numbered filenames (`001_Title.mp4`) that preserve playlist order
- Failed downloads don't stop the run: they are listed at the end
- Progress bar for every download

## Requirements

- Python 3.8+
- [`pytubefix`](https://pypi.org/project/pytubefix/)
- [`ffmpeg`](https://ffmpeg.org/download.html) (only needed for merging or MP3 conversion)

You will be asked for:

1. **The playlist or video URL**
2. **Whether to merge audio and video** into a single file (`Enter` = yes)
3. If you answered no: **whether to convert the audio to MP3** (`Enter` = no)
