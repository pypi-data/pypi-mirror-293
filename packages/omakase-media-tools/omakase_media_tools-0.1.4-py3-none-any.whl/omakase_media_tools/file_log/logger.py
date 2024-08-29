#!/usr/bin/env python3

import logging
import os
from pathlib import Path

def setup_ffmpeg_logger(name, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create 'logs' directory in the root if it doesn't exist
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)

    ffmpeg_logger = logging.getLogger(f"{name}.ffmpeg")
    ffmpeg_logger.setLevel(level)
    
    # Create log file in the 'logs' directory
    log_file_path = log_dir / f"{name}_ffmpeg.log"
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    ffmpeg_logger.addHandler(file_handler)

    # Prevent the logger from propagating messages to the root logger
    ffmpeg_logger.propagate = False

    return ffmpeg_logger

def ffmpeg_error(ffmpeg_logger: logging.Logger, message):
        out_message = f"FFmpeg error: {message}\nFFmpeg must be installed separately\nFor installation instructions, visit: https://ffmpeg.org"
        ffmpeg_logger.error(out_message)
        print(out_message)