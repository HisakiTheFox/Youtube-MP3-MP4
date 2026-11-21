import os
import shutil
import subprocess

from pytubefix import Playlist, YouTube
from pytubefix.cli import on_progress
from pytubefix.helpers import safe_filename


def pick_streams(yt):
    # best audio (highest bitrate)
    audio = (
        yt.streams.filter(only_audio=True)
        .order_by('abr').desc().first()
    )
    # best video: highest resolution, then highest fps
    video = max(
        yt.streams.filter(only_video=True, file_extension='mp4'),
        key=lambda s: (int(s.resolution[:-1]) if s.resolution else 0, s.fps or 0),
    )
    return audio, video


def download_video(url, folder, index, merge):
    yt = YouTube(url, on_progress_callback=on_progress)
    title = safe_filename(yt.title)
    print(f'\n[{index}] {yt.title}')

    audio, video = pick_streams(yt)
    print(f'  Video: {video.resolution} {video.fps} FPS | Audio: {audio.abr}')

    audio_path = audio.download(output_path=folder, filename=f'{index:03d}_{title}_audio.m4a')
    video_path = video.download(output_path=folder, filename=f'{index:03d}_{title}_video.mp4')

    if merge:
        out_path = os.path.join(folder, f'{index:03d}_{title}.mp4')
        subprocess.run(
            ['ffmpeg', '-y', '-loglevel', 'error',
             '-i', video_path, '-i', audio_path,
             '-c:v', 'copy', '-c:a', 'aac', out_path],
            check=True,
        )
        os.remove(audio_path)
        os.remove(video_path)
        print('  Merged into a single file.')
    else:
        print('  Audio and video saved as separate files.')


def ask_yes_no(prompt, default=True):
    suffix = ' [Y/n]: ' if default else ' [y/N]: '
    answer = input(prompt + suffix).strip().lower()
    if not answer:
        return default
    return answer in ('y', 'yes', 's', 'si', 'sì')


def main():
    playlist_url = input('Enter the YouTube playlist URL: ').strip()
    merge = ask_yes_no('Merge audio and video into a single file?')

    if merge and not shutil.which('ffmpeg'):
        print('ffmpeg not found: files will be saved separately.')
        merge = False

    pl = Playlist(playlist_url)
    folder = safe_filename(pl.title)
    os.makedirs(folder, exist_ok=True)

    urls = list(pl.video_urls)
    print(f'Playlist: {pl.title} ({len(urls)} videos)')

    failed = []
    for i, url in enumerate(urls, start=1):
        try:
            download_video(url, folder, i, merge)
        except Exception as e:
            print(f'  ERROR on {url}: {e}')
            failed.append(url)

    print('\nDone.')
    if failed:
        print('Videos not downloaded:')
        for u in failed:
            print(' ', u)


if __name__ == '__main__':
    main()