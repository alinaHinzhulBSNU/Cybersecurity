import traceback
import csv
from PIL import Image, ImageDraw
from random import randint


# CUSTOM EXCEPTION
class MessageIsTooLong(Exception):
    def __init__(self, text):
        self.txt = text


# WRITE MESSAGE TO IMAGE
def encrypt(path_to_image, path_to_keys):
    keys = list()

    image = Image.open(path_to_image)
    draw = ImageDraw.Draw(image)
    pixels = image.load()
    width = image.size[0]
    height = image.size[1]

    message = input("Input message: ")

    if len(message) < width * height:
        for letter_code in ([ord(letter) for letter in message]):
            key = (randint(1, width - 10), randint(1, height - 10))
            r, g = pixels[key][0:2]
            draw.point(key, (r, g, letter_code))
            keys.append(key)
        new_file_full_name = input("Input new file full name (path): ")
        image.save(new_file_full_name, "png")
        write_keys_to_file(path_to_keys, keys)
    else:
        raise MessageIsTooLong("Message is too long for this image!")


# GET MESSAGE FROM IMAGE
def decrypt(path_to_image, path_to_keys):
    keys = read_keys_from_file(path_to_keys)
    image = Image.open(path_to_image)
    pixels = image.load()
    result = list()

    for key in keys:
        result.append(pixels[key][2])

    return ''.join([chr(symbol) for symbol in result])


# WRITE KEYS TO FILE
def write_keys_to_file(path, keys):
    with open(path, "w") as file:
        for key in keys:
            file.write(str(key) + '\n')


# READ KEYS FROM FILE
def read_keys_from_file(path):
    keys = list()

    with open(path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            pixel_coordinates = list()
            for string in row:
                pixel_coordinate = int("".join([char for char in string if char.isdigit()]))
                pixel_coordinates.append(pixel_coordinate)
            keys.append(tuple(pixel_coordinates))

    return keys


if __name__ == '__main__':
    try:
        print("STEGANOGRAPHY:")

        image_path = input("Path to image: ")
        keys_path = input("Path to keys: ")

        mode = input("\nSelect mode: \n1 - Encrypt\n2 - Decrypt\n")

        if mode == "1":
            encrypt(image_path, keys_path)
        elif mode == "2":
            message = decrypt(image_path, keys_path)
            print("Message is: '" + message + "'")
        else:
            print("Invalid mode selected!")
    except Exception as ex:
        print(traceback.format_exc())
