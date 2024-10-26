#!/usr/bin/env python3
from flask import Flask, Response, stream_with_context
import time
import os
import sys

app = Flask(__name__)

# Define colors as ANSI escape sequences for full background colors
COLORS = [
    '\033[41m',  # Red background
    '\033[44m',  # Blue background
    '\033[42m',  # Green background
    '\033[43m',  # Yellow background
    '\033[47m',  # White background
]

COLOR_RESET = '\033[0m'

# Terminal control sequences
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'
SAVE_CURSOR = '\033[s'
RESTORE_CURSOR = '\033[u'
ALTERNATIVE_SCREEN = '\033[?1049h'
NORMAL_SCREEN = '\033[?1049l'


def clear_screen():
    return '\033[2J\033[H'


def apply_full_color(color):
    # Create a full screen of color by filling it with spaces
    # Get terminal size (default to 24x80 if can't determine)
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        rows, columns = int(rows), int(columns)
    except:
        rows, columns = 24, 80

    # Create a full screen of colored spaces
    colored_screen = []
    for _ in range(rows):
        colored_screen.append(f"{color}{' ' * columns}{COLOR_RESET}")

    return '\n'.join(colored_screen)


def generate_frames():
    # Initialize terminal
    yield ALTERNATIVE_SCREEN + HIDE_CURSOR

    try:
        while True:
            for color in COLORS:
                # Save cursor, clear screen, show colored screen, restore cursor
                yield (SAVE_CURSOR +
                       clear_screen() +
                       apply_full_color(color) +
                       RESTORE_CURSOR)

                # Wait before changing to next color
                time.sleep(1)  # 1 second per color
    except:
        # Ensure we restore terminal state even if something goes wrong
        yield SHOW_CURSOR + NORMAL_SCREEN


@app.route('/')
def stream_ascii():
    return Response(
        stream_with_context(generate_frames()),
        mimetype='text/plain'
    )


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    try:
        app.run(host='0.0.0.0', port=port)
    finally:
        # Ensure terminal is restored if the app crashes
        sys.stdout.write(SHOW_CURSOR + NORMAL_SCREEN)
        sys.stdout.flush()