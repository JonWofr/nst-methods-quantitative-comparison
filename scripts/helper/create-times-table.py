import pandas as pd
from matplotlib import pyplot as plt
import os


method_names = ['collaborative-distillation', 'fast-neural-style',
                'pytorch-adain', 'pytorch-neural-style-transfer', 'pytorch-wct']
figure, axis = plt.subplots(figsize=(1920/100, 1080/100))

all_times_df = pd.DataFrame(columns=['method_name', 'duration_min_in_ms',
                            'duration_max_in_ms', 'duration_mean_in_ms', 'duration_median_in_ms'])


for method_name in method_names:
    times_file_url = os.path.join(
        '..', '..', 'nst-methods', method_name, 'times.csv')

    times_df = pd.read_csv(times_file_url)
    duration_in_ms = times_df['duration_in_ms']
    duration_min_in_ms = duration_in_ms.min()
    duration_max_in_ms = duration_in_ms.max()
    duration_mean_in_ms = duration_in_ms.mean()
    duration_median_in_ms = duration_in_ms.median()
    all_times_df = all_times_df.append({
        'method_name': method_name,
        'duration_min_in_ms': duration_min_in_ms,
        'duration_max_in_ms': duration_max_in_ms,
        'duration_mean_in_ms': round(duration_mean_in_ms),
        'duration_median_in_ms': round(duration_median_in_ms)
    }, ignore_index=True)

axis.axis('off')
axis.table(cellText=all_times_df.values, colLabels=all_times_df.columns)

figure_output_url = os.path.join('..', '..', 'plots', 'times-table.png')
plt.savefig(figure_output_url, bbox_inches='tight', pad_inches=0.1)
# plt.show()