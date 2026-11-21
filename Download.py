from pytubefix import YouTube
from pytubefix.cli import on_progress

url = 'https://www.youtube.com/watch?v=LMda9kzKTJc'
yt = YouTube(url, on_progress_callback=on_progress)


def itags(resolution='1080p'):
    # miglior audio (bitrate più alto)
    audio_stream = (
        yt.streams.filter(only_audio=True)
        .order_by('abr')
        .desc()
        .first()
    )

    # miglior video alla risoluzione richiesta, qualunque fps
    video_stream = (
        yt.streams.filter(res=resolution, only_video=True)
        .order_by('fps')
        .desc()
        .first()
    )

    # se la risoluzione non esiste, prendi la più alta disponibile
    if video_stream is None:
        print(f'{resolution} non disponibile, uso la risoluzione massima.')
        video_stream = (
            yt.streams.filter(only_video=True)
            .order_by('resolution')
            .desc()
            .first()
        )

    print(f'Video: {video_stream.resolution} {video_stream.fps} FPS')
    print(f'Audio: {audio_stream.abr}')
    return audio_stream.itag, video_stream.itag


audio, video = itags('720p')

# nomi diversi per non sovrascrivere i file
yt.streams.get_by_itag(audio).download(filename_prefix='audio_')
yt.streams.get_by_itag(video).download(filename_prefix='video_')