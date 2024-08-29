import matplotlib as mpl
import pandas as pd
from matplotlib import pyplot as plt

from cumulative.opts import options


class Canvas:
    """
    Defines the drawing area in terms of matplotlib config, colors and preferences.
    """

    def __init__(
        self, x_label: str = "X", y_label: str = "Y", interactive: bool = None, facecolor: str = "white", figsize=None
    ):
        """
        Initializes canvas with X,Y labels, in `interactive` mode on/off.
        """

        interactive = options().get("plot.interactive", prefer=interactive)

        mpl.rcParams.update(mpl.rcParamsDefault)
        plt.rcParams["font.family"] = "monospace"
        cmap = mpl.colormaps["cool"]

        if interactive:
            plt.ion()
        else:
            plt.ioff()

        if figsize is None:
            figsize = (5, 5)

        fig, ax = plt.subplots(figsize=figsize)

        ax.clear()
        ax.set_facecolor(facecolor)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        self.fig = fig
        self.ax = ax
        self.cmap = cmap
        self.pen_color = "black"

    def show(self):
        plt.show()


class UnlimitCanvas(Canvas):
    """
    Empty canvas.
    """

    def __init__(self):
        super().__init__()
        self.ax.set_facecolor("green")


class WhiteEmptyCanvas(Canvas):
    """
    Empty canvas.
    """

    def __init__(self):
        super().__init__(self)


class Plot:
    def __init__(self, c):
        """
        Initializes the plotting interface for the `c` Cumulative instance.
        """
        self.c = c

    def render(self, save_to: str = None):
        """
        Draw what's on the canvas, to screen and/or file.
        """

        if plt.isinteractive():
            plt.show()

        save_to = options().get("plot.save_to", prefer=save_to)
        if save_to is not None and save_to.endswith(".svg"):
            plt.savefig(save_to, format="svg", bbox_inches="tight")

        plt.close()
        return self

    def xrays(
        self,
        src: str | None = None,
        canvas: Canvas | None = None,
        alpha: float = 1,
        ms: float = 1,
        lw: float = 1,
        k: int = 20,
        style: str = "-",
        color=None,
    ):
        """
        Simplifies the `src` prefix interpolating on `k` points, and renders them as monochrome points/curves.
        """

        src = options().get("transforms.src", prefer=src)
        tmp = options().get("transforms.tmp")

        with options().ctx(
            {
                "transforms": {
                    "src": src,
                    "dst": tmp,
                    "drop": True,
                }
            }
        ):

            self.c.interpolate(src=src, method="pchipp", k=k, num=k)
            self.c.plot.scatter(canvas=canvas, alpha=alpha, ms=ms, lw=lw, style=style, color=color)
            self.c.drop(src=tmp)
            return self

    def scatter(
        self,
        src: str | None = None,
        canvas: Canvas | None = None,
        style: str = ".",
        ms: float = 2,
        lw: float = 1,
        score: str | None = None,
        alpha: str | None = 0.5,
        x_label: str = "X",
        y_label: str = "Y",
        color=None,
    ):

        src = options().get("transforms.src", prefer=src)
        canvas = options().get("plot.canvas_cls", prefer=canvas)

        if isinstance(canvas, type):
            # is a class, instantiate it
            canvas = canvas()

        if canvas is None:
            canvas = Canvas(x_label=x_label, y_label=y_label)

        if color is None:
            color = canvas.pen_color

        for _, row in self.c.df.iterrows():
            row_color = canvas.cmap(row[score]) if isinstance(score, str) else color
            row_alpha = row[alpha] if isinstance(alpha, str) else alpha
            pd.Series(row[f"{src}.y"], index=row[f"{src}.x"]).plot(
                style=style,
                lw=lw,
                ms=ms,
                color=row_color,
                alpha=row_alpha,
                ax=canvas.ax,
            )

        return self
