import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fast-neural-style-dir-url', required=True, help='The url to the local repository of the NST method \'fast-neural-style\'. Note: The repository itself is named \'examples\' but its subdirectory is named \'fast-neural-style\'. The url to the subdirectory should be provided.')
    args = parser.parse_args()
    train_models(args)


def train_models(args):
    train_data_dir_url = os.path.abspath(os.path.join('..', '..', 'data', 'train'))
    style_images_dir_url = os.path.abspath(os.path.join('..', '..', 'data', 'test', 'style-images-256'))
    trained_models_dir_url = os.path.abspath(os.path.join('..', '..', 'nst-methods', 'fast-neural-style', 'trained-models'))

    style_image_filenames = os.listdir(style_images_dir_url)

    # Change directory to the directory of the NST method for which the stylized-images should be generated
    os.chdir(args.fast_neural_style_dir_url)

    for style_image_filename in style_image_filenames:
        style_image_file_url = os.path.join(style_images_dir_url, style_image_filename)

        command = f'python neural_style/neural_style.py train --dataset {train_data_dir_url} --style-image {style_image_file_url} --save-model-dir {trained_models_dir_url} --cuda 1'

        # Execute the command to stylize the content-style-image pair in another subshell
        os.system(command)
        print(f'Training model for style image: {style_image_filename}')


if __name__ == "__main__":
    main()