import subprocess
import os
from pathlib import Path
import yt_dlp
import ffmpeg

def _download_video(url, output_dir, filename, format="mp4", audio_only=False):
    # Adjust the format options based on whether it's video or audio
    if audio_only:
        # If audio_only is True, extract audio and save as MP3 (or another format)
        ydl_opts = {
            'format': 'bestaudio/best',  # Download best audio
            'outtmpl': f'{output_dir}/{filename}.%(ext)s',  # Use extension of the extracted audio
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,  # Convert to the desired audio format (e.g., 'mp3', 'm4a', 'opus')
                'preferredquality': '192',  # Audio quality (e.g., 192 kbps)
            }],
        }
    else:
        # If downloading video, select the best video and audio and merge into a single file
        ydl_opts = {
            'format': f'bestvideo[ext={format}]+bestaudio[ext=m4a]/best[ext={format}]',  # Download best video with chosen format
            'outtmpl': f'{output_dir}/{filename}.%(ext)s',  # Output filename
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': format,  # Convert to the desired video format if needed
            }],
        }

    # Perform the download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print(f"Download complete: {filename}.{format}")

def _trim_video(file_path, output_dir, start_time, end_time, output_filename, output_format):
    if (start_time == "") and (end_time == ""):
        raise Exception('Start Time and End Time cannot be both empty.')

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct the full output file path and infer the output format
    output_file = os.path.join(output_dir, f'{output_filename}.{output_format}')
    
    # Trim the input file based on start_time and end_time
    input_args = {}
    if start_time != "":
        input_args['ss'] = start_time
    if end_time != "":
        input_args['to'] = end_time

    # ffmpeg trimming with input arguments and specifying output format
    ffmpeg.input(file_path, **input_args).output(output_file, format=output_format).run()

    print(f"Trimmed video/audio saved to: {output_file}")

