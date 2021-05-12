import argparse
import os
import shutil

parser = argparse.ArgumentParser(description='Simple script which gives all filenames of the files in a directory a pre- and/or suffix. The renamed files are rather copies of their originals than replacements.')
parser.add_argument('--files-dir-url', required=True, help='The url of the directory which files should be renamed.')
parser.add_argument('--renamed-files-dir-url', required=True, help='The url of the directory to which the renamed files are copied.')
parser.add_argument('--prefix', required=False, default='', help='The prefix which will be prepended to every filename.')
parser.add_argument('--suffix', required=False, default='', help='The suffix which will be appended to every filename.')
args = parser.parse_args()

files_dir_url = args.files_dir_url
filenames = os.listdir(files_dir_url)

for filename in filenames:
    file_url = os.path.join(files_dir_url, filename)
    filename_without_ext, ext = os.path.splitext(filename)
    os.makedirs(args.renamed_files_dir_url, exist_ok=True)
    renamed_filename = f'{args.prefix}{filename_without_ext}{args.suffix}{ext}'
    renamed_file_url = os.path.join(args.renamed_files_dir_url, renamed_filename)
    shutil.copyfile(file_url, renamed_file_url)