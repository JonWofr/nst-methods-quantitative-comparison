import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Script to convert all .png images in a directory into .jpg images. The .png images will be replaced.')
parser.add_argument('--images-dir-url', required=True, help='The image directory in which the images are located which should be converted from .png to .jpg')
args = parser.parse_args()

images_dir_url = args.images_dir_url
images_filenames = os.listdir(images_dir_url)

for image_filename in images_filenames:
    image_file_url = os.path.join(images_dir_url, image_filename)
    with Image.open(image_file_url, formats=('PNG',)) as image:
        rgb_image = image.convert('RGB')
    rgb_image.save(f'{os.path.splitext(image_file_url)[0]}.jpg')
    os.remove(image_file_url)
