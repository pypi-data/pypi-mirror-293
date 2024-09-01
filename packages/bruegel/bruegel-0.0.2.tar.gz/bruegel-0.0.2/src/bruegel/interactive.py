import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import pathlib

import anywidget
import traitlets
from traittypes import Array

class SpatialWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "index.js"
    _css = pathlib.Path(__file__).parent / "index.css"
    value = traitlets.Int(0).tag(sync=True)
    image = traitlets.Unicode().tag(sync=True)
    extent = traitlets.List().tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_image(self, image):
        self.image = image



def plot_spatial(
    adata: sc.AnnData,
    widget: SpatialWidget,
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
    legend_ax=None,
    show_grid=False,
    step_grid=100,
    scale_spot=1,
    zorder=0,
    norm="minmax",
    spot_to_pixel=None,
    layer=None,
    fig_width=None,
    fig_height=None,
    transparent_colors = ("#FFFFFF", ),
    alpha_spot = 1,
):
    """
    Parameters
    ----------
    adata
        Anndata object containing spatial information.
    widget
        Widget to display the spatial plot.
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
    transparent_colors
        Colors to make transparent.
    """
    image = adata.uns["spatial"]["images"][image_id]

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
                raise NotImplementedError("Reading tiff files is not yet implemented")
            else:
                raise ValueError("image should be a numpy array or tiffslide.TiffSlide")

        if img.shape[0] == 0 or img.shape[1] == 0:
            print(extents_image)
            raise ValueError("No image data found in the specified area")

        # base 64 encode
        img = (img * 255).astype(np.uint8)
        import base64
        import io

        imgbase64 = io.BytesIO()
        mpl.image.imsave(imgbase64, img, format="png")
        widget.load_image(base64.b64encode(imgbase64.getvalue()).decode("utf-8"))

    # plotdata = pd.concat(
    #     [
    #         pd.DataFrame(
    #             adata.obsm[spot_to_pixel] * image["scale"] * image["microns_per_pixel"],
    #             columns=["x", "y"],
    #         ),
    #         pd.DataFrame(adata.obsm["spatial"], columns=["X", "Y"]),
    #     ],
    #     axis=1,
    # )
    # plotdata.index = adata.obs.index

    # radius = adata.uns["spatial"]["scalefactors"]["bin_size_um"]

    # plotdata_all = plotdata

    # extent_filter = (
    #     (plotdata["x"] > extents[0, 0] - radius)
    #     & (plotdata["x"] < extents[0, 1] + radius)
    #     & (plotdata["y"] > extents[1, 0] - radius)
    #     & (plotdata["y"] < extents[1, 1] + radius)
    # )

    # # plot spots (if any)
    # if len(plotdata) and (color is not None):
    #     plotdata = plotdata_all.loc[extent_filter].copy()

    #     # get expression values
    #     plotdata["expression"] = get_value(adata[extent_filter], color, layer=layer)

    #     # type of column
    #     if plotdata["expression"].dtype.name == "category":
    #         plotdata["expression"] = plotdata["expression"].cat.codes
    #     elif plotdata["expression"].dtype.name == "bool":
    #         plotdata["expression"] = plotdata["expression"].astype(int)

    #     if norm == "minmax":
    #         norm = mpl.colors.Normalize(
    #             plotdata["expression"].min(), plotdata["expression"].max()
    #         )
    #     elif norm == "0max":
    #         norm = mpl.colors.Normalize(0, plotdata["expression"].max())
    #     elif norm == "0q":
    #         norm = mpl.colors.Normalize(
    #             0, np.quantile(plotdata["expression"].values, 0.999)
    #         )
    #     elif norm is None:
    #         norm = mpl.colors.Normalize()
    #     else:
    #         norm = norm

    #     # remove spots with 0 value
    #     plotdata = plotdata.loc[plotdata["expression"] > 0]

    #     # Choose colormap
    #     if len(plotdata) > 0:

    #         # determine rotation
    #         if "rotation" in image:
    #             rotation = image["rotation"]
    #         else:
    #             if "rotation" not in adata.uns["spatial"]:
    #                 rotation = 0
    #             else:
    #                 rotation = adata.uns["spatial"]["rotation"]

    #         # TODO: if not rotated, we could use matshow
    #         collection = RectangleCollection(
    #             widths=[radius * scale_spot * 1.01] * len(plotdata),
    #             heights=[radius * scale_spot * 1.01] * len(plotdata),
    #             angles=[rotation] * len(plotdata),
    #             facecolors=cmap(norm(plotdata["expression"])),
    #             edgecolors="none",
    #             units="xy",
    #             offsets=plotdata[["x", "y"]].values,
    #             transOffset=ax.transData,
    #             zorder=zorder,
    #             alpha = alpha_spot,
    #         )
    #         ax.add_collection(collection)

    # if show_locations:
    #     for ix, (x, y) in plotdata[["x", "y"]].iterrows():
    #         text = ax.text(x, y, f"{ix}", fontsize=6, color="black", ha="center")
    #         text.set_path_effects(
    #             [
    #                 mpl.patheffects.Stroke(linewidth=4, foreground="white"),
    #                 mpl.patheffects.Normal(),
    #             ]
    #         )

    # ax.set_xlim(*extents[0])
    # ax.set_ylim(*extents[1][::-1])

    # # size bar
    # if (extents[0, 1] - extents[0, 0]) > 1000:
    #     size = 1000
    #     label = "1000 µm"
    # elif (extents[0, 1] - extents[0, 0]) > 100:
    #     size = 100
    #     label = "100 µm"
    # else:
    #     size = 10
    #     label = "10 µm"

    # if show_grid:
    #     ax.grid()
    #     ax.set_xticks(np.arange(*(np.array(ax.get_xlim()) // step_grid * step_grid), step_grid))
    #     ax.tick_params(axis="x", which="major", labelrotation=90)
    #     ax.set_yticks(np.arange(*(np.array(ax.get_ylim()[::-1]) // step_grid * step_grid), step_grid))
    #     ax.tick_params(axis="y", which="major", labelrotation=0)
    # else:
    #     ax.set_xticks([extents[0, 0], extents[0, 0] + size])
    #     ax.set_xticklabels(["", ""])
    #     ax.set_xticks([extents[0, 0] + size / 2], minor=True)
    #     ax.set_xticklabels([f"{label}"], minor=True, fontsize=10)
    #     ax.tick_params(axis="x", which="minor", length=0)

    #     ax.set_yticks([])

    # if fig is not None:
    #     return fig
