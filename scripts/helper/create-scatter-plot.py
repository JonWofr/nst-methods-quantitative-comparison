import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--e-statistics-layer', required=True, choices=[1, 2, 3, 4, 5], type=int)
    args = parser.parse_args()

    create_scatter_plot(args)


def create_scatter_plot(args):  
    figure, axes = plt.subplots(nrows=5, ncols=2)
    for axis_row_index, axis_row in enumerate(axes):
        for axis_column_index, axis_column in enumerate(axis_row):
            configure_axis(axis_column, axis_row_index, axis_column_index, args.e_statistics_layer)

    method_names = ['collaborative-distillation', 'fast-neural-style', 'pytorch-adain', 'pytorch-neural-style-transfer', 'pytorch-wct']
    method_colors = ['red', 'blue', 'green', 'black', 'cyan']

    for method_name, method_color in zip(method_names, method_colors):
        e_statistics_file_url = os.path.join('..', '..', 'nst-methods', method_name, 'e-statistics.csv')
        c_statistics_file_url = os.path.join('..', '..', 'nst-methods', method_name, 'c-statistics.csv')

        e_statistics_df = pd.read_csv(e_statistics_file_url)
        c_statistics_df = pd.read_csv(c_statistics_file_url)

        x = e_statistics_df[f'E{str(args.e_statistics_layer)}']
        y = c_statistics_df['C']
        styles = e_statistics_df['style']
        
        plot_all_points(x, y, axes, styles, color=method_color, label=method_name)


    handles, labels = axes[-1, -1].get_legend_handles_labels()
    unique = [(handle, label) for index, (handle, label) in enumerate(zip(handles, labels)) if label not in labels[:index]]
    figure.legend(*zip(*unique), loc='lower right')
    figure.subplots_adjust(wspace=0, hspace=0)
    figure.suptitle(f'Image-specific (E from layer cov{args.e_statistics_layer}_1)')
    figure_output_url = os.path.join('..', '..', 'plots', f'scatter-plot-layer-conv{args.e_statistics_layer}_1.png')
    plt.savefig(figure_output_url)
    # plt.show()



def configure_axis(axis, axis_row_index, axis_column_index, e_statistics_layer):
    axis_index = axis_row_index * 2 + axis_column_index
    axis.axvline(c='grey', lw=1)
    axis.axhline(c='grey', lw=1)
    axis.grid()
    axis.set_xlim((-6, 0))
    axis.set_ylim((0.2, 0.8))
    if axis_row_index == 4:
        axis.set_xlabel('E')
    else:
        axis.set_xticklabels([])
    if axis_column_index == 0:
        axis.set_ylabel('C')
    else:
        axis.set_yticklabels([])


def plot_all_points(x, y, axes, styles, **kwargs):
    for x_value, y_value, style in zip(x, y, styles) :
        axes[int((style-1)/2), (style-1)%2].scatter(x_value, y_value, **kwargs)


if __name__ == "__main__":
    main()