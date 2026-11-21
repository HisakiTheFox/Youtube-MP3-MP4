from pytubefix import YouTube
from pytubefix.cli import on_progress

url = input('Enter the YouTube video URL: ').strip()
resolution = '1080p'

yt = YouTube(url, on_progress_callback=on_progress)


def itags(resolution='1080p'):
    # best audio (highest bitrate)
    audio_stream = (
        yt.streams.filter(only_audio=True)
        .order_by('abr')
        .desc()
        .first()
    )

    # best video at the requested resolution, any fps
    video_stream = (
        yt.streams.filter(res=resolution, only_video=True)
        .order_by('fps')
        .desc()
        .first()
    )

    # if the resolution doesn't exist, pick the highest available
    if video_stream is None:
        print(f'{resolution} not available, using the maximum resolution.')
        video_stream = max(
            yt.streams.filter(only_video=True),
            key=lambda s: (int(s.resolution[:-1]) if s.resolution else 0, s.fps or 0),
        )

    print(f'Video: {video_stream.resolution} {video_stream.fps} FPS')
    print(f'Audio: {audio_stream.abr}')
    return audio_stream.itag, video_stream.itag


audio, video = itags(resolution)

# different prefixes so the files don't overwrite each other
yt.streams.get_by_itag(audio).download(filename_prefix='audio_')
yt.streams.get_by_itag(video).download(filename_prefix='video_')