"""Drawing module."""

import matplotlib.pyplot as plt
import numpy as np


class Drawer:
    """Drawer class."""

    def draw(self, *args, **kwargs):
        """Draw the tesselation."""
        raise NotImplementedError


class MPLDrawer(Drawer):
    """Matplotlib drawer class."""

    def __init__(self, cmap: str = "binary"):
        self.cmap = cmap

    def draw(self, tesselation: np.ndarray):
        """Draw the tesselation."""
        plt.imshow(tesselation, cmap=plt.get_cmap(self.cmap))
