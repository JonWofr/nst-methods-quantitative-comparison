import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method-name', required=True, help='The name of the NST method for which the E statistic should be generated.')
    parser.add_argument('--quantitative-style-project-dir-url', required=True, help='The URL to the local repository of the quantitative-style project. Can be relative or absolute.')
    args = parser.parse_args()
    # The E statistic generation has to happen from the corresponding subdirectory
    args.quantitative_style_project_dir_url = os.path.join(args.quantitative_style_project_dir_url, 'Baed_E_scripts')
    
    generate_e_statistics(args)


def generate_e_statistics(args):
    style_images_dir_url = os.path.abspath(os.path.join('..', '..', 'data', 'test', 'style-images-512'))
    stylized_images_dir_url = os.path.abspath(os.path.join('..', '..', 'nst-methods', args.method_name, 'stylized-images'))
    stylized_images_file_url = os.path.abspath(os.path.join('..', '..', 'nst-methods', args.method_name, 'stylized-images.csv'))
    e_statistics_file_url = os.path.abspath(os.path.join('..', '..', 'nst-methods', args.method_name, 'e-statistics.csv'))

    # The algorithm to calculate the e statistics requires a file in which all stylized-image filenames are listed
    create_stylized_images_file(stylized_images_file_url, stylized_images_dir_url)

    # Change directory to the directory of the quantitative-style project
    os.chdir(args.quantitative_style_project_dir_url)

    command = f'python E_Statistics_Demo.py --style-images-dir-url {style_images_dir_url} --stylized-images-dir-url {stylized_images_dir_url} --stylized-images-file-url {stylized_images_file_url} --e-statistics-file-url {e_statistics_file_url}'

    os.system(command)


def create_stylized_images_file(stylized_images_file_url, stylized_images_dir_url):
    stylized_images_file = open(stylized_images_file_url, 'w')
    for index, stylized_image_filename in enumerate(os.listdir(stylized_images_dir_url)):
        stylized_images_file.write(stylized_image_filename if index == 0 else f'\n{stylized_image_filename}')
    stylized_images_file.close()


if __name__ == "__main__":
    main()

