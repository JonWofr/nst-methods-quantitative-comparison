import pandas as pd
import os
import matplotlib.pyplot as plt
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--style', required=True,
                        choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', ])
    parser.add_argument('--content-index', required=True, type=int, choices=[
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9], help='There are 10 content-style-image pairs for each style. With the content-index you specify which specific one should be plotted.')
    parser.add_argument('--statistics', required=True,
                        choices=['E1', 'E2', 'E3', 'E4', 'E5', 'C'])
    args = parser.parse_args()

    create_stylized_image_line_plot(args)


def create_stylized_image_line_plot(args):
    method_names = ['collaborative-distillation', 'fast-neural-style',
                    'pytorch-adain', 'pytorch-neural-style-transfer', 'pytorch-wct']
    figure, axes = plt.subplots(nrows=1, ncols=7, figsize=(7*512/100, 512/100))

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

    all_ec_statistics_df = all_ec_statistics_df.sort_values(
        by=[args.statistics])

    # Plot the content-image on one end of the line
    content_image_axis_index = 0 if args.statistics != 'C' else -1
    axes[content_image_axis_index].set_title('content-image')
    axes[content_image_axis_index].axis('off')
    axes[content_image_axis_index].imshow(plt.imread(os.path.join(
        '..', '..', 'data', 'test', 'content-images-512', f"{all_ec_statistics_df.iloc[0]['content']}.jpg")))

    # Plot the style-image on the other end of the line
    style_image_axis_index = 0 if args.statistics == 'C' else -1
    axes[style_image_axis_index].set_title('style-image')
    axes[style_image_axis_index].axis('off')
    axes[style_image_axis_index].imshow(plt.imread(os.path.join(
        '..', '..', 'data', 'test', 'style-images-512', f'{args.style}.jpg')))

    for index in range(len(all_ec_statistics_df)):
        ec_statistics_series = all_ec_statistics_df.iloc[index]
        method_name = ec_statistics_series['method_name']
        stylized_image_file_url = os.path.join('..', '..', 'nst-methods', method_name, 'stylized-images',
                                               f"weightdefault_content{ec_statistics_series['content']}_style{ec_statistics_series['style']}.jpg")
        stylized_image = plt.imread(stylized_image_file_url)
        axes[index + 1].set_title(
            f'{method_name}\n({args.statistics}: {round(float(ec_statistics_series[args.statistics]), 2)})')
        axes[index + 1].axis('off')
        axes[index + 1].imshow(stylized_image)

    figure.subplots_adjust(wspace=0, hspace=0)
    # figure.suptitle(f'Image comparison (sorted by {args.statistics})')
    figure_output_url = os.path.join('..', '..', 'plots', 'stylized-image-line-plots',
                                     f'stylized-image-line-plot-statistics-{args.statistics}-style-{args.style}-content-index-{args.content_index}.png')
    plt.savefig(figure_output_url, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    main()
