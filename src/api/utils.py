import base64
import os

from .config import Config


def get_image_data(filename: str):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    image_dir = os.path.join(current_dir, Config.IMAGE_DIRECTORY)
    fp = os.path.join(image_dir, filename)
    b64 = ""
    with open(fp, "rb") as f:
        b64 = base64.b64encode(f.read())
    return b64
