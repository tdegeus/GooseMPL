"""
This module provides some extensions to matplotlib.

:dependencies:

    * numpy
    * matplotlib

:copyright:

    | Tom de Geus
    | tom@geus.me
    | http://www.geus.me
"""
from __future__ import annotations

import deprecation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import curve_fit

from ._version import version


def system_has_latex():
    r"""
    Return ``True`` if the system has LaTeX installed.
    """

    from distutils.spawn import find_executable

    if find_executable("latex"):
        return True

    return False


def find_latex_font_serif():
    r"""
    Find an available font to mimic LaTeX, and return its name.
    """

    import os
    import re
    import matplotlib.font_manager

    def name(font):
        return os.path.splitext(os.path.split(font)[-1])[0].split(" - ")[0]

    fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext="ttf")

    matches = [
        r".*Computer\ Modern\ Roman.*",
        r".*CMU\ Serif.*",
        r".*CMU.*",
        r".*Times.*",
        r".*DejaVu.*",
        r".*Serif.*",
    ]

    for match in matches:
        for font in fonts:
            if re.match(match, font):
                return name(font)

    return None


def copy_style():
    r"""
    Write all goose-styles to the relevant matplotlib configuration directory.
    """

    import os

    # style definitions
    # -----------------

    styles = {}

    styles[
        "goose.mplstyle"
    ] = """
figure.figsize       : 8,6
font.weight          : normal
font.size            : 16
axes.labelsize       : medium
axes.titlesize       : medium
xtick.labelsize      : small
ytick.labelsize      : small
xtick.top            : True
ytick.right          : True
axes.facecolor       : none
axes.prop_cycle      : cycler('color',['k', 'r', 'g', 'b', 'y', 'c', 'm'])
legend.fontsize      : medium
legend.fancybox      : true
legend.columnspacing : 1.0
legend.handletextpad : 0.2
lines.linewidth      : 2
image.cmap           : afmhot
image.interpolation  : nearest
image.origin         : lower
savefig.facecolor    : none
figure.autolayout    : True
errorbar.capsize     : 2
"""

    styles[
        "goose-tick-in.mplstyle"
    ] = """
xtick.direction      : in
ytick.direction      : in
"""

    styles[
        "goose-tick-lower.mplstyle"
    ] = """
xtick.top            : False
ytick.right          : False
axes.spines.top      : False
axes.spines.right    : False
"""

    if system_has_latex() and find_latex_font_serif() is not None:

        styles[
            "goose-latex.mplstyle"
        ] = r"""
font.family          : serif
font.serif           : {serif:s}
font.weight          : bold
font.size            : 18
text.usetex          : true
text.latex.preamble  : \usepackage{{amsmath, amsfonts, amssymb, bm}}
""".format(
            serif=find_latex_font_serif()
        )

    elif system_has_latex():

        styles[
            "goose-latex.mplstyle"
        ] = r"""
font.family          : serif
font.weight          : bold
font.size            : 18
text.usetex          : true
text.latex.preamble  : \usepackage{{amsmath, amsfonts, amssymb, bm}}
"""

    else:

        import warnings

        message = """LaTeX is not installed.
To use LaTeX with 'goose-latex':
1) Install LaTeX.
2) Rerun 'GooseMPL.copy_style()'
Until that time 'goose-latex' will be an empty style."""

        warnings.warn(message, Warning)

        styles["goose-latex.mplstyle"] = ""

    # write style definitions
    # -----------------------

    # directory name where the styles are stored
    dirname = os.path.abspath(os.path.join(matplotlib.get_configdir(), "stylelib"))

    # make directory if it does not yet exist
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    # write all styles
    for fname, style in styles.items():
        open(os.path.join(dirname, fname), "w").write(style)


def latex_float(number, fmt="{0:.2g}"):
    r"""
    Convert a number to a LaTeX notation.
    See `this answer <https://stackoverflow.com/a/13490601/2646505>`__

    :argument:

        **number** (``<float>``)
            A number.

    :options:

        **fmt** (``<str>`` | [``'{0:.2g}'``])
            Format used to to initially convert the number to a string.

    :returns:

        **string** (``<str>``)
            The number in LaTeX notation.
    """

    float_str = fmt.format(number)

    if "e" in float_str:
        base, exponent = float_str.split("e")
        if base == "1":
            return fr"10^{{{int(exponent)}}}"
        else:
            return fr"{base} \times 10^{{{int(exponent)}}}"

    return float_str


def minmax(a):
    r"""
    Return [np.min(a), np.max(a)]
    """
    return np.array([np.min(a), np.max(a)])


def set_decade_lims(axis=None, direction=None):
    r"""
    Set limits the the floor/ceil values in terms of decades.

    :options:

        **axis** ([``plt.gca()``] | ...)
            Specify the axis to which to apply the limits.

        **direction** ([``None``] | ``'x'`` | ``'y'``)
            Limit the application to a certain direction (default: both).
    """

    # get current axis
    if axis is None:
        axis = plt.gca()

    # x-axis
    if direction is None or direction == "x":
        # - get current limits
        MIN, MAX = axis.get_xlim()
        # - floor/ceil to full decades
        MIN = 10 ** (np.floor(np.log10(MIN)))
        MAX = 10 ** (np.ceil(np.log10(MAX)))
        # - apply
        axis.set_xlim([MIN, MAX])

    # y-axis
    if direction is None or direction == "y":
        # - get current limits
        MIN, MAX = axis.get_ylim()
        # - floor/ceil to full decades
        MIN = 10 ** (np.floor(np.log10(MIN)))
        MAX = 10 ** (np.ceil(np.log10(MAX)))
        # - apply
        axis.set_ylim([MIN, MAX])


def scale_lim(lim, factor=1.05):
    r"""
    Scale limits to be 5% wider, to have a nice plot.

    :arguments:

        **lim** (``<list>`` | ``<str>``)
            The limits. May be a string "[...,...]", which is converted to a list.

    :options:

        **factor** ([``1.05``] | ``<float>``)
            Scale factor.
    """

    # convert string "[...,...]"
    if isinstance(lim, str):
        lim = eval(lim)

    # scale limits
    D = lim[1] - lim[0]
    lim[0] -= (factor - 1.0) / 2.0 * D
    lim[1] += (factor - 1.0) / 2.0 * D

    return lim


def abs2rel_x(x, axis=None):
    r"""
    Transform absolute x-coordinates to relative x-coordinates. Relative coordinates correspond to a
    fraction of the relevant axis. Be sure to set the limits and scale before calling this function!

    :arguments:

        **x** (``float``, ``list``)
            Absolute coordinates.

    :options:

        **axis** ([``plt.gca()``] | ...)
            Specify the axis to which to apply the limits.

    :returns:

        **x** (``float``, ``list``)
            Relative coordinates.
    """

    # get current axis
    if axis is None:
        axis = plt.gca()

    # get current limits
    xmin, xmax = axis.get_xlim()

    # transform
    # - log scale
    if axis.get_xscale() == "log":
        try:
            return [
                (np.log10(i) - np.log10(xmin)) / (np.log10(xmax) - np.log10(xmin))
                if i is not None
                else i
                for i in x
            ]
        except:
            return (np.log10(x) - np.log10(xmin)) / (np.log10(xmax) - np.log10(xmin))
    # - normal scale
    else:
        try:
            return [(i - xmin) / (xmax - xmin) if i is not None else i for i in x]
        except:
            return (x - xmin) / (xmax - xmin)


def abs2rel_y(y, axis=None):
    r"""
    Transform absolute y-coordinates to relative y-coordinates. Relative coordinates correspond to a
    fraction of the relevant axis. Be sure to set the limits and scale before calling this function!

    :arguments:

        **y** (``float``, ``list``)
            Absolute coordinates.

    :options:

        **axis** ([``plt.gca()``] | ...)
            Specify the axis to which to apply the limits.

    :returns:

        **y** (``float``, ``list``)
            Relative coordinates.
    """

    # get current axis
    if axis is None:
        axis = plt.gca()

    # get current limits
    ymin, ymax = axis.get_ylim()

    # transform
    # - log scale
    if axis.get_xscale() == "log":
        try:
            return [
                (np.log10(i) - np.log10(ymin)) / (np.log10(ymax) - np.log10(ymin))
                if i is not None
                else i
                for i in y
            ]
        except:
            return (np.log10(y) - np.log10(ymin)) / (np.log10(ymax) - np.log10(ymin))
    # - normal scale
    else:
        try:
            return [(i - ymin) / (ymax - ymin) if i is not None else i for i in y]
        except:
            return (y - ymin) / (ymax - ymin)


def rel2abs_x(x, axis=None):
    r"""
    Transform relative x-coordinates to absolute x-coordinates. Relative coordinates correspond to a
    fraction of the relevant axis. Be sure to set the limits and scale before calling this function!

    :arguments:

        **x** (``float``, ``list``)
            Relative coordinates.

    :options:

        **axis** ([``plt.gca()``] | ...)
            Specify the axis to which to apply the limits.

    :returns:

        **x** (``float``, ``list``)
            Absolute coordinates.
    """

    # get current axis
    if axis is None:
        axis = plt.gca()

    # get current limits
    xmin, xmax = axis.get_xlim()

    # transform
    # - log scale
    if axis.get_xscale() == "log":
        try:
            return [
                10.0 ** (np.log10(xmin) + i * (np.log10(xmax) - np.log10(xmin)))
                if i is not None
                else i
                for i in x
            ]
        except:
            return 10.0 ** (np.log10(xmin) + x * (np.log10(xmax) - np.log10(xmin)))
    # - normal scale
    else:
        try:
            return [xmin + i * (xmax - xmin) if i is not None else i for i in x]
        except:
            return xmin + x * (xmax - xmin)


def rel2abs_y(y, axis=None):
    r"""
    Transform relative y-coordinates to absolute y-coordinates. Relative coordinates correspond to a
    fraction of the relevant axis. Be sure to set the limits and scale before calling this function!

    :arguments:

        **y** (``float``, ``list``)
            Relative coordinates.

    :options:

        **axis** ([``plt.gca()``] | ...)
            Specify the axis to which to apply the limits.

    :returns:

        **y** (``float``, ``list``)
            Absolute coordinates.
    """

    # get current axis
    if axis is None:
        axis = plt.gca()

    # get current limits
    ymin, ymax = axis.get_ylim()

    # transform
    # - log scale
    if axis.get_xscale() == "log":
        try:
            return [
                10.0 ** (np.log10(ymin) + i * (np.log10(ymax) - np.log10(ymin)))
                if i is not None
                else i
                for i in y
            ]
        except:
            return 10.0 ** (np.log10(ymin) + y * (np.log10(ymax) - np.log10(ymin)))
    # - normal scale
    else:
        try:
            return [ymin + i * (ymax - ymin) if i is not None else i for i in y]
        except:
            return ymin + y * (ymax - ymin)


def subplots(scale_x=None, scale_y=None, scale=None, **kwargs):
    r"""
    Run ``matplotlib.pyplot.subplots`` with ``figsize`` set to the correct multiple of the default.

    :additional options:

        **scale, scale_x, scale_y** (``<float>``)
            Scale the figure-size (along one of the dimensions).
    """

    if "figsize" in kwargs:
        return plt.subplots(**kwargs)

    width, height = matplotlib.rcParams["figure.figsize"]

    if scale is not None:
        width *= scale
        height *= scale

    if scale_x is not None:
        width *= scale_x

    if scale_y is not None:
        height *= scale_y

    nrows = kwargs.pop("nrows", 1)
    ncols = kwargs.pop("ncols", 1)

    width = ncols * width
    height = nrows * height

    return plt.subplots(nrows=nrows, ncols=ncols, figsize=(width, height), **kwargs)


def savefig(*args, **kwargs):
    r"""
    Run ``matplotlib.pyplot.savefig`` while making sure that the directory exists.
    """

    import os

    dirname = os.path.dirname(args[0])

    if len(dirname) > 0:
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    return plt.savefig(*args, **kwargs)


def close(*args, **kwargs):
    r"""
    Run ``matplotlib.pyplot.close``.
    """

    return plt.close(*args, **kwargs)


def plot(x, y, units="absolute", axis=None, **kwargs):
    r"""
    Plot.

    :arguments:

        **x, y** (``list``)
            Coordinates.

    :options:

        **units** ([``'absolute'``] | ``'relative'``)
            The type of units in which the coordinates are specified. Relative coordinates correspond
            to a fraction of the relevant axis. If you use relative coordinates, be sure to set the
            limits and scale before calling this function!

        ...
            Any ``plt.plot(...)`` option.

    :returns:

        The handle of the ``plt.plot(...)`` command.
    """

    # get current axis
    if axis is None:
        axis = plt.gca()

    # transform
    if units.lower() == "relative":
        x = rel2abs_x(x, axis)
        y = rel2abs_y(y, axis)

    # plot
    return axis.plot(x, y, **kwargs)


def text(x, y, text, units="absolute", axis=None, **kwargs):
    r"""
    Plot a text.

    :arguments:

        **x, y** (``float``)
            Coordinates.

        **text** (``str``)
            Text to plot.

    :options:

        **units** ([``'absolute'``] | ``'relative'``)
            The type of units in which the coordinates are specified. Relative coordinates correspond
            to a fraction of the relevant axis. If you use relative coordinates, be sure to set the
            limits and scale before calling this function!

        ...
            Any ``plt.text(...)`` option.

    :returns:

        The handle of the ``plt.text(...)`` command.
    """

    # get current axis
    if axis is None:
        axis = plt.gca()

    # transform
    if units.lower() == "relative":
        x = rel2abs_x(x, axis)
        y = rel2abs_y(y, axis)

    # plot
    return axis.text(x, y, text, **kwargs)


def diagonal_powerlaw(
    exp, ll=None, lr=None, tl=None, tr=None, width=None, height=None, plot=False, **kwargs
):
    r"""
    Set the limits such that a power-law with a certain exponent lies on the diagonal.

    :arguments:

        **exp** (``<float>``)
            The power-law exponent.

        **ll, lr, tl, tr** (``<list>``)
            Coordinates of the lower-left, or the lower-right, or the top-left, or the top-right corner.

        **width, height** (``<float>``)
            Width or the height.

    :options:

        **axis** ([``plt.gca()``] | ...)
            Specify the axis to which to apply the limits.

        **plot** ([``False``] | ``True``)
            Plot the diagonal.

        ...
            Any ``plt.plot(...)`` option.

    :returns:

        The handle of the ``plt.plot(...)`` command (if any).
    """

    axis = kwargs.pop("axis", plt.gca())

    if width and not height:
        width = np.log(width)
    elif height and not width:
        height = np.log(height)
    else:
        raise OSError('Specify "width" or "height"')

    if ll and not lr and not tl and not tr:
        ll = [np.log(ll[0]), np.log(ll[1])]
    elif lr and not ll and not tl and not tr:
        lr = [np.log(lr[0]), np.log(lr[1])]
    elif tl and not lr and not ll and not tr:
        tl = [np.log(tl[0]), np.log(tl[1])]
    elif tr and not lr and not tl and not ll:
        tr = [np.log(tr[0]), np.log(tr[1])]
    else:
        raise OSError('Specify "ll" or "lr" or "tl" or "tr"')

    axis.set_xscale("log")
    axis.set_yscale("log")

    if width:
        height = width * np.abs(exp)
    elif height:
        width = height / np.abs(exp)

    if ll:
        axis.set_xlim(sorted([np.exp(ll[0]), np.exp(ll[0] + width)]))
        axis.set_ylim(sorted([np.exp(ll[1]), np.exp(ll[1] + height)]))
    elif lr:
        axis.set_xlim(sorted([np.exp(lr[0]), np.exp(lr[0] - width)]))
        axis.set_ylim(sorted([np.exp(lr[1]), np.exp(lr[1] + height)]))
    elif tl:
        axis.set_xlim(sorted([np.exp(tl[0]), np.exp(tl[0] + width)]))
        axis.set_ylim(sorted([np.exp(tl[1]), np.exp(tl[1] - height)]))
    elif tr:
        axis.set_xlim(sorted([np.exp(tr[0]), np.exp(tr[0] - width)]))
        axis.set_ylim(sorted([np.exp(tr[1]), np.exp(tr[1] - height)]))

    if plot:
        if exp > 0:
            return plot_powerlaw(exp, 0.0, 0.0, 1.0, **kwargs)
        else:
            return plot_powerlaw(exp, 0.0, 1.0, 1.0, **kwargs)


def annotate_powerlaw(text, exp, startx, starty, width=None, rx=0.5, ry=0.5, **kwargs):
    r"""
    Added a label to the middle of a power-law annotation (see ``goosempl.plot_powerlaw``).

    :arguments:

        **exp** (``float``)
            The power-law exponent.

        **startx, starty** (``float``)
            Start coordinates.

    :options:

        **width, height, endx, endy** (``float``)
            Definition of the end coordinate (only on of these options is needed).

        **rx, ry** ([``0.5``] | ``float``)
            x- and y-position of the label relative to the width and the height of the power-law
            annotation line (as can be plotted by ``goosempl.plot_powerlaw``).
            E.g. ``rx = 0.5, ry = 0.5`` corresponds to the middle of the line.

        **units** ([``'relative'``] | ``'absolute'``)
            The type of units in which the coordinates are specified. Relative coordinates correspond
            to a fraction of the relevant axis. If you use relative coordinates, be sure to set the
            limits and scale before calling this function!

        **axis** ([``plt.gca()``] | ...)
            Specify the axis to which to apply the limits.

        ...
            Any ``plt.text(...)`` option.

    :returns:

        The handle of the ``plt.text(...)`` command.
    """

    endx = kwargs.pop("endx", None)
    endy = kwargs.pop("endy", None)
    height = kwargs.pop("height", None)
    units = kwargs.pop("units", "relative")
    axis = kwargs.pop("axis", plt.gca())

    if axis.get_xscale() != "log" or axis.get_yscale() != "log":
        raise OSError(
            "This function only works on a log-log scale, where the power-law is a straight line"
        )

    # fix axis limits
    axis.set_xlim(axis.get_xlim())
    axis.set_ylim(axis.get_ylim())

    # apply width/height
    if width is not None:

        endx = startx + width
        endy = None

    elif height is not None:

        if exp > 0:
            endy = starty + height
        elif exp == 0:
            endy = starty
        else:
            endy = starty - height

        endx = None

    # transform
    if units.lower() == "relative":
        [startx, endx] = rel2abs_x([startx, endx], axis)
        [starty, endy] = rel2abs_y([starty, endy], axis)

    # determine multiplication constant
    const = starty / (startx ** exp)

    # get end x/y-coordinate
    if endx is not None:
        endy = const * endx ** exp
    else:
        endx = (endy / const) ** (1 / exp)

    # middle
    x = 10.0 ** (np.log10(startx) + rx * (np.log10(endx) - np.log10(startx)))
    y = 10.0 ** (np.log10(starty) + ry * (np.log10(endy) - np.log10(starty)))

    # plot
    return axis.text(x, y, text, **kwargs)


def plot_powerlaw(exp, startx, starty, width=None, **kwargs):
    r"""
    Plot a power-law.

    :arguments:

        **exp** (``float``)
            The power-law exponent.

        **startx, starty** (``float``)
            Start coordinates.

    :options:

        **width, height, endx, endy** (``float``)
            Definition of the end coordinate (only on of these options is needed).

        **units** ([``'relative'``] | ``'absolute'``)
            The type of units in which the coordinates are specified. Relative coordinates correspond
            to a fraction of the relevant axis. If you use relative coordinates, be sure to set the
            limits and scale before calling this function!

        **axis** ([``plt.gca()``] | ...)
            Specify the axis to which to apply the limits.

        **return_parameters** ([``False``] | ``True``)
            If ``True`` the output is a tuple: the handle of the plot, and the parameters that
            define the powerlaw: the constant and the exponent.

        ...
            Any ``plt.plot(...)`` option.

    :returns:

        The handle of the ``plt.plot(...)`` command.
    """

    return_parameters = kwargs.pop("return_parameters", False)
    endx = kwargs.pop("endx", None)
    endy = kwargs.pop("endy", None)
    height = kwargs.pop("height", None)
    units = kwargs.pop("units", "relative")
    axis = kwargs.pop("axis", plt.gca())

    if axis.get_xscale() != "log" or axis.get_yscale() != "log":
        raise OSError(
            "This function only works on a log-log scale, where the power-law is a straight line"
        )

    # fix axis limits
    axis.set_xlim(axis.get_xlim())
    axis.set_ylim(axis.get_ylim())

    # apply width/height
    if width is not None:

        endx = startx + width
        endy = None

    elif height is not None:

        if exp > 0:
            endy = starty + height
        elif exp == 0:
            endy = starty
        else:
            endy = starty - height

        endx = None

    # transform
    if units.lower() == "relative":
        [startx, endx] = rel2abs_x([startx, endx], axis)
        [starty, endy] = rel2abs_y([starty, endy], axis)

    # determine multiplication constant
    const = starty / (startx ** exp)

    # get end x/y-coordinate
    if endx is not None:
        endy = const * endx ** exp
    else:
        endx = (endy / const) ** (1 / exp)

    h = axis.plot([startx, endx], [starty, endy], **kwargs)

    if return_parameters:
        return (h, (const, exp))

    return h


def grid_powerlaw(exp, insert=0, skip=0, end=-1, step=0, axis=None, **kwargs):
    r"""
    Draw a power-law grid: a grid that respects a certain power-law exponent. The grid-lines start from
    the positions of the ticks.

    :arguments:

        **exp** (``float``)
            The power-law exponent.

    :options:

        **insert** (``<int>``)
            Insert extra lines in between the default lines set by the tick positions.

        **skip, end, step** (``<int>``)
            Select from the lines based on ``coor = coor[skip:end:step]``.

        **axis** ([``plt.gca()``] | ...)
            Specify the axis to which to apply the limits.

        ...
            Any ``plt.plot(...)`` option.

    :returns:

        The handle of the ``plt.plot(...)`` command.
    """

    if axis is None:
        axis = plt.gca()

    kwargs.setdefault("color", "k")
    kwargs.setdefault("linestyle", "--")
    kwargs.setdefault("linewidth", 1)

    if axis.get_xscale() != "log" or axis.get_yscale() != "log":
        raise OSError(
            "This function only works on a log-log scale, where the power-law is a straight line"
        )

    # zero-exponent: draw horizontal lines
    if exp == 0:

        # y-coordinate of the start positions
        starty = abs2rel_y(axis.get_yticks(), axis=axis)

        # insert extra coordinates
        if insert > 0:

            n = len(starty)
            x = np.linspace(0, 1, n + (n - 1) * int(insert))
            xp = np.linspace(0, 1, n)

            starty = np.interp(x, xp, starty)

        # skip coordinates
        skip = int(skip)
        end = int(end)
        step = int(1 + step)
        starty = starty[skip:end:step]

        # set remaining coordinates
        endy = starty
        startx = np.zeros(len(starty))
        endx = np.ones(len(starty))

    # all other exponents
    else:

        # get the axis' size in real coordinates
        # - get the limits
        xmin, xmax = axis.get_xlim()
        ymin, ymax = axis.get_ylim()
        # - compute the size in both directions
        deltax = np.log10(xmax) - np.log10(xmin)
        deltay = np.log10(ymax) - np.log10(ymin)

        # convert the exponent in real coordinates to an exponent in relative coordinates
        b = np.abs(exp) * deltax / deltay

        # x-coordinate of the start positions
        startx = abs2rel_x(axis.get_xticks(), axis=axis)

        # compute how many labels need to be prepended
        Dx = startx[1] - startx[0]
        nneg = int(np.floor(1.0 / (b * Dx))) - 1

        # add extra to be sure
        if insert > 0:
            nneg += 1

        # prepend
        if nneg > 0:
            startx = np.hstack((startx[0] + np.cumsum(-Dx * np.ones(nneg))[::-1], startx))

        # insert extra coordinates
        if insert > 0:

            n = len(startx)
            x = np.linspace(0, 1, n + (n - 1) * int(insert))
            xp = np.linspace(0, 1, n)

            startx = np.interp(x, xp, startx)

        # skip coordinates
        if step > 0:
            skip = int(skip)
            step = int(1 + step)
            startx = startx[skip::step]

        # x-coordinate of the end of the lines
        endx = startx + 1 / b

        # y-coordinate of the start and the end of the lines
        if exp > 0:
            starty = np.zeros(len(startx))
            endy = np.ones(len(startx))
        else:
            starty = np.ones(len(startx))
            endy = np.zeros(len(startx))

    # convert to real coordinates
    startx = rel2abs_x(startx, axis)
    endx = rel2abs_x(endx, axis)
    starty = rel2abs_y(starty, axis)
    endy = rel2abs_y(endy, axis)

    # plot
    lines = axis.plot(np.vstack((startx, endx)), np.vstack((starty, endy)), **kwargs)

    # remove access in labels
    plt.setp(lines[1:], label="_")

    # return handles
    return lines


def fit_powerlaw(
    xdata: ArrayLike,
    ydata: ArrayLike,
    prefactor: float = None,
    exponent: float = None,
    axis: plt.Axes = None,
    fmt: str = None,
    **kwargs,
):
    r"""
    Fit a powerlaw by converting the data to their logarithm and fitting a straight line.
    This function does not support more customised operation like fitting an offset,
    but custom code can be easily written by copy/pasting from here.

    :param xdata: Data points along the x-axis.
    :param ydata: Data points along the y-axis.
    :param prefactor: Prefactor (fitted if not specified).
    :param exponent: Exponent (fitted if not specified).
    :param axis: Axis to plot along (not plotted if not specified).
    :param fmt: Format for the label (if plotting). E.g. ``r"${{{0:.3f}}} x^{{{1:.2f}}}$"``
    :param kwargs: Other plot options

    :return:
        ``prefactor, exponent[, h]``
        The (fitted) prefector and exponent, and optionally the handle (if plotting)
    """

    i = np.logical_and(xdata > 0, ydata > 0)
    logx = np.log(xdata[i])
    logy = np.log(ydata[i])
    i = np.logical_or(np.isnan(logx), np.isnan(logy))
    logy = logy[~i]
    logx = logx[~i]

    if prefactor is None and exponent is None:

        def f(logx, log_prefactor, exponent):
            return log_prefactor + exponent * logx

        param, _ = curve_fit(f, logx, logy)
        prefactor = np.exp(param[0])
        exponent = param[1]

    elif prefactor is None:

        def f(logx, log_prefactor):
            return log_prefactor + exponent * logx

        param, _ = curve_fit(f, logx, logy)
        prefactor = np.exp(param[0])

    elif exponent is None:

        log_prefactor = np.log(prefactor)

        def f(logx, exponent):
            return log_prefactor + exponent * logx

        param, _ = curve_fit(f, logx, logy)
        exponent = param[0]

    if axis is None:
        return (prefactor, exponent)

    xp = np.logspace(np.log10(np.min(np.exp(logx))), np.log10(np.max(np.exp(logx))), 1000)
    yp = prefactor * xp ** exponent

    if fmt:
        assert "label" not in kwargs
        kwargs["label"] = fmt.format(prefactor, exponent)

    h = axis.plot(xp, yp, **kwargs)

    return (prefactor, exponent, h)


def random_from_cdf(shape, P, x, linspace=False, shuffle=True):
    r"""
    Generate a random number based on a discrete cumulative probability density function.

    :arguments:

        **shape** (```<array_like>``)
            Shape of the output array.

        **P, x** (```<array_like>``)
            Cumulative probability of each data point ``x``.

    :options:

        **linspace** ([``False``] | ``True``)
            If ``True`` the cumulative probabilities of the output array are drawn from an equally
            spaced array. Otherwise they are drawn randomly.

        **shuffle** ([``True``] | ``False``)
            If ``True`` the output is shuffled (before reshaping), otherwise the output it sorted.
    """

    N = np.prod(shape)

    if linspace:
        Py = np.linspace(0, 1, N)
    else:
        Py = np.sort(np.random.rand(N))

    y = np.interp(Py, P, x)

    if shuffle:
        np.random.shuffle(y)

    return y.reshape(shape)


def histogram_bin_edges_minwidth(min_width, bins):
    r"""
    Merge bins with right-neighbour until each bin has a minimum width.

    :arguments:

        **bins** (``<array_like>``)
            The bin-edges.

        **min_width** (``<float>``)
            The minimum bin width.
    """

    # escape
    if min_width is None:
        return bins
    if min_width is False:
        return bins

    # keep removing where needed
    while True:

        idx = np.where(np.diff(bins) < min_width)[0]

        if len(idx) == 0:
            return bins

        idx = idx[0]

        if idx + 1 == len(bins) - 1:
            bins = np.hstack((bins[:idx], bins[-1]))
        else:
            j = idx + 1
            k = idx + 2
            bins = np.hstack((bins[:j], bins[k:]))


def histogram_bin_edges_mincount(data, min_count, bins):
    r"""
    Merge bins with right-neighbour until each bin has a minimum number of data-points.

    :arguments:

        **data** (``<array_like>``)
            Input data. The histogram is computed over the flattened array.

        **bins** (``<array_like>`` | ``<int>``)
            The bin-edges (or the number of bins, automatically converted to equal-sized bins).

        **min_count** (``<int>``)
            The minimum number of data-points per bin.
    """

    # escape
    if min_count is None:
        return bins
    if min_count is False:
        return bins

    # check
    if not isinstance(min_count, int):
        raise OSError('"min_count" must be an integer number')

    # keep removing where needed
    while True:

        P, _ = np.histogram(data, bins=bins, density=False)

        idx = np.where(P < min_count)[0]

        if len(idx) == 0:
            return bins

        idx = idx[0]

        if idx + 1 == len(P):
            bins = np.hstack((bins[:idx], bins[-1]))
        else:
            j = idx + 1
            k = idx + 2
            bins = np.hstack((bins[:j], bins[k:]))


def histogram_bin_edges_integer(bin_edges):
    r"""
    Merge bins not encompassing an integer with the preceding bin.
    For example: a bin with edges ``[1.1, 1.9]`` is removed, but ``[0.9, 1.1]`` is not removed.

    :param array_like bin_edges: Bin-edges.
    :return: Bin-edges.
    """

    if type(bin_edges) == list:
        bin_edges = np.array(bin_edges)

    assert bin_edges.size > 1

    i = np.where(np.diff(np.floor(bin_edges)) >= 1)[0]

    if i[0] > 0:
        i[0] = 0

    i = list(i) + [bin_edges.size - 1]

    return bin_edges[i]


def histogram_bin_edges(
    data,
    bins=10,
    mode="equal",
    min_count=None,
    integer=False,
    remove_empty_edges=True,
    min_width=None,
):
    r"""
    Determine bin-edges.

    :arguments:

        **data** (``<array_like>``)
            Input data. The histogram is computed over the flattened array.

    :options:

        **bins** ([``10``] | ``<int>``)
            The number of bins.

        **mode** ([``'equal'`` | ``<str>``)
            Mode with which to compute the bin-edges:
            * ``'equal'``: each bin has equal width.
            * ``'log'``: logarithmic spacing.
            * ``'uniform'``: uniform number of data-points per bin.

        **min_count** (``<int>``)
            The minimum number of data-points per bin.

        **min_width** (``<float>``)
            The minimum width of each bin.

        **integer** ([``False``] | ``True``)
            If ``True``, bins not encompassing an integer are removed
            (e.g. a bin with edges ``[1.1, 1.9]`` is removed, but ``[0.9, 1.1]`` is not removed).

        **remove_empty_edges** ([``True``] | ``False``)
            Remove empty bins at the beginning or the end.

    :returns:

        **bin_edges** (``<array of dtype float>``)
            The edges to pass into histogram.
    """

    # determine the bin-edges

    if mode == "equal":

        bin_edges = np.linspace(np.min(data), np.max(data), bins + 1)

    elif mode == "log":

        bin_edges = np.logspace(np.log10(np.min(data)), np.log10(np.max(data)), bins + 1)

    elif mode == "uniform":

        # - check
        if hasattr(bins, "__len__"):
            raise OSError("Only the number of bins can be specified")

        # - use the minimum count to estimate the number of bins
        if min_count is not None and min_count is not False:
            if not isinstance(min_count, int):
                raise OSError('"min_count" must be an integer number')
            bins = int(np.floor(float(len(data)) / float(min_count)))

        # - number of data-points in each bin (equal for each)
        count = int(np.floor(float(len(data)) / float(bins))) * np.ones(bins, dtype="int")

        # - increase the number of data-points by one is an many bins as needed,
        #   such that the total fits the total number of data-points
        count[np.linspace(0, bins - 1, len(data) - np.sum(count)).astype(np.int)] += 1

        # - split the data
        idx = np.empty((bins + 1), dtype="int")
        idx[0] = 0
        idx[1:] = np.cumsum(count)
        idx[-1] = len(data) - 1

        # - determine the bin-edges
        bin_edges = np.unique(np.sort(data)[idx])

    else:

        raise OSError("Unknown option")

    # remove empty starting and ending bin (related to an unfortunate choice of bin-edges)

    if remove_empty_edges:

        N, _ = np.histogram(data, bins=bin_edges, density=False)

        idx = np.min(np.where(N > 0)[0])
        jdx = np.max(np.where(N > 0)[0])
        k = jdx + 2
        bin_edges = bin_edges[idx:k]

    # merge bins with too few data-points (if needed)

    bin_edges = histogram_bin_edges_mincount(data, min_count=min_count, bins=bin_edges)

    # merge bins that have too small of a width

    bin_edges = histogram_bin_edges_minwidth(min_width=min_width, bins=bin_edges)

    # select only bins that encompass an integer (and retain the original bounds)

    if integer:
        bin_edges = histogram_bin_edges_integer(bin_edges)

    # return

    return bin_edges


def histogram(data, return_edges=True, **kwargs):
    r"""
    Compute histogram.
    See `numpy.histrogram <https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html>`__

    :extra options:

        **return_edges** ([``True``] | [``False``])
            Return the bin edges if set to ``True``, return their midpoints otherwise.
    """

    # use NumPy's default function to compute the histogram
    P, bin_edges = np.histogram(data, **kwargs)

    # return default output
    if return_edges:
        return P, bin_edges

    # convert bin_edges -> mid-points of each bin
    x = np.diff(bin_edges) / 2.0 + bin_edges[:-1]

    # return with bin mid-points
    return P, x


def histogram_cumulative(data, **kwargs):
    r"""
    Compute cumulative histogram.
    See `numpy.histrogram <https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html>`__

    :extra options:

        **return_edges** ([``True``] | [``False``])
            Return the bin edges if set to ``True``, return their midpoints otherwise.

        **normalize** ([``False``] | ``True``)
            Normalize such that the final probability is one. In this case the function returns the
            (binned) cumulative probability density.
    """

    return_edges = kwargs.pop("return_edges", True)

    norm = kwargs.pop("normalize", False)

    P, edges = np.histogram(data, **kwargs)

    P = np.cumsum(P)

    if norm:
        P = P / P[-1]

    if not return_edges:
        edges = np.diff(edges) / 2.0 + edges[:-1]

    return P, edges


def hist(P, edges, **kwargs):
    r"""
    Plot histogram.
    """

    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon

    # extract local options
    axis = kwargs.pop("axis", plt.gca())
    cindex = kwargs.pop("cindex", None)
    autoscale = kwargs.pop("autoscale", True)

    # set defaults
    kwargs.setdefault("edgecolor", "k")

    # no color-index -> set transparent
    if cindex is None:
        kwargs.setdefault("facecolor", (0.0, 0.0, 0.0, 0.0))

    # convert -> list of Polygons
    poly = []
    for p, xl, xu in zip(P, edges[:-1], edges[1:]):
        coor = np.array(
            [
                [xl, 0.0],
                [xu, 0.0],
                [xu, p],
                [xl, p],
            ]
        )
        poly.append(Polygon(coor))
    args = poly

    # convert patches -> matplotlib-objects
    p = PatchCollection(args, **kwargs)
    # add colors to patches
    if cindex is not None:
        p.set_array(cindex)
    # add patches to axis
    axis.add_collection(p)

    # rescale the axes manually
    if autoscale:
        # - get limits
        xlim = [edges[0], edges[-1]]
        ylim = [0, np.max(P)]
        # - set limits +/- 10% extra margin
        axis.set_xlim([xlim[0] - 0.1 * (xlim[1] - xlim[0]), xlim[1] + 0.1 * (xlim[1] - xlim[0])])
        axis.set_ylim([ylim[0] - 0.1 * (ylim[1] - ylim[0]), ylim[1] + 0.1 * (ylim[1] - ylim[0])])

    return p


def cdf(data, mode="continuous", **kwargs):
    """
    Return cumulative density.

    :arguments:

        **data** (``<numpy.ndarray>``)
            Input data, to plot the distribution for.

    :returns:

        **P** (``<numpy.ndarray>``)
            Cumulative probability.

        **x** (``<numpy.ndarray>``)
            Data points.
    """

    return (np.linspace(0.0, 1.0, len(data)), np.sort(data))


def patch(*args, **kwargs):
    """
    Add patches to plot. The color of the patches is indexed according to a specified color-index.

    :example:

        Plot a finite element mesh: the outline of the undeformed configuration, and the deformed
        configuration for which the elements get a color e.g. based on stress::

            import matplotlib.pyplot as plt
            import goosempl          as gplt

            fig,ax = plt.subplots()

            p = gplt.patch(coor=coor+disp,conn=conn,axis=ax,cindex=stress,cmap='YlOrRd',edgecolor=None)
            _ = gplt.patch(coor=coor     ,conn=conn,axis=ax)

            cbar = fig.colorbar(p,axis=ax,aspect=10)

            plt.show()

    :arguments - option 1/2:

        **patches** (``<list>``)
            List with patch objects. Can be replaced by specifying ``coor`` and ``conn``.

    :arguments - option 2/2:

        **coor** (``<numpy.ndarray>`` | ``<list>`` (nested))
            Matrix with on each row the coordinates (positions) of each node.

        **conn** (``<numpy.ndarray>`` | ``<list>`` (nested))
            Matrix with on each row the number numbers (rows in ``coor``) which form an element (patch).

    :options:

        **cindex** (``<numpy.ndarray>``)
            Array with, for each patch, the value that should be indexed to a color.

        **axis** (``<matplotlib>``)
            Specify an axis to include to plot in. By default the current axis is used.

        **autoscale** ([``True``] | ``False``)
            Automatically update the limits of the plot (currently automatic limits of Collections are
            not supported by matplotlib).

    :recommended options:

        **cmap** (``<str>`` | ...)
            Specify a colormap.

        **linewidth** (``<float>``)
            Width of the edges.

        **edgecolor** (``<str>`` | ...)
            Color of the edges.

        **clim** (``(<float>,<float>)``)
            Lower and upper limit of the color-axis.

    :returns:

        **handle** (``<matplotlib>``)
            Handle of the patch objects.

    .. seealso::

        *   `matplotlib example
            <http://matplotlib.org/examples/api/patch_collection.html>`_.
    """

    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon

    # check dependent options
    if "coor" not in kwargs or "conn" not in kwargs:
        raise OSError('Specify both "coor" and "conn"')

    # extract local options
    axis = kwargs.pop("axis", plt.gca())
    cindex = kwargs.pop("cindex", None)
    coor = kwargs.pop("coor", None)
    conn = kwargs.pop("conn", None)
    autoscale = kwargs.pop("autoscale", True)

    # set defaults
    kwargs.setdefault("edgecolor", "k")

    # no color-index -> set transparent
    if cindex is None:
        kwargs.setdefault("facecolor", (0.0, 0.0, 0.0, 0.0))

    # convert mesh -> list of Polygons
    if coor is not None and conn is not None:
        poly = []
        for iconn in conn:
            poly.append(Polygon(coor[iconn, :]))
        args = tuple(poly, *args)

    # convert patches -> matplotlib-objects
    p = PatchCollection(args, **kwargs)
    # add colors to patches
    if cindex is not None:
        p.set_array(cindex)
    # add patches to axis
    axis.add_collection(p)

    # rescale the axes manually
    if autoscale:
        # - get limits
        xlim = [np.min(coor[:, 0]), np.max(coor[:, 0])]
        ylim = [np.min(coor[:, 1]), np.max(coor[:, 1])]
        # - set limits +/- 10% extra margin
        axis.set_xlim([xlim[0] - 0.1 * (xlim[1] - xlim[0]), xlim[1] + 0.1 * (xlim[1] - xlim[0])])
        axis.set_ylim([ylim[0] - 0.1 * (ylim[1] - ylim[0]), ylim[1] + 0.1 * (ylim[1] - ylim[0])])

    return p


@deprecation.deprecated(
    deprecated_in="0.6.0", current_version=version, details="Use openscienceplot_matplotlib"
)
def write_data(data, key, handle):
    r"""
    Save plot data to HDF5-file.

    :arguments:

        **data** (``h5py.File``)
            Opened HDF5 file.

        **key** (``<str>``)
            Name of the dataset to which to write.

        **handle**
            The handle to write.
    """

    import warnings

    if key == "/":
        raise OSError("Cannot write to root")

    if len(handle) == 1:
        handle = handle[0]

    if isinstance(handle, matplotlib.lines.Line2D):
        xy = handle.get_xydata()
        dset = data.create_dataset(key, xy.shape, dtype=xy.dtype)
        dset[:, :] = xy
        dset.attrs["artist"] = "matplotlib.lines.Line2D"
        dset.attrs["color"] = handle.get_color()
        dset.attrs["linestyle"] = handle.get_linestyle()
        dset.attrs["marker"] = handle.get_marker()
        return

    if isinstance(handle, matplotlib.container.ErrorbarContainer):
        xy = handle[0].get_xydata()
        dset = data.create_dataset(key, xy.shape, dtype=xy.dtype)
        dset[:, :] = xy
        dset.attrs["artist"] = "matplotlib.lines.Line2D"
        dset.attrs["color"] = handle[0].get_color()
        dset.attrs["linestyle"] = handle[0].get_linestyle()
        dset.attrs["marker"] = handle[0].get_marker()
        warnings.warn("Error-bars not saved, help wanted.", Warning)
        return

    raise OSError("Unknown handle. Please consider filing a bug-report.")


@deprecation.deprecated(
    deprecated_in="0.6.0", current_version=version, details="Use openscienceplot_matplotlib"
)
def restore_data(data, key, axis=None):
    r"""
    Restore plot from HDF5-file.

    :arguments:

        **data** (``h5py.File``)
            Opened HDF5 file.

        **key** (``<str>``)
            Name of the dataset from which to read.

    :options:

        **axis** ([``plt.gca()``] | ...)
            Specify the axis on which to plot.

    :returns:

        **handle**
            The handle of the created plot.
    """

    if axis is None:
        plt.gca()

    dset = data[key]

    if dset.attrs["artist"] == "matplotlib.lines.Line2D":

        xy = dset[...]
        opts = {}

        for key in ["color", "linestyle", "marker"]:
            if key in dset.attrs:
                opts[key] = dset.attrs[key]

        return axis.plot(xy, **opts)

    raise OSError("Data-set not interpretable. Please consider filing a bug-report.")
