import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--pytorch-adain-dir-url', required=True, help='The url to the local repository of pytorch-AdaIN. Can be relative or absolute.')
args = parser.parse_args()

content_images_dir_url = os.path.abspath(os.path.join('..', '..', 'data', 'test', 'content-images-512'))
style_images_dir_url = os.path.abspath(os.path.join('..', '..', 'data', 'test', 'style-images-512'))
stylized_images_dir_url = os.path.abspath('stylized-images')

# Change directory to the directory of the pytorch-AdaIN project
os.chdir(args.pytorch_adain_dir_url)

# Execute the command to stylize the content-style-image pair in another subshell
os.system(f'python test.py --content {content_images_dir_url}/100007.jpg --style {style_images_dir_url}/1.png --content_size 0 --style_size 0 --output {stylized_images_dir_url}')