#!/usr/bin/env python3
import time
import sys
import random
import requests
import urllib.request

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image


def get_pokemon():
    random_pokemon = random.randint(1, 898)  # There are 898 Pokémon in total
    url = f"https://pokeapi.co/api/v2/pokemon/{random_pokemon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_name = data["name"].capitalize()
        image_url = f"https://github.com/PokeAPI/sprites/tree/master/sprites/pokemon/other/showdown/1.gif"
        image_filename = f'./showdown/{random_pokemon}.gif'
        return image_filename
    else:
        print(f"Failed to fetch Pokémon data. Status code: {response.status_code}")
        return None
image_file = get_pokemon()
gif = Image.open(image_file)

try:
    num_frames = gif.n_frames
except Exception:
    sys.exit("provided image is not a gif")


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 128
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Preprocess the gifs frames into canvases to improve playback performance
canvases = []
print("Preprocessing gif, this may take a moment depending on the size of the gif...")
for frame_index in range(0, num_frames):
    gif.seek(frame_index)
    # must copy the frame out of the gif, since thumbnail() modifies the image in-place
    frame = gif.copy()
    frame.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    canvas = matrix.CreateFrameCanvas()
    canvas.SetImage(frame.convert("RGB"))
    canvases.append(canvas)
# Close the gif file to save memory now that we have copied out all of the frames
gif.close()

print("Completed Preprocessing, displaying gif")

try:
    print("Press CTRL-C to stop.")

    # Infinitely loop through the gif
    cur_frame = 0
    while(True):
        matrix.SwapOnVSync(canvases[cur_frame])
        if cur_frame == num_frames - 1:
            cur_frame = 0
        else:
            cur_frame += 1
except KeyboardInterrupt:
    sys.exit(0)
