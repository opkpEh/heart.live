#!/usr/bin/env python3
from flask import Flask, Response, stream_with_context
import time
import os
import sys

app = Flask(__name__)

COLORS = [
    '\033[38;5;183m',
]

COLOR_RESET = '\033[0m'

HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'
SAVE_CURSOR = '\033[s'
RESTORE_CURSOR = '\033[u'
ALTERNATIVE_SCREEN = '\033[?1049h'
NORMAL_SCREEN = '\033[?1049l'


def clear_screen():
    return '\033[2J\033[H'


def load_frames(frames_dir):
    frames = []
    try:
        for i in range(27):
            print(i)
            with open(os.path.join(frames_dir, f"ascii-art({i}).txt"), 'r', encoding='utf-8') as f:
                frames.append(f.read())
    except Exception as e:
        print(f"Error loading frames: {e}")
        sys.exit(1)
    return frames


def apply_color(frame, color):
    return f"{color}{frame}{COLOR_RESET}"


def generate_frames(frames):
    yield ALTERNATIVE_SCREEN + HIDE_CURSOR

    frame_count = 0
    color_index = 0

    try:
        while True:
            current_frame = frames[frame_count % len(frames)]
            current_color = COLORS[color_index % len(COLORS)]

            colored_frame = apply_color(current_frame, current_color)

            yield (SAVE_CURSOR +
                   clear_screen() +
                   colored_frame + '\n' +
                   RESTORE_CURSOR)

            time.sleep(0.05)

            frame_count += 1
            color_index += 1

    except:
        yield SHOW_CURSOR + NORMAL_SCREEN


@app.route('/')
def stream_ascii():
    frames_dir = os.getenv('FRAMES_DIR', './frames')
    frames = load_frames(frames_dir)

    return Response(
        stream_with_context(generate_frames(frames)),
        mimetype='text/plain'
    )


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    try:
        app.run(host='0.0.0.0', port=port)
    finally:
        sys.stdout.write(SHOW_CURSOR + NORMAL_SCREEN)
        sys.stdout.flush()