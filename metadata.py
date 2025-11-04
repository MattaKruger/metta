import os

from mutagen.flac import FLAC

data_dir = "data"

for filename in os.listdir(data_dir):
    if filename.endswith(".flac"):
        filepath = os.path.join(data_dir, filename)
        audio = FLAC(filepath)
        print(f"Vorbis comments for {filename}:")
        if audio.tags:
            for key, value in audio.tags.items():
                print(f"  {key}: {value}")
        else:
            print("  No comments found.")
        print()
