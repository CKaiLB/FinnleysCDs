import os
import subprocess

def download_spotify_playlist(url, filename):
    # Check if spotdl is installed
    try:
        subprocess.run(["spotdl", "--version"], check=True)
    except subprocess.CalledProcessError:
        print("spotdl is not installed. Please install it using 'pip install spotdl'.")
        return

    # Spotify playlist URL
    # Replace with your actual Spotify playlist URL
    playlist_url = str(url)

    # Set the output directory
    output_dir = str(filename)
    os.makedirs(output_dir, exist_ok=True)

    # Build the spotdl command
    command = [
        "spotdl",
        playlist_url,
        "--output", f"{output_dir}/",
        "--format", "mp3"
    ]

    # Run the command
    subprocess.run(command)