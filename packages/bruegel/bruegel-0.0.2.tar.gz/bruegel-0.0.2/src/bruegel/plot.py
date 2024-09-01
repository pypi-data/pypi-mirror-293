import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import pathlib
import polyptich as pp


class RectangleCollection(mpl.collections.Collection):
    """
    A collection of rectangles, drawn using splines.
    This code is based on matplotlib's EllipsoidsCollection.
    But is the only collection that allows to draw the size of the patch in data coordinates.
    We therefore use this to draw spots in spatial plots.
    The other collections (e.g. RegularPolyCollection) do not allow use of data coordinates for the size.
    Drawing many Rectangles and combining them in a Collection would allows this flexibility, but is very slow.
    While plt.scatter is fast, it again is not possible to draw the size in data coordinates.
    Or in the very least, very tricky because you need to calculate the size in points.
    """

    def __init__(self, widths, heights, angles, *, units="xy", **kwargs):
        """
        Parameters
        ----------
        widths : array-like
            The lengths of the first axes (e.g., major axis lengths).
        heights : array-like
            The lengths of second axes.
        angles : array-like
            The angles of the first axes, degrees CCW from the x-axis.
        units : {'points', 'inches', 'dots', 'width', 'height', 'x', 'y', 'xy'}
            The units in which majors and minors are given; 'width' and
            'height' refer to the dimensions of the axes, while 'x' and 'y'
            refer to the *offsets* data units. 'xy' differs from all others in
            that the angle as plotted varies with the aspect ratio, and equals
            the specified angle only when the aspect ratio is unity.  Hence
            it behaves the same as the `~.patches.Rectangle` with
            ``axes.transData`` as its transform.
        **kwargs
            Forwarded to `Collection`.
        """
        super().__init__(**kwargs)
        self.set_widths(widths)
        self.set_heights(heights)
        self.set_angles(angles)
        self._units = units
        self.set_transform(mpl.transforms.IdentityTransform())
        self._transforms = np.empty((0, 3, 3))

        # note, we do not use unit_rectangle because it is centered at 0.5,0.5 instead of 0.0,0.0
        # self._paths = [mpl.path.Path.unit_rectangle()]

        # to mimick the behavior of EllipsesCollection, we use the following path centered at 0.0,0.0
        # and where size represents the radius
        self._paths = [
            mpl.path.Path(np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]]))
        ]

    def _set_transforms(self):
        """Calculate transforms immediately before drawing."""

        ax = self.axes
        fig = self.figure

        if self._units == "xy":
            sc = 1
        elif self._units == "x":
            sc = ax.bbox.width / ax.viewLim.width
        elif self._units == "y":
            sc = ax.bbox.height / ax.viewLim.height
        elif self._units == "inches":
            sc = fig.dpi
        elif self._units == "points":
            sc = fig.dpi / 72.0
        elif self._units == "width":
            sc = ax.bbox.width
        elif self._units == "height":
            sc = ax.bbox.height
        elif self._units == "dots":
            sc = 1.0
        else:
            raise ValueError(f"Unrecognized units: {self._units!r}")

        self._transforms = np.zeros((len(self._widths), 3, 3))
        widths = self._widths * sc
        heights = self._heights * sc
        sin_angle = np.sin(self._angles)
        cos_angle = np.cos(self._angles)
        self._transforms[:, 0, 0] = widths * cos_angle
        self._transforms[:, 0, 1] = heights * -sin_angle
        self._transforms[:, 1, 0] = widths * sin_angle
        self._transforms[:, 1, 1] = heights * cos_angle
        self._transforms[:, 2, 2] = 1.0

        _affine = mpl.transforms.Affine2D
        if self._units == "xy":
            m = ax.transData.get_affine().get_matrix().copy()
            m[:2, 2:] = 0
            self.set_transform(_affine(m))

    def set_widths(self, widths):
        """Set the lengths of the first axes (e.g., major axis)."""
        self._widths = 0.5 * np.asarray(widths).ravel()
        self.stale = True

    def set_heights(self, heights):
        """Set the lengths of second axes (e.g., minor axes)."""
        self._heights = 0.5 * np.asarray(heights).ravel()
        self.stale = True

    def set_angles(self, angles):
        """Set the angles of the first axes, degrees CCW from the x-axis."""
        self._angles = np.deg2rad(angles).ravel()
        self.stale = True

    def get_widths(self):
        """Get the lengths of the first axes (e.g., major axis)."""
        return self._widths * 2

    def get_heights(self):
        """Set the lengths of second axes (e.g., minor axes)."""
        return self._heights * 2

    def get_angles(self):
        """Get the angles of the first axes, degrees CCW from the x-axis."""
        return np.rad2deg(self._angles)

    @mpl.artist.allow_rasterization
    def draw(self, renderer):
        self._set_transforms()
        super().draw(renderer)


def read_tiff_slide(image_tif, extents, microns_per_pixel, axsize, desired_dpi=300):
    import tiffslide

    if isinstance(image_tif, (pathlib.Path, str)):
        image_tif = tiffslide.TiffSlide(image_tif)
    else:
        image_tif = image_tif

    # calculate expected dpi based on axis sizes and extents
    size_pixels = np.diff(extents)[:, 0] / microns_per_pixel
    desired_dpi = 300
    expected_dpi = (size_pixels / np.array(axsize)).min()

    zoom = expected_dpi / desired_dpi
    level = image_tif.get_best_level_for_downsample(zoom)
    mag = image_tif.level_downsamples[level]
    extents_image = extents / microns_per_pixel

    img = image_tif.read_region(
        location=extents_image[:, 0],
        level=level,
        size=(
            (extents_image[0, 1] - extents_image[0, 0]) / mag,
            (extents_image[1, 1] - extents_image[1, 0]) / mag,
        ),
        as_array=True,
    )
    return img

def read_zarr_slide(image_zarr, extents, microns_per_pixel, axsize, desired_dpi=300):
    from ome_zarr.io import parse_url
    if isinstance(image_zarr, (pathlib.Path, str)):
        pass
    else:
        raise ValueError("image_zarr should be a path to a zarr file")

    # calculate expected dpi based on axis sizes and extents
    size_pixels = np.diff(extents)[:, 0] / microns_per_pixel
    desired_dpi = 300
    expected_dpi = (size_pixels / np.array(axsize)).min()
    zoom = expected_dpi / desired_dpi

    # round to nearest power of 2
    level = int(np.round(np.log2(zoom)))
    mag = 2 ** level

    # read image
    from ome_zarr.reader import Reader
    reader = Reader(parse_url(image_zarr))
    nodes = list(reader())

    # first node is the image
    image_node = nodes[0]
    extents_image = (extents / microns_per_pixel / mag).astype(int)

    # ome_zarr stores in CMY => 255-
    img = 255-image_node.data[level][:, extents_image[1, 0]:extents_image[1, 1], extents_image[0, 0]:extents_image[0, 1]].transpose(1, 2, 0)
    return img


def get_value(adata, color, layer=None):
    if color in adata.var.index:
        return sc.get.obs_df(adata, color, layer=layer)
    elif color in adata.obs.columns:
        return adata.obs[color]
    elif "symbol" in adata.var.columns:
        if color in adata.var["symbol"].values:
            return sc.get.obs_df(
                adata, adata.var.query(f"symbol == '{color}'").index[0], layer=layer
            )
        else:
            raise ValueError(f"Could not find {color} in var or obs")
    else:
        raise ValueError(f"Could not find {color} in var or obs")


def plot_spatial(
    adata: sc.AnnData,
    ax=None,
    show_image: bool = True,
    alpha_image: float = 0.4,
    image_id="fullres",
    color=None,
    cmap=mpl.cm.Blues,
    extents=None,
    center=None,
    width=200,
    height=None,
    grayscale=False,
    figsize=(5, 5),
    show_locations=False,
    show_grid=False,
    step_grid=100,
    scale_spot=1,
    zorder=0,
    norm="minmax",
    spot_to_pixel=None,
    layer=None,
    transparent_colors = ("#FFFFFF", ),
    alpha_spot = 1,
):
    """
    Parameters
    ----------
    adata
        Anndata object containing spatial information.
    ax
        Matplotlib axis to plot on.
    show_image
        Whether to show the image.
    alpha_image
        Transparency of the image.
    image_id
        Key in adata.uns["spatial"]["images"].
    color
        Key in adata.obs or adata.var.
    cmap
        Colormap to use.
    extents
        Extents in microns.
    center
        Alternative to extents, center the plot around this point.
    width
        Width in microns, only used if center is not None.
    height
        Height in microns, only used if center is not None. Defaults to width.
    grayscale
        Whether to show the image in grayscale.
    figsize
        Figure size, only used if ax is None.
    show_locations
        Whether to show the spot locations.
    show_grid
        Whether to show the grid.
    scale_spot
        Scale the spot size.
    zorder
        Zorder of the spots.
    spot_to_pixel
        Key in adata.obsm. Should point to a 2D array with x and y coordinates in pixels. If None, use "image". If provided in the image, use that.
    transparent_colors
        Colors to make transparent.
    """
    image = adata.uns["spatial"]["images"][image_id]

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=100)
    else:
        fig = None
        fig = ax.get_figure()
    axsize = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).size

    if spot_to_pixel is None:
        if "spot_to_pixel" in image:
            spot_to_pixel = image["spot_to_pixel"]
        else:
            spot_to_pixel = "image"
    if spot_to_pixel not in adata.obsm:
        raise ValueError(f"Could not find {spot_to_pixel} in adata.obsm")

    # spot coordinates in microns
    spot_coordinates = (
        adata.obsm[spot_to_pixel] * image["scale"] * image["microns_per_pixel"]
    )

    ax.set_aspect("equal")

    # get extents
    if extents is None:
        if center is not None:
            if height is None:
                height = width
            extents = np.array(
                [
                    [center[0] - width / 2, center[0] + width / 2],
                    [center[1] - height / 2, center[1] + height / 2],
                ]
            )
        else:
            # default extents
            extents = np.array(
                [
                    [spot_coordinates[:, 0].min(), spot_coordinates[:, 0].max()],
                    [spot_coordinates[:, 1].min(), spot_coordinates[:, 1].max()],
                ]
            )
    else:
        extents = np.array(extents)
        if extents.ndim == 1:
            raise ValueError("extents should be a 2D array")
        elif extents.shape[0] != 2:
            raise ValueError("extents should have 2 rows")
        elif extents.shape[1] != 2:
            raise ValueError("extents should have 2 columns")

    # plot image
    if show_image:
        # extract img
        if isinstance(image["image"], np.ndarray):
            if grayscale:
                img = image["image"].mean(2, keepdims=True)
                img = np.concatenate([img] * 3, axis=2)
            else:
                img = image["image"]
            extents_image = (extents / image["microns_per_pixel"]).astype(int)

            # TODO: if out of bounds, simply pad with white
            if extents_image[0, 0] < 0:
                raise ValueError("Extents are out of bounds")
            if extents_image[1, 0] < 0:
                raise ValueError("Extents are out of bounds")
            if extents_image[0, 1] > image["dimensions"][1]:
                raise ValueError("Extents are out of bounds")
            if extents_image[1, 1] > image["dimensions"][0]:
                raise ValueError("Extents are out of bounds")

            img = img[extents_image[1, 0]:extents_image[1, 1], extents_image[0, 0]:extents_image[0, 1]]
        else:
            import tiffslide

            if (
                isinstance(image["image"], (str, pathlib.Path))
                and (str(image["image"]).endswith(".tif"))
            ) or (isinstance(image["image"], tiffslide.TiffSlide)):
                img = read_tiff_slide(
                    image["image"],
                    extents,
                    image["microns_per_pixel"],
                    axsize,
                    desired_dpi=100,
                )
            elif (
                isinstance(image["image"], (str, pathlib.Path))
                and (str(image["image"]).endswith(".zarr"))
            ):
                img = read_zarr_slide(
                    image["image"],
                    extents,
                    image["microns_per_pixel"],
                    axsize,
                    desired_dpi=100,
            )
            else:
                raise ValueError("image should be a numpy array or tiffslide.TiffSlide")
            
        # make transparent
        # for transparent_color in transparent_colors:
        #     transparent_color = ((np.array(mpl.colors.hex2color(transparent_color)))*255).astype(int)
        #     img = np.where(
        #         (img == transparent_color).all(axis=2)[:, :, None],
        #         np.array([255, 255, 255]),
        #         img,
        #     )

        if img.shape[0] == 0 or img.shape[1] == 0:
            raise ValueError("No image data found in the specified area", f"{extents=}", f"{extents_image=}")

        if img.ndim == 2:
            img = np.stack([img] * 3, axis=2)
        ax.imshow(
            img,
            extent=[
                *extents[0],
                *extents[1][::-1],
            ],
            alpha=alpha_image,
        )

    plotdata = pd.concat(
        [
            pd.DataFrame(
                adata.obsm[spot_to_pixel] * image["scale"] * image["microns_per_pixel"],
                columns=["x", "y"],
            ),
            pd.DataFrame(adata.obsm["spatial"], columns=["X", "Y"]),
        ],
        axis=1,
    )
    plotdata.index = adata.obs.index

    radius = adata.uns["spatial"]["scalefactors"]["bin_size_um"]

    plotdata_all = plotdata

    extent_filter = (
        (plotdata["x"] > extents[0, 0] - radius)
        & (plotdata["x"] < extents[0, 1] + radius)
        & (plotdata["y"] > extents[1, 0] - radius)
        & (plotdata["y"] < extents[1, 1] + radius)
    )

    # plot spots (if any)
    if len(plotdata) and (color is not None):
        plotdata = plotdata_all.loc[extent_filter].copy()

        # get expression values
        plotdata["expression"] = get_value(adata[extent_filter], color, layer=layer)

        # type of column
        if plotdata["expression"].dtype.name == "category":
            plotdata["expression"] = plotdata["expression"].cat.codes
        elif plotdata["expression"].dtype.name == "bool":
            plotdata["expression"] = plotdata["expression"].astype(int)

        if norm == "minmax":
            norm = mpl.colors.Normalize(
                plotdata["expression"].min(), plotdata["expression"].max()
            )
        elif norm == "0max":
            norm = mpl.colors.Normalize(0, plotdata["expression"].max())
        elif norm == "0q":
            norm = mpl.colors.Normalize(
                0, np.quantile(plotdata["expression"].values, 0.999)
            )
        elif norm is None:
            norm = mpl.colors.Normalize()
        else:
            norm = norm

        # remove spots with 0 value
        plotdata = plotdata.loc[plotdata["expression"] > 0]

        # Choose colormap
        if len(plotdata) > 0:

            # determine rotation
            if "rotation" in image:
                rotation = image["rotation"]
            else:
                if "rotation" not in adata.uns["spatial"]:
                    rotation = 0
                else:
                    rotation = adata.uns["spatial"]["rotation"]

            # TODO: if not rotated, we could use matshow to speed things up
            collection = RectangleCollection(
                widths=[radius * scale_spot * 1.01] * len(plotdata),
                heights=[radius * scale_spot * 1.01] * len(plotdata),
                angles=[rotation] * len(plotdata),
                facecolors=cmap(norm(plotdata["expression"])),
                edgecolors="none",
                units="xy",
                offsets=plotdata[["x", "y"]].values,
                transOffset=ax.transData,
                zorder=zorder,
                alpha = alpha_spot,
            )
            ax.add_collection(collection)

    if show_locations:
        for ix, (x, y) in plotdata[["x", "y"]].iterrows():
            text = ax.text(x, y, f"{ix}", fontsize=6, color="black", ha="center")
            text.set_path_effects(
                [
                    mpl.patheffects.Stroke(linewidth=4, foreground="white"),
                    mpl.patheffects.Normal(),
                ]
            )

    ax.set_xlim(*extents[0])
    ax.set_ylim(*extents[1][::-1])

    # size bar
    if (extents[0, 1] - extents[0, 0]) > 1000:
        size = 1000
        label = "1000 µm"
    elif (extents[0, 1] - extents[0, 0]) > 100:
        size = 100
        label = "100 µm"
    else:
        size = 10
        label = "10 µm"

    if show_grid:
        ax.grid()
        ax.set_xticks(np.arange(*(np.array(ax.get_xlim()) // step_grid * step_grid), step_grid))
        ax.tick_params(axis="x", which="major", labelrotation=90)
        ax.set_yticks(np.arange(*(np.array(ax.get_ylim()[::-1]) // step_grid * step_grid), step_grid))
        ax.tick_params(axis="y", which="major", labelrotation=0)
    else:
        ax.set_xticks([extents[0, 0], extents[0, 0] + size])
        ax.set_xticklabels(["", ""])
        ax.set_xticks([extents[0, 0] + size / 2], minor=True)
        ax.set_xticklabels([f"{label}"], minor=True, fontsize=10)
        ax.tick_params(axis="x", which="minor", length=0)

        ax.set_yticks([])

    return fig, [
        {
            "norm": norm,
            "cmap": cmap,
            "type": "colorbar",
            "label": color,
        }
    ]

def plot_spatial_legend(ax_legends, legends_info):
    for legend_info in legends_info:
        if legend_info["type"] == "colorbar":
            ax_legend = ax_legends.add_right(pp.grid.Panel((0.2, 1.5)))
            cbar = mpl.colorbar.ColorbarBase(
                ax_legend,
                cmap=legend_info["cmap"],
                norm=legend_info["norm"],
                orientation="vertical",
            )
            # put label underneath color bar
            ax_legend.annotate(legend_info["label"], xy=(0.5, 0), xytext=(0, -5), textcoords="offset points", ha="center", va="top", fontsize=12)
            # cbar.set_label(legend_info["label"], rotation = 0, labelpad = 10)


def plot_spatial_rgb(
    adata: sc.AnnData,
    ax=None,
    show_image: bool = True,
    alpha_image: float = 0.4,
    image_id="fullres",
    r=None,
    g=None,
    b=None,
    extents=None,
    center=None,
    width=200,
    height=None,
    grayscale=False,
    figsize=(5, 5),
    show_locations=False,
    legend_ax=None,
    show_grid=False,
    scale_spot=1,
    zorder=0,
    norm="minmax",
    spot_to_pixel=None,
    layer=None,
):
    """
    Parameters
    ----------
    adata
        Anndata object containing spatial information.
    ax
        Matplotlib axis to plot on.
    show_image
        Whether to show the image.
    alpha_image
        Transparency of the image.
    image_id
        Key in adata.uns["spatial"]["images"].
    extents
        Extents in microns.
    center
        Alternative to extents, center the plot around this point.
    width
        Width in microns, only used if center is not None.
    height
        Height in microns, only used if center is not None. Defaults to width.
    grayscale
        Whether to show the image in grayscale.
    figsize
        Figure size, only used if ax is None.
    show_locations
        Whether to show the spot locations.
    legend_ax
        Matplotlib axis to plot the legend on.
    show_grid
        Whether to show the grid.
    scale_spot
        Scale the spot size.
    zorder
        Zorder of the spots.
    spot_to_pixel
        Key in adata.obsm. Should point to a 2D array with x and y coordinates in pixels. If None, use "image". If provided in the image, use that.
    """
    image = adata.uns["spatial"]["images"][image_id]

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=100)
    else:
        fig = None
        fig = ax.get_figure()
    axsize = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).size

    if spot_to_pixel is None:
        if "spot_to_pixel" in image:
            spot_to_pixel = image["spot_to_pixel"]
        else:
            spot_to_pixel = "image"
    if spot_to_pixel not in adata.obsm:
        raise ValueError(f"Could not find {spot_to_pixel} in adata.obsm")

    # spot coordinates in microns
    spot_coordinates = (
        adata.obsm[spot_to_pixel] * image["scale"] * image["microns_per_pixel"]
    )

    ax.set_aspect("equal")

    # get extents
    if extents is None:
        if center is not None:
            if height is None:
                height = width
            extents = np.array(
                [
                    [center[0] - width / 2, center[0] + width / 2],
                    [center[1] - height / 2, center[1] + height / 2],
                ]
            )
        else:
            # default extents
            extents = np.array(
                [
                    [spot_coordinates[:, 0].min(), spot_coordinates[:, 0].max()],
                    [spot_coordinates[:, 1].min(), spot_coordinates[:, 1].max()],
                ]
            )
    else:
        extents = np.array(extents)
        if extents.ndim == 1:
            raise ValueError("extents should be a 2D array")
        elif extents.shape[0] != 2:
            raise ValueError("extents should have 2 rows")
        elif extents.shape[1] != 2:
            raise ValueError("extents should have 2 columns")

    # plot image
    if show_image:
        # extract img
        if isinstance(image["image"], np.ndarray):
            if grayscale:
                img = image["image"].mean(2, keepdims=True)
                img = np.concatenate([img] * 3, axis=2)
            else:
                img = image["image"]
        else:
            import tiffslide

            if (
                isinstance(image["image"], (str, pathlib.Path))
                and (str(image["image"]).endswith(".tif"))
            ) or (isinstance(image["image"], tiffslide.TiffSlide)):
                img = read_tiff_slide(
                    image["image"],
                    extents,
                    image["microns_per_pixel"],
                    axsize,
                    desired_dpi=100,
                )
            else:
                raise ValueError("image should be a numpy array or tiffslide.TiffSlide")

        ax.imshow(
            img,
            extent=[
                *extents[0],
                *extents[1][::-1],
            ],
            alpha=alpha_image,
        )

    plotdata = pd.concat(
        [
            pd.DataFrame(
                adata.obsm[spot_to_pixel] * image["scale"] * image["microns_per_pixel"],
                columns=["x", "y"],
            ),
            pd.DataFrame(adata.obsm["spatial"], columns=["X", "Y"]),
        ],
        axis=1,
    )
    plotdata.index = adata.obs.index

    radius = adata.uns["spatial"]["scalefactors"]["bin_size_um"]

    # remove spots outside the plot
    plotdata = plotdata.loc[
        (plotdata["x"] > extents[0, 0] - radius)
        & (plotdata["x"] < extents[0, 1] + radius)
        & (plotdata["y"] > extents[1, 0] - radius)
        & (plotdata["y"] < extents[1, 1] + radius)
    ]

    # plot spots (if any)
    legends_info = []
    if len(plotdata) and (r is not None):
        colors = np.zeros((len(plotdata), 3))
        for i, color in enumerate([r, g, b]):
            if color is None:
                continue
            if color in adata.var.index:
                plotdata["expression"] = sc.get.obs_df(adata, color, layer=layer)
            elif color in adata.obs.columns:
                plotdata["expression"] = adata.obs[color]
            elif "symbol" in adata.var.columns:
                if color in adata.var["symbol"].values:
                    plotdata["expression"] = sc.get.obs_df(
                        adata,
                        adata.var.query(f"symbol == '{color}'").index[0],
                        layer=layer,
                    )
                else:
                    raise ValueError(f"Could not find {color} in var or obs")

            plotdata["expression"] = np.clip(plotdata["expression"], 0, 1)
            if norm == "minmax":
                normalizer = mpl.colors.Normalize(
                    plotdata["expression"].min(), plotdata["expression"].max()
                )
            elif norm == "0max":
                normalizer = mpl.colors.Normalize(0, plotdata["expression"].max())
            elif norm == "0q":
                normalizer = mpl.colors.Normalize(
                    0,
                    np.quantile(plotdata["expression"].values, 0.99),
                    # 0, plotdata["expression"].max()
                )

            colors[:, i] = np.clip(normalizer(plotdata["expression"]), 0, 1)

            legends_info.append(
                {
                    "norm": normalizer,
                    "cmap": mpl.cm.Reds if i == 0 else mpl.cm.Greens if i == 1 else mpl.cm.Blues,
                    "type": "colorbar",
                    "label": color,
                }
            )

        filter = colors.sum(1) > 0
        plotdata_oi = plotdata.loc[filter]
        colors_oi = colors[filter]
        opacity = np.sqrt(np.max(colors_oi, axis = 1))
        colors_oi = colors_oi / colors_oi.max(0)
        colors_oi = np.concatenate([colors_oi, opacity[:, None]], axis=1)

        # Choose colormap
        if len(plotdata) > 0:
            if "rotation" in image:
                rotation = image["rotation"]
            else:
                if "rotation" not in adata.uns["spatial"]:
                    rotation = 0
                else:
                    rotation = adata.uns["spatial"]["rotation"]

            collection = RectangleCollection(
                widths=[radius * scale_spot] * len(plotdata_oi),
                heights=[radius * scale_spot] * len(plotdata_oi),
                angles=[rotation] * len(plotdata_oi),
                facecolors=colors_oi,
                edgecolors="none",
                units="xy",
                offsets=plotdata_oi[["x", "y"]].values,
                transOffset=ax.transData,
                zorder=zorder,
            )
            ax.add_collection(collection)

    if show_locations:
        for ix, (x, y) in plotdata[["x", "y"]].iterrows():
            text = ax.text(x, y, f"{ix}", fontsize=6, color="black", ha="center")
            text.set_path_effects(
                [
                    mpl.patheffects.Stroke(linewidth=4, foreground="white"),
                    mpl.patheffects.Normal(),
                ]
            )

    ax.set_xlim(*extents[0])
    ax.set_ylim(*extents[1][::-1])

    # size bar
    if (extents[0, 1] - extents[0, 0]) > 1000:
        size = 1000
        label = "1000 µm"
    elif (extents[0, 1] - extents[0, 0]) > 100:
        size = 100
        label = "100 µm"
    else:
        size = 10
        label = "10 µm"

    if show_grid:
        ax.grid()
    else:
        ax.set_xticks([extents[0, 0], extents[0, 0] + size])
        ax.set_xticklabels(["", ""])
        ax.set_xticks([extents[0, 0] + size / 2], minor=True)
        ax.set_xticklabels([f"{label}"], minor=True, fontsize=10)
        ax.tick_params(axis="x", which="minor", length=0)

        ax.set_yticks([])

    return fig, legends_info

