import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--plot-type', required=True, choices=['line-plot', 'map-plot'])
parser.add_argument('--statistics', required=True, choices=['E1', 'E2', 'E3', 'E4', 'E5', 'C'])
args = parser.parse_args()

for style in range(1, 11):
    for content_index in range (10):
        os.system(f"python create-stylized-image-{args.plot_type}.py --style {style} --content-index {content_index} {'--statistics' if args.plot_type == 'line-plot' else '--e-statistics'} {args.statistics}")