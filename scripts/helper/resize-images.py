import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Script to resize the images. If only one of the two options --smaller-side-size, --larger-side-size is provided the size of the other side will be calculated according to the aspect ratio. If both are provided the smaller side of the image will be resized to the smaller size and the larger side will be resized to the larger size (effectively preserving the images orientation).')
parser.add_argument('--images-dir-url', required=True, help='The image directory in which the images are located which should be resized.')
parser.add_argument('--resized-images-dir-url', required=True, help='The image directory in which the resized images should be stored.')
parser.add_argument('--smaller-side-size', type=int, default=None, help='By defining this the images smaller side (i.e. either width or height) will be resized to the given value and the other side will be resized respecting the aspect ratio. Either this option or --larger-side-size has to be defined or both.')
parser.add_argument('--larger-side-size', type=int, default=None, help='By defining this the images larger side (i.e. either width or height) will be resized to the given value and the other side will be resized respecting the aspect ratio. Either this option or --smaller-side-size has to be defined or both.')
args = parser.parse_args()

os.makedirs(args.resized_images_dir_url, exist_ok=True)
image_filenames = os.listdir(args.images_dir_url)

for image_filename in image_filenames:
    image_file_url = os.path.join(args.images_dir_url, image_filename)
    with Image.open(image_file_url) as image:
        aspect_ratio = image.width / image.height
        if aspect_ratio >= 1: # Image is square or horizontal
            new_width = args.larger_side_size if args.larger_side_size else int(args.smaller_side_size * aspect_ratio)
            new_height = args.smaller_side_size if args.smaller_side_size else int(args.larger_side_size / aspect_ratio)
        else: # Image is vertical
            new_width = args.smaller_side_size if args.smaller_side_size else int(args.larger_side_size * aspect_ratio)
            new_height = args.larger_side_size if args.larger_side_size else int(args.smaller_side_size / aspect_ratio)
        resized_image = image.resize((new_width, new_height))
    resized_image_file_url = os.path.join(
        args.resized_images_dir_url, image_filename)
    resized_image.save(resized_image_file_url)
