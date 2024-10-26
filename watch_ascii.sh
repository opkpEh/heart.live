#!/bin/bash

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo "curl is not installed. Please install it first."
    exit 1
fi

# Default URL
URL=${1:-"http://localhost:5000"}

# Clear the terminal and hide the cursor
clear
tput civis

# Function to clean up on exit
cleanup() {
    tput cnorm  # Show cursor
    exit 0
}

# Set up trap for clean exit
trap cleanup INT TERM

# Stream the animation
curl -N "$URL"
