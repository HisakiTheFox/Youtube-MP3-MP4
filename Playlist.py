import os
import shutil
import subprocess

from pytubefix import Playlist, YouTube
from pytubefix.cli import on_progress
from pytubefix.helpers import safe_filename

PLAYLIST_URL = 'https://youtube.com/playlist?list=PLWWPx8DxEZUPjIz0_PRniOlJZPOjnUsmm&si=QxIcPu_jQRT8FnJD'
RESOLUTION = '1080p'   # se non esiste, usa la massima disponibile
MERGE = True           # richiede ffmpeg


def pick_streams(yt, resolution):
    audio = (
        yt.streams.filter(only_audio=True)
        .order_by('abr').desc().first()
    )
    video = (
        yt.streams.filter(res=resolution, only_video=True, file_extension='mp4')
        .order_by('fps').desc().first()
    )
    if video is None:
        print(f'  {resolution} non disponibile, uso la massima.')
        video = (
            yt.streams.filter(only_video=True, file_extension='mp4')
            .order_by('resolution').desc().first()
        )
    return audio, video


def download_video(url, folder, index):
    yt = YouTube(url, on_progress_callback=on_progress)
    title = safe_filename(yt.title)
    print(f'\n[{index}] {yt.title}')

    audio, video = pick_streams(yt, RESOLUTION)
    print(f'  Video: {video.resolution} {video.fps} FPS | Audio: {audio.abr}')

    audio_path = audio.download(output_path=folder, filename=f'{index:03d}_{title}_audio.m4a')
    video_path = video.download(output_path=folder, filename=f'{index:03d}_{title}_video.mp4')

    if MERGE and shutil.which('ffmpeg'):
        out_path = os.path.join(folder, f'{index:03d}_{title}.mp4')
        subprocess.run(
            ['ffmpeg', '-y', '-loglevel', 'error',
             '-i', video_path, '-i', audio_path,
             '-c:v', 'copy', '-c:a', 'aac', out_path],
            check=True,
        )
        os.remove(audio_path)
        os.remove(video_path)
        print('  Unito in un unico file.')
    elif MERGE:
        print('  ffmpeg non trovato: audio e video lasciati separati.')


def main():
    pl = Playlist(PLAYLIST_URL)
    folder = safe_filename(pl.title)
    os.makedirs(folder, exist_ok=True)

    urls = list(pl.video_urls)
    print(f'Playlist: {pl.title} ({len(urls)} video)')

    failed = []
    for i, url in enumerate(urls, start=1):
        try:
            download_video(url, folder, i)
        except Exception as e:
            print(f'  ERRORE su {url}: {e}')
            failed.append(url)

    print('\nFinito.')
    if failed:
        print('Video non scaricati:')
        for u in failed:
            print(' ', u)


if __name__ == '__main__':
    main()