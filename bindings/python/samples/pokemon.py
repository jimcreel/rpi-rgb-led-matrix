#!/usr/bin/env python3
import time
import sys
import random
import requests
import urllib.request

from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from PIL import Image

options = RGBMatrixOptions()
options.rows = 128
options.cols = 128
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'

matrix = RGBMatrix(options = options)

def get_pokemon():
    random_pokemon = random.randint(1, 898)
    url = f"https://pokeapi.co/api/v2/pokemon/{random_pokemon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_name = data["name"].capitalize()
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{random_pokemon}.png"
        image_filename = f'./showdown/{random_pokemon}.png'
        urllib.request.urlretrieve(image_url, image_filename)
        return image_filename
    else:
        print(f"Failed to fetch Pokémon data. Status code: {response.status_code}")
        return None

def process_gif(gif):
    try: 
        num_frames = gif.n_frames
    except Exception:
        sys.exit("provided image is not a gif")
    
    canvases = []
    print("Preprocessing gif, this may take a moment depending on the size of the gif...")
    gif.seek(0)
    for frame_index in range(0, num_frames):
        gif.seek(frame_index)
        frame = gif.copy()
        frame.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        canvas = matrix.CreateFrameCanvas()
        canvas.SetImage(frame.convert("RGB"))
        canvases.append(canvas)
    gif.close()

    print("Completed Preprocessing, displaying gif")
    display_gif(canvases, matrix, num_frames)

def display_gif(canvases, matrix, num_frames):
    counter = 0
    while(True):
        cur_frame = counter % num_frames
        for canvas in canvases:
            matrix.SwapOnVSync(canvases[cur_frame])
            time.sleep(0.1)
        counter += 1

def __main__():
    gif_path = get_pokemon()
    if gif_path is None:
        sys.exit(1)
    gif = Image.open(gif_path)
    process_gif(gif)

__main__()
