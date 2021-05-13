import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms


def confidence_ellipse(x, y, ax, n_std=1, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


figure, axis = plt.subplots()

axis.axvline(c='grey', lw=1)
axis.axhline(c='grey', lw=1)
axis.grid()
axis.set_xlabel('E')
axis.set_ylabel('C')

method_names = ['collaborative-distillation', 'fast-neural-style', 'pytorch-adain', 'pytorch-neural-style-transfer', 'pytorch-wct', 'content-reference', 'style-reference']
method_colors = ['red', 'blue', 'green', 'black', 'orange', 'purple', 'brown']

for method_name, method_color in zip(method_names, method_colors):
    e_statistics_file_url = os.path.join('..', '..', 'nst-methods', method_name, 'e-statistics.csv')
    c_statistics_file_url = os.path.join('..', '..', 'nst-methods', method_name, 'c-statistics.csv')
    
    e_statistics_df = pd.read_csv(e_statistics_file_url)
    c_statistics_df = pd.read_csv(c_statistics_file_url)

    x = e_statistics_df['E1']
    y = c_statistics_df['C']

    axis.scatter(x, y, c=method_color, alpha=0.5, label=method_name)

    confidence_ellipse(x, y, axis, edgecolor=method_color)


axis.legend()
plt.show()
