import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import argparse


plot_label_map = {
    'collaborative-distillation': 'Collaborative Distillation',
    'fast-neural-style': 'Fast Neural Style',
    'pytorch-adain': 'AdaIN',
    'pytorch-neural-style-transfer': 'A Neural Algorithm of Artistic Style',
    'pytorch-wct': 'WCT',
    'content-reference': 'Content Reference',
    'style-reference': 'Style Reference'
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--style', required=True,
                        choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', ])
    parser.add_argument('--content-index', required=True, type=int, choices=[
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9], help='There are 10 content-style-image pairs for each style. With the content-index you specify which specific one should be plotted.')
    parser.add_argument('--e-statistics', required=True,
                        choices=['E1', 'E2', 'E3', 'E4', 'E5'])
    args = parser.parse_args()

    create_scatter_plot(args)


def create_scatter_plot(args):
    method_names = ['collaborative-distillation', 'fast-neural-style', 'pytorch-adain',
                    'pytorch-neural-style-transfer', 'pytorch-wct']
    figure, axes = plt.subplots(
        nrows=3, ncols=3, figsize=(3*512/100, 3*512/100))

    all_ec_statistics_df = pd.DataFrame(
        columns=['content', 'style', 'E1', 'E2', 'E3', 'E4', 'E5', 'C'])

    for method_name in method_names:
        e_statistics_file_url = os.path.join(
            '..', '..', 'nst-methods', method_name, 'e-statistics.csv')
        c_statistics_file_url = os.path.join(
            '..', '..', 'nst-methods', method_name, 'c-statistics.csv')

        e_statistics_df = pd.read_csv(e_statistics_file_url)
        c_statistics_df = pd.read_csv(c_statistics_file_url)
        ec_statistics_df = pd.merge(
            e_statistics_df, c_statistics_df, how='inner', on=['content', 'style'])

        sub_ec_statistics_df = ec_statistics_df.query(f"style == {int(args.style)}").iloc[args.content_index][[
            'content', 'style', 'E1', 'E2', 'E3', 'E4', 'E5', 'C']]
        sub_ec_statistics_df['method_name'] = method_name
        all_ec_statistics_df = all_ec_statistics_df.append(
            sub_ec_statistics_df)

    min_e_statistic = min(all_ec_statistics_df[args.e_statistics])
    max_e_statistic = max(all_ec_statistics_df[args.e_statistics])
    range_e_statistic = max_e_statistic - min_e_statistic

    min_c_statistic = min(all_ec_statistics_df['C'])
    max_c_statistic = max(all_ec_statistics_df['C'])
    range_c_statistic = max_c_statistic - min_c_statistic

    # Make all axes invisible
    for index in range(9):
        axis = axes[int(index / 3)][index % 3]
        axis.set_xticks([])
        axis.set_xticklabels([])
        axis.set_yticks([])
        axis.set_yticklabels([])
        axis.set_frame_on(False)
        x_labels = {
            0: f'Niedrig Base-{args.e_statistics}',
            1: f'Mittel Base-{args.e_statistics}',
            2: f'Hoch Base-{args.e_statistics}'
        }
        y_labels = {
            0: 'Niedrig Base-C',
            1: 'Mittel Base-C',
            2: 'Hoch Base-C'
        }
        if index % 3 == 0:
            axis.set_ylabel(y_labels[2 - int(index / 3)], fontsize=18)
        if int(index / 3) == 2:
            axis.set_xlabel(x_labels[index % 3], fontsize=18)
        placeholder_image = plt.imread(os.path.join('..', '..', 'assets', 'images', 'placeholder.jpg'))
        axis.imshow(placeholder_image)

    for index in range(len(all_ec_statistics_df)):
        ec_statistics_series = all_ec_statistics_df.iloc[index]
        method_name = ec_statistics_series['method_name']
        stylized_image_file_url = os.path.join('..', '..', 'nst-methods', method_name, 'stylized-images',
                                               f"weightdefault_content{ec_statistics_series['content']}_style{ec_statistics_series['style']}.jpg")
        stylized_image = plt.imread(stylized_image_file_url)
        row_index = int((ec_statistics_series['C'] - min_c_statistic) /
                        (range_c_statistic / 3)) if ec_statistics_series['C'] != max_c_statistic else 2
        column_index = int((ec_statistics_series[args.e_statistics] - min_e_statistic) /
                           (range_e_statistic / 3)) if ec_statistics_series[args.e_statistics] != max_e_statistic else 2
        axes[2 - row_index][column_index].set_title(
            f"{plot_label_map[method_name]}\n(Base-{args.e_statistics}: {round(float(ec_statistics_series[args.e_statistics]), 2)}, Base-C: {ec_statistics_series['C']})")
        axes[2 - row_index][column_index].imshow(stylized_image)

    figure.subplots_adjust(wspace=0.1, hspace=0.1)
    figure_output_url = os.path.join('..', '..', 'plots', 'stylized-image-map-plots',
                                     f'stylized-image-map-plot-statistics-{args.e_statistics}-style-{args.style}-content-index-{args.content_index}.png')
    plt.savefig(figure_output_url, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    main()
