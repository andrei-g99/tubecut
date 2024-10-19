import os
import yt_dlp
import subprocess
from pathlib import Path

def _download_video(url, output_dir, filename, ffmpeg_path, format="mp4", audio_only=False):
    if audio_only:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/{filename}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': '192',
            }],
            'ffmpeg_location': str(ffmpeg_path), 
        }
    else:
        ydl_opts = {
            'format': f'bestvideo[ext={format}]+bestaudio[ext=m4a]/best[ext={format}]',
            'outtmpl': f'{output_dir}/{filename}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': format,
            }],
            'ffmpeg_location': str(ffmpeg_path), 
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def _trim_video(file_path, output_dir, start_time, end_time, output_filename, output_format, ffmpeg_path):

    if (start_time == "") and (end_time == ""):
        raise ValueError('Start Time and End Time cannot be both empty.')

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f'{output_filename}.{output_format}'

    command = [str(ffmpeg_path), '-i', str(file_path)]

    if start_time == '':
        command.extend(['-ss', '0'])
    else:
        command.extend(['-ss', start_time])
    if end_time != "":
        command.extend(['-to', end_time])

    command.append(str(output_file))

    try:
        subprocess.run(command, check=True)
        print(f"Trimmed video/audio saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error trimming video: {e}")
