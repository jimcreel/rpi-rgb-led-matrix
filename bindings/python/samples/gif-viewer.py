#!/usr/bin/env python3
import time
import sys
import random
import requests
import urllib.request

from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from PIL import Image

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 128
options.cols = 128
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

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

def process_gif(gif):
    try: 
        num_frames = gif.n_frames
    except Exception:
        sys.exit("provided image is not a gif")

    
    # Preprocess the gifs frames into canvases to improve playback performance
    canvases = []
    print("Preprocessing gif, this may take a moment depending on the size of the gif...")
    gif.seek(0)
    for frame_index in range(0, num_frames):
        gif.seek(frame_index)
        # must copy the frame out of the gif, since thumbnail() modifies the image in-place
        frame = gif.copy()
        frame.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        canvas = matrix.CreateFrameCanvas()
        canvas.SetImage(frame.convert("RGB"))
        canvases.append(canvas)
    # Close the gif file to save memory now that we have copied out all of the frames
    images = []
    durations = []
    for i in range(gif.n_frames):
        gif.seek(i)
        gif.convert('RGBA')
        gif_temp = Image.new('RGBA',gif.size,(0,0,0,0))
        gif_temp.paste(gif,(0,0))
        images.append(gif_temp)
        durations.append(gif.info['duration'])
    images[0].save(
        'test-out.gif', 
        interlace=True,
        save_all=True,
        append_images=images[1:],
        loop=0,
        duration=durations,
        disposal=2,
        background = None,
        optimize=False
    )
    gif.close()

    print("Completed Preprocessing, displaying gif")
    # Preprocess the gifs frames into canvases to improve playback performance
    display_gif(canvases, matrix, num_frames)


# Modify the original display_gif function
def display_gif(canvases, matrix, num_frames):
    cur_frame = 0
    counter = 1
    frame_rate = 0

    while(counter <= 3):
        # Swap the canvas onto the matrix display
        matrix.SwapOnVSync(canvases[cur_frame])

        if cur_frame == num_frames - 1:
            cur_frame = 0
            counter += 1
        else:
            if frame_rate >= 0:
                cur_frame += 1
            else:
                frame_rate += 1

    # Perform the fade out effect instead of clearing
    __main__()



def __main__():
    gif_path = get_pokemon()
    print(gif_path)
    gif=Image.open(gif_path)
    gif.seek(0)
    print(gif.n_frames)
    if gif is None:
        sys.exit(1)  # Exit the script if there's an issue fetching Pokémon data
    process_gif(gif)

__main__()