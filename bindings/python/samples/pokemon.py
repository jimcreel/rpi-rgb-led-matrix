#!/usr/bin/env python3
import time
import sys
import random
import requests
import urllib.request

from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from PIL import Image



import random
import requests
from PIL import Image
import os

def get_pokemon():
    random_pokemon = random.randint(1, 898)
    url = f"https://pokeapi.co/api/v2/pokemon/{random_pokemon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_name = data["name"].capitalize()
        shiny_chance = random.randint(1, 100)
        female_chance = random.randint(1, 100)
        path = './showdown/'
        if shiny_chance <= 25 and female_chance >= 50:
            path += 'shiny/female/'
        elif shiny_chance <= 25:
            path += 'shiny/'
        elif female_chance >= 50:
            path += 'female/'
        path += f'{random_pokemon}.gif'
        print(path)
        if os.path.exists(path):
            return path
        else:
            print(f"Failed to fetch Pokémon data. Status code: {response.status_code}")
            get_pokemon()
    else:
        print(f"Failed to fetch Pokémon data. Status code: {response.status_code}")
        return None



# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)


try:
    print("Press CTRL-C to stop.")
    gif_path = get_pokemon()
    print(gif_path)
    gif=Image.open('./showdown/858.gif')
    print(gif.n_frames)
    if gif is None:
        sys.exit(1)  # Exit the script if there's an issue fetching Pokémon data
    
    gif.seek(0)
    canvases = []
    # loop through the gif and slow it down 3x, move to the next gif after 10 seconds
    for frame_index in range(0, gif.n_frames * 3):
        matrix.SwapOnVSync(canvases[frame_index % gif.n_frames])
        time.sleep(1 / 10)
        if frame_index % gif.n_frames == 0:
            
            canvases = []
            print("Preprocessing gif, this may take a moment depending on the size of the gif...")
            for frame_index in range(0, gif.n_frames):
                gif.seek(frame_index)
                # must copy the frame out of the gif, since thumbnail() modifies the image in-place
                frame = gif.copy()
                frame.thumbnail((matrix.width, matrix.height), Image.LANCZOS)
                canvas = matrix.CreateFrameCanvas()
                canvas.SetImage(frame.convert("RGB"))
                canvases.append(canvas)
            # Close the gif file to save memory now that we have copied out all of the frames
            gif.close()
            print("Completed Preprocessing, displaying gif")

except KeyboardInterrupt:
    sys.exit(0)

