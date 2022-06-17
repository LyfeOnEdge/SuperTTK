from PIL import Image, ImageTk
from numpy import asarray
import io, os

# Converts a png encoded in bytes to an image tkinter can process
def load_image_from_byte_array(byte_array):
    return Image.open(io.BytesIO(byte_array))


def load_tk_image_from_byte_array(byte_array):
    return ImageTk.PhotoImage(load_tk_image_object_from_bytes_array(byte_array))


# Not Used. Function to create byte-encoded images for use with tkinter
def convert_image_to_bytes_array(image):
    byte_array = io.BytesIO()
    image.save(byte_array, format="PNG")
    return byte_array.getvalue()


def convert_png_to_bytes_array(png_path):
    byte_array = io.BytesIO()
    Image.open(png_path, mode="r").save(byte_array, format="PNG")
    return byte_array.getvalue()


def load(file_name, size=None):
    width, height = size
    img = Image.open(file_name)
    if size:
        img = img.resize((width, height), Image.BOX)


def convert_image_to_grayscale(image):
    return image.convert("LA")


def convert_image_to_blackandwhite(image):
    image = image.convert("L")
    return image.convert("1")
