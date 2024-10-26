#!/usr/bin/env python3
from flask import Flask, Response, stream_with_context
import time
import os
from colorama import init, Fore, Style
import sys

app = Flask(__name__)

# Initialize colorama
init()

# ANSI escape codes for colors (these work better over curl than colorama)
COLORS = [
    '\033[31m',  # red
    '\033[33m',  # yellow
    '\033[32m',  # green
    '\033[36m',  # cyan
    '\033[34m',  # blue
    '\033[35m',  # magenta
]

COLOR_RESET = '\033[0m'


def clear_screen():
    return '\033[2J\033[H'


def apply_diagonal_rainbow(frame, frame_count):
    """Apply diagonal rainbow colors to the frame."""
    lines = frame.split('\n')
    colored_lines = []

    for y, line in enumerate(lines):
        if not line.strip():  # Skip empty lines
            colored_lines.append(line)
            continue

        colored_chars = []
        for x, char in enumerate(line):
            if char.strip():  # Only color visible characters
                # Calculate color index based on diagonal position and frame count
                color_idx = (x + y + frame_count) % len(COLORS)
                colored_chars.append(f"{COLORS[color_idx]}{char}{COLOR_RESET}")
            else:
                colored_chars.append(char)

        colored_lines.append(''.join(colored_chars))

    return '\n'.join(colored_lines)


def load_frames(frames_dir):
    frames = []
    try:
        for file_name in sorted(os.listdir(frames_dir)):
            if file_name.endswith(('.txt', '.ascii')):
                with open(os.path.join(frames_dir, file_name), 'r', encoding='utf-8') as f:
                    frames.append(f.read())
        if not frames:
            raise Exception(f"No .txt or .ascii files found in {frames_dir}")
    except Exception as e:
        print(f"Error loading frames: {e}")
        sys.exit(1)
    return frames


def generate_frames(frames, delay=0.1):
    frame_count = 0
    while True:
        for frame in frames:
            # Apply rainbow colors diagonally
            colored_frame = apply_diagonal_rainbow(frame, frame_count)
            yield clear_screen() + colored_frame + '\n'
            time.sleep(delay)
            frame_count += 1


@app.route('/')
def stream_ascii():
    frames_dir = os.getenv('FRAMES_DIR', './frames')
    delay = float(os.getenv('FRAME_DELAY', '0.1'))

    frames = load_frames(frames_dir)

    return Response(
        stream_with_context(generate_frames(frames, delay)),
        mimetype='text/plain'
    )


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)