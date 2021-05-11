import os
import argparse
import time
import shutil


def main():
    method_names = ['collaborative-distillation', 'fast-neural-style', 'pytorch-adain', 'pytorch-neural-style-transfer', 'pytorch-wct']

    parser = argparse.ArgumentParser(description='Script which generates 100 stylized-images corresponding to the 100 content-style-image pairs for a given method.')
    parser.add_argument('--method-name', required=True, choices=method_names, help='The name of the NST method for which the stylized-images should be generated.')
    parser.add_argument('--method-dir-url', required=True, help='The url to the local repository of the NST method. Can be relative or absolute.')
    args = parser.parse_args()
    if args.method_name == 'collaborative-distillation':
        # This method has to be exectued from the subdirectory 'PytorchWCT'
        args.method_dir_url = os.path.join(args.method_dir_url, 'PytorchWCT')
    
    prepare_dirs(args)
    stylize_images(args)


# All previously created stylized-images (if any) for that particular method are deleted and the directory gets (re)created
def prepare_dirs(args):
    stylized_images_dir_url = os.path.join('..', '..', 'nst-methods', args.method_name, 'stylized-images')
    if os.path.isdir(stylized_images_dir_url):
        shutil.rmtree(stylized_images_dir_url)
    os.makedirs(stylized_images_dir_url)


def stylize_images(args):
    content_images_dir_url = os.path.abspath(os.path.join('..', '..', 'data', 'test', 'content-images-512'))
    style_images_dir_url = os.path.abspath(os.path.join('..', '..', 'data', 'test', 'style-images-512'))
    stylized_images_dir_url = os.path.abspath(os.path.join('..', '..', 'nst-methods', args.method_name, 'stylized-images'))

    fast_neural_style_trained_models_dir_url = os.path.abspath(os.path.join('..', '..', 'nst-methods', 'fast-neural-style', 'trained-models'))

    content_style_image_pairs_file_url = os.path.join('..', '..', 'data', 'test', 'content-style-image-pairs.csv')
    content_style_image_pairs_file = open(content_style_image_pairs_file_url, 'r')

    times_file_url = os.path.abspath(os.path.join('..', '..', 'nst-methods', args.method_name, 'times.csv'))
    times_file = open(times_file_url, 'w')
    times_file.write('content_style_image_pair_index,start_time_in_ms,end_time_in_ms,duration_in_ms')

    # Change directory to the directory of the NST method for which the stylized-images should be generated
    os.chdir(args.method_dir_url)

    for line_index, line in enumerate(content_style_image_pairs_file):
        # The first line can be excluded because it is the header of the file
        if line_index == 0:
            continue
        content_style_image_pair_index, content_image_filename, style_image_filename = line.strip('\n').split(',')
        stylized_image_filename = f'weightdefault_content{os.path.splitext(content_image_filename)[0]}_style{os.path.splitext(style_image_filename)[0]}.jpg'

        content_image_file_url = os.path.join(content_images_dir_url, content_image_filename)
        style_image_file_url = os.path.join(style_images_dir_url, style_image_filename)
        stylized_image_file_url = os.path.join(stylized_images_dir_url, stylized_image_filename)

        # The method pytorch-wct needs special preprocessing
        if args.method_name == 'pytorch-wct':
            content_image_file_url, style_image_file_url = preprocess_pytorch_wct(content_image_file_url, style_image_file_url, stylized_images_dir_url)

        # Each implementation requires a slightly different command to be executed
        command = parse_command(args.method_name, content_image_file_url, style_image_file_url, stylized_image_file_url, fast_neural_style_trained_models_dir_url)

        print(f'\n\nStylizing content-style-image-pair number {content_style_image_pair_index}...')
        start_time_in_ms = int(time.time() * 1000)

        # Execute the command to stylize the content-style-image pair in another subshell
        os.system(command)

        end_time_in_ms = int(time.time() * 1000)
        duration_in_ms = end_time_in_ms - start_time_in_ms
        times_file.write(f'\n{content_style_image_pair_index},{start_time_in_ms},{end_time_in_ms},{duration_in_ms}')
        print('\nTime needed (in ms):', duration_in_ms)

        # The method pytorch-wct needs special postprocessing
        if args.method_name == 'pytorch-wct':
            postprocess_pytorch_wct(stylized_images_dir_url)

        # Some methods do not provide the option to give the stylized-image a custom name. In order to compare the methods with each other each stylized-image has to follow the same naming convention.
        if args.method_name == 'collaborative-distillation' or args.method_name == 'pytorch-adain' or args.method_name == 'pytorch-wct':
            print('stylized-image file need renaming. Renaming...')
            rename_stylized_image(args.method_name, stylized_images_dir_url, stylized_image_filename)


    content_style_image_pairs_file.close()
    times_file.close()


def preprocess_pytorch_wct(content_image_file_url, style_image_file_url, stylized_images_dir_url):
    temp_content_image_dir_url = os.path.join(stylized_images_dir_url, 'temp', 'content-image')
    temp_style_image_dir_url = os.path.join(stylized_images_dir_url, 'temp', 'style-image')
    temp_content_image_file_url = os.path.join(temp_content_image_dir_url, 'in.jpg')
    temp_style_image_file_url = os.path.join(temp_style_image_dir_url, 'in.jpg')
    os.makedirs(temp_content_image_dir_url)
    os.makedirs(temp_style_image_dir_url)
    shutil.copyfile(content_image_file_url, temp_content_image_file_url)
    shutil.copyfile(style_image_file_url, temp_style_image_file_url)
    return temp_content_image_file_url, temp_style_image_file_url


def parse_command(method_name, content_image_file_url, style_image_file_url, stylized_image_file_url, fast_neural_style_trained_models_dir_url):
    command = {
        'collaborative-distillation': f'python WCT.py --contentPath {os.path.dirname(content_image_file_url)} --stylePath {os.path.dirname(style_image_file_url)} --picked_content_mark {os.path.basename(content_image_file_url)} --picked_style_mark {os.path.basename(style_image_file_url)} --outf {os.path.dirname(stylized_image_file_url)} --mode 16x --debug',
        'fast-neural-style': f"python {os.path.join('neural_style', 'neural_style.py')} eval --content-image {content_image_file_url} --output-image {stylized_image_file_url} --model {os.path.join(fast_neural_style_trained_models_dir_url, f'{os.path.splitext(os.path.basename(style_image_file_url))[0]}.model')} --cuda 1",
        'pytorch-adain': f'python test.py --content {content_image_file_url} --style {style_image_file_url} --content_size 0 --style_size 0 --output {os.path.dirname(stylized_image_file_url)}',
        'pytorch-neural-style-transfer': f'python NeuralStyleTransfer.py --content-image {content_image_file_url} --style-image {style_image_file_url} --stylized-image {stylized_image_file_url}',
        'pytorch-wct': f'python WCT.py --contentPath {os.path.dirname(content_image_file_url)} --stylePath {os.path.dirname(style_image_file_url)} --cuda --fineSize 0 --outf {os.path.dirname(stylized_image_file_url)}'
    }
    return command[method_name]


def postprocess_pytorch_wct(stylized_images_dir_url):
    shutil.rmtree(os.path.join(stylized_images_dir_url, 'temp'))


def rename_stylized_image(method_name, stylized_images_dir_url, stylized_image_filename):
    stylized_image_filenames = os.listdir(stylized_images_dir_url)
    most_recent_stylized_image_filename = sorted(stylized_image_filenames, key=lambda x: os.path.getctime(os.path.join(stylized_images_dir_url, x)))[-1]
    most_recent_stylized_image_file_url = os.path.join(stylized_images_dir_url, most_recent_stylized_image_filename)
    os.rename(most_recent_stylized_image_file_url, os.path.join(stylized_images_dir_url, stylized_image_filename))


if __name__ == "__main__":
    main()

