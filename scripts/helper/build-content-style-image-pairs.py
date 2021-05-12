# This file can be used to randomly generate 100 content-style-pairs and write them to a csv file


import os
import random

content_images_dir_url = os.path.join('..', '..', 'data', 'test', 'content-images-512')
style_images_dir_url = os.path.join('..', '..', 'data', 'test', 'style-images-512')

style_image_filenames = os.listdir(style_images_dir_url)

content_style_image_pairs_file_url = os.path.abspath(os.path.join('..', '..', 'data', 'test', 'content-style-image-pairs.csv'))
content_style_image_pairs_file = open(content_style_image_pairs_file_url, 'w')
content_style_image_pairs_file.write('index,content_image_filename,style_image_filename')

content_image_filenames = os.listdir(content_images_dir_url)

for style_image_filename_index, style_image_filename in enumerate(style_image_filenames):
    sample_content_image_filenames = random.sample(content_image_filenames, k=10)
    for sample_content_image_filename_index, sample_content_image_filename in enumerate(sample_content_image_filenames):
        content_image_filenames.remove(sample_content_image_filename)
        content_style_image_pairs_file.write(f'\n{style_image_filename_index * 10 + sample_content_image_filename_index + 1},{sample_content_image_filename},{style_image_filename}')

content_style_image_pairs_file.close()
    