"""
Various visualization utilities/widgets.

"""
from fractions import Fraction

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from panda3d.core import CardMaker, NodePath, Texture, Vec4


def get_aspect_ratio(frame, max_height=10):
    """Given a frame (xmin, xmax, ymin, ymax), get the approximate
    (width, height) integer ratio.

    """
    ratio = Fraction.from_float(
        (frame[1] - frame[0]) / (frame[3] - frame[2])
    ).limit_denominator(max_height)
    return ratio.numerator, ratio.denominator


class Function2DPlot:
    """Plot a graph Z = f(X,Y).

    Parameters
    ----------
    datalims : (4,) sequence, optional
      Specifies (xmin, xmax, ymin, ymax) for the plot. If None, will
      be computed from the first call to update_data.
    size : (2,) sequence, optional
      Size provided to the matplotlib.figure.Figure object (in inches).
    dpi : int, optional
      Resolution provided to the matplotlib.figure.Figure object.
    levels : float sequence, optional
      List of isolevels for which to draw a contour.

    """
    def __init__(self, datalims=None, size=(1, 1), dpi=128, levels=None):
        self.datalims = datalims
        self.levels = levels
        fig = Figure(figsize=size, dpi=dpi, frameon=False)
        self.fig = fig
        self.canvas = FigureCanvas(fig)
        ax = Axes(fig, [0, 0, 1, 1])
        ax.set_axis_off()
        fig.add_axes(ax)
        self.ax = ax

    def update_data(self, X, Y, Z):
        """Update the data and return the corresponding HxWx3 BGR image."""
        ax = self.ax
        canvas = self.canvas
        try:
            self._img.set_data(Z)  # note that set_array aliases set_data
        except AttributeError:
            if self.datalims is None:
                self.datalims = [X.min(), X.max(), Y.min(), Y.max()]
            self._img = ax.imshow(
                Z,
                origin='lower',
                extent=self.datalims,
                interpolation='bicubic',
                aspect='auto'
            )
        if self.levels is not None:
            try:
                self._ctr.collections[0].remove()
            except AttributeError:
                pass
            finally:
                self._ctr = ax.contour(X, Y, Z, levels=self.levels)
        canvas.draw()
        image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        image.shape = canvas.get_width_height()[::-1] + (3,)  # Ensure no copy
        image = np.flip(image, -1)  # Flip RGB->BGR (Panda3d uses BGR!)
        return image


class ImageCard:
    """Panda3D card with an arbitrary image dynamically applied as texture.

    Parameters
    ----------
    name : string
      Name of the node.
    frame : Vec4, optional
      Frame of the card (xmin, xmax, ymin, ymax).
    resol : (2,) int sequence, optional
      Pixel resolution of the texture (width, height).

    """
    def __init__(self, name, frame=Vec4(0, 1, 0, 1), resol=(128, 128)):
        self.name = name
        self.frame = frame
        self._tex = Texture(self.name)
        self._tex.setup_2d_texture(
            resol[0], resol[1],
            Texture.T_unsigned_byte,
            Texture.F_rgb8,
        )
        self._cm = CardMaker(name)
        self._cm.set_frame(frame)

    def generate(self):
        card = NodePath(self._cm.generate())
        card.set_texture(self._tex)
        card.set_two_sided(True)
        #  card.set_transparency(True)
        #  card.set_alpha_scale(.9)
        return card.node()

    def set_image(self, image):
        src = image.flat
        dst_ptr = self._tex.modify_ram_image()
        dst = np.asarray(dst_ptr)
        np.copyto(dst, src)
