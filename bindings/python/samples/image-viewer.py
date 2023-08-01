#!/usr/bin/env python3
import time
import sys
import urllib.request
import random
import requests

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

def get_pokemon():
    random_pokemon = random.randint(1, 898)  # There are 898 Pokémon in total
    url = f"https://pokeapi.co/api/v2/pokemon/{random_pokemon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_name = data["name"].capitalize()
        shiny_chance = random.randint(1, 100)
        female_chance = random.randint(1, 100)
        

        
        image_url = data["sprites"]["front_default"]
        image_filename = "pokemon.png"
        urllib.request.urlretrieve(image_url, image_filename)
        return image_filename, pokemon_name
    else:
        print(f"Failed to fetch Pokémon data. Status code: {response.status_code}")
        return None

def draw_pokemon(image_file, matrix, pokemon_name):
    image = Image.open(image_file)

    # Make image fit our screen.
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    textColor = graphics.Color(255, 255, 0)

    offscreen_canvas.Clear()

    # Draw the image
    offscreen_canvas.SetImage(image.convert('RGB'), 0, 0)

    # Calculate the starting x-coordinate to right-justify the text
    text_width = len(pokemon_name) * 7  # 7 pixels wide per character (7x13 font
    starting_x = matrix.width - text_width - 5
    starting_y = 28
    # Draw the right-justified Pokémon name
    graphics.DrawText(offscreen_canvas, font, starting_x, 14, textColor, pokemon_name)

    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

try:
    print("Press CTRL-C to stop.")

    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 128
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
    options.led_rgb_sequence = 'RBG'
    options.brightness = 30
    matrix = RGBMatrix(options=options)

    while True:
        result = get_pokemon()
        
        if result is not None:
            image_file, pokemon_name = result
            draw_pokemon(image_file, matrix, pokemon_name)
        time.sleep(10)  # Adjust the sleep time as needed

except KeyboardInterrupt:
    sys.exit(0)
