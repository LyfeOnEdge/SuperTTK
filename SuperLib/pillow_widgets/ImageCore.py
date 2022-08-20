import io
from PIL import Image, ImageTk

# Converts a png encoded in bytes to an image tkinter can process
def load_tk_image_from_bytes_array(bytes_array):
    return ImageTk.PhotoImage(Image.open(io.BytesIO(bytes_array)))