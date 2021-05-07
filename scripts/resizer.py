import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--images-dir-url', required=True,
                    help='The image directory in which the images are located which should be resized')
parser.add_argument('--resized-images-dir-url', required=True,
                    help='The image directory in which the resized images should be stored')
parser.add_argument('--resized-image-filename-prefix', required=False, default='resized-',
                    help='An optional prefix for the resized images\' filenames')
parser.add_argument('--size', type=int, required=True,
                    help='The size the image should be resized to. Note: Only the smaller side of the image is resized to this number and the other side is resized so that the aspect ratio is preserved')
args = parser.parse_args()

images_dir_url = args.images_dir_url
images_filenames = os.listdir(images_dir_url)

for image_filename in images_filenames:
    image_file_url = os.path.join(images_dir_url, image_filename)
    with Image.open(image_file_url) as image:
        width, height = [image.width, image.height]
        aspect_ratio = width / height
        size = args.size
        new_width = int(size * aspect_ratio if width > height else size)
        new_height = int(size if width > height else size / aspect_ratio)
        resized_image = image.resize((new_width, new_height))
    resized_images_dir_url = args.resized_images_dir_url
    os.makedirs(resized_images_dir_url, exist_ok=True)
    resized_image_file_url = os.path.join(
        resized_images_dir_url, f'{args.resized_image_filename_prefix}{image_filename}')
    resized_image.save(resized_image_file_url)
