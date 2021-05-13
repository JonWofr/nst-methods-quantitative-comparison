# This script is needed to resize the stylized-images of the style-reference directory (which are simply the style-images of each content-style-image pair with a size of 512). The other resize-images script is useful in order to get resized images which keep their orientation. However the stylized-images of the style-reference directory also have to change their orientation. This has to be done because otherwise those images do not fit their matching content-images and the C statistics could not be calculated.

import os
from PIL import Image

stylized_images_dir_url = os.path.join('..', '..', 'nst-methods', 'style-reference', 'stylized-images')
resized_stylized_images_dir_url = os.path.join('..', '..', 'nst-methods', 'style-reference', 'stylized-images-321')
os.makedirs(resized_stylized_images_dir_url, exist_ok=True)
stylized_images_filenames = os.listdir(stylized_images_dir_url)

for stylized_image_filename in stylized_images_filenames:
    stylized_image_file_url = os.path.join(stylized_images_dir_url, stylized_image_filename)

    content_image_filename_without_ext = os.path.splitext(stylized_image_filename)[0].split('_')[1][7:]
    content_image_file_url = os.path.join('..', '..', 'data', 'test', 'content-images', f'{content_image_filename_without_ext}.jpg')
    content_image = Image.open(content_image_file_url)

    stylized_image = Image.open(stylized_image_file_url)
    resized_stylized_image = stylized_image.resize((content_image.width, content_image.height))
    resized_stylized_image.save(os.path.join(resized_stylized_images_dir_url, stylized_image_filename))
