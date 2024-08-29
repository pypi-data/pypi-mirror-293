#!/usr/bin/env python3

from omakase_media_tools.file_log.logger import setup_ffmpeg_logger, ffmpeg_error
import os
import sys
from pathlib import Path

try:
    import ffmpeg
except ImportError:
    ffmpeg_error("ffmpeg package not found.")
    ffmpeg = None

# Constants
THUMBNAIL_SIZE = '320x180'
THUMBNAIL_QUALITY = 6

ffmpeg_logger = setup_ffmpeg_logger("create_thumbnails")

def format_time(seconds):
    # Format time in HH:MM:SS.mmm
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def generate_vtt(directory, output_vtt_file, interval_in_secs=10):
    """
    Generate an OMP VTT file for a directory of thumbnail JPG files.
    :param directory: the directory of JPEG files
    :param output_vtt_file: the name of the VTT file to create
    :param interval_in_secs: the interval between thumbnails (needed to generate the VTT timestamps)
    """

    # Get the list of JPEG files
    jpeg_files = sorted([f for f in os.listdir(directory) if f.endswith('.jpeg') or f.endswith('.jpg')])

    # Create the VTT file
    with open(output_vtt_file, 'w') as vtt:
        vtt.write("WEBVTT\n\n")

        # Generate the captions
        for index, filename in enumerate(jpeg_files):
            start_time = index * interval_in_secs
            end_time = (index + 1) * interval_in_secs - 0.001  # Subtract 0.001 second to avoid overlap in timestamps
            vtt.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            vtt.write(f"{filename}\n\n")


def create_thumbnails(source_video_file_path, thumbnail_directory='', interval_in_secs=10):
    """
    Create thumbnails from source video file using ffmpeg.
    :param source_video_file_path: the path to the source video file
    :param thumbnail_directory: the directory to save thumbnails to
    :param interval_in_secs: the number of seconds between thumbnails

    Command line ffmpeg syntax for reference:
        ffmpeg
          -loglevel error
          -ss 00:00:00
          -i file
          -frames:v 100
          -s 320x180
          -qscale:v 6
          -f image2
          source_video%3d.jpg
    """

    # If ffmpeg is none, import above failed skip generation
    if ffmpeg is None:
        print("Error: ffmpeg package not available. Skipping thumbnail generation.")
        return
    try:
        thumbnail_file_template = thumbnail_directory + '/' + Path(source_video_file_path).stem + '%5d.jpg'
        stream = (
            ffmpeg
            .input(source_video_file_path, ss='00:00:00')
            .filter('fps', fps=1 / interval_in_secs)
            .output(thumbnail_file_template, s=THUMBNAIL_SIZE, format='image2', qscale=THUMBNAIL_QUALITY)
        )

        stdout, stderr = stream.run(capture_stdout=True, capture_stderr=True)
        ffmpeg_logger.info(f"FFmpeg output: {stdout.decode('utf-8')}")
        
        print("Thumbnails generated successfully")

    except ffmpeg.Error as e:
        error_message = e.stderr.decode('utf-8') if e.stderr else str(e)
        ffmpeg_error(ffmpeg_logger, error_message)
    except Exception as e:
        err_msg = str(e)
        if "ffmpeg" in err_msg.lower():
            ffmpeg_error(ffmpeg_logger, err_msg)
            return
        print(f"An unexpected error occurred: {str(e)}", file=sys.stderr)
    
def generate_thumbnail_track(source_video_file_path, output_vtt_dir, samples_per_second=2):
    # Ensure output directory exists
    if output_vtt_dir:
        os.makedirs(output_vtt_dir, exist_ok=True)

    create_thumbnails(source_video_file_path, output_vtt_dir, samples_per_second)
    generate_vtt(output_vtt_dir, str(Path(output_vtt_dir) / 'thumbnails.vtt'), samples_per_second)
