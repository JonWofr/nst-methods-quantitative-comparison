from matplotlib import pyplot as plt
import os

style_images_dir_url = os.path.join('..', '..', 'data', 'test', 'style-images-512')
style_image_filenames = os.listdir(style_images_dir_url)
style_image_filenames_without_ext = [os.path.splitext(style_image_filename)[0] for style_image_filename in style_image_filenames]
sorted_style_image_filenames = [x[1] for x in sorted(enumerate(style_image_filenames), key=lambda x: int(style_image_filenames_without_ext[x[0]]))]

# Default dpi in matplotlib is 100
figure, axes = plt.subplots(nrows=5, ncols=2, figsize=(512*2/100, 512*5/100))

for index, style_image_filename in enumerate(sorted_style_image_filenames):
    style_image_file_url = os.path.join(style_images_dir_url, style_image_filename)
    style_image = plt.imread(style_image_file_url)
    axis = axes[int(index / 2), index % 2]
    axis.axis('off')
    axis.imshow(style_image)

figure.subplots_adjust(wspace=0, hspace=0)
# figure.suptitle('style-images')
figure_output_url = os.path.join('..', '..', 'plots', 'style-images-plot.png')
plt.savefig(figure_output_url, bbox_inches='tight', pad_inches=0)
# plt.show()