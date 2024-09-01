import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from alive_progress import alive_bar
from matplotlib.animation import FuncAnimation
from palettable.scientific.sequential import Bamako_3_r

from .cli import BAR_CONFIG


def animate(args, **kwargs):
    plt.style.use("pysagem.plotstyle")

    data = kwargs["data"]
    mean = kwargs["mean"]
    rest_gens = kwargs["rest_gens"]
    add_dist_gens = kwargs["add_dist_gens"]

    mean_nat = mean["native"]
    mean_inv = mean["invasive"]
    landscape = data["quality"]
    natpop = data["natpop"]
    invpop = data["invpop"]

    generations = np.arange(args.gen)

    landscape_cmap = mpl.colors.ListedColormap(Bamako_3_r.mpl_colors)
    landscape_norm = mpl.colors.Normalize(vmin=0, vmax=2)
    mean_norm = mpl.colors.Normalize(vmin=0, vmax=1000)

    fig = plt.figure()
    spec = fig.add_gridspec(2, 3)

    ax0 = fig.add_subplot(spec[0, :])
    ax1 = fig.add_subplot(spec[1, 0])
    ax2 = fig.add_subplot(spec[1, 1])
    ax3 = fig.add_subplot(spec[1, 2])
    axs = fig.axes

    # ax0
    nat_meanplot = ax0.plot(
        generations[0], mean_nat[0], color="tab:blue", animated=True
    )[0]

    inv_meanplot = ax0.plot(
        generations[0], mean_inv[0], color="tab:red", animated=True
    )[0]

    text_gen = ax0.text(
        0.5,
        1.05,
        "",
        ha="center",
        transform=ax0.transAxes,
        animated=True,
    )

    ax0.set_ylabel("Mean across Landscape")
    ax0.set_xlabel("")
    ax0.set_ylim(0, 1150)
    ax0.set_xlim(0, args.gen - 1)
    ax0.set_yticks([0, 250, 500, 750, 1000])

    # ax1
    landscape_plot = ax1.imshow(
        np.reshape(landscape[0], (-1, args.length)),
        cmap=landscape_cmap,
        norm=landscape_norm,
        animated=True,
    )

    ax1.set_title("Landscape Quality")
    ax1.set_ylim(0, args.length - 1)
    ax1.set_xlim(0, args.length - 1)
    landscape_cbar = plt.colorbar(
        mpl.cm.ScalarMappable(norm=landscape_norm, cmap=landscape_cmap),
        ax=ax1,
        location="bottom",
        pad=0.05,
    )
    landscape_cbar.set_ticks([0, 1, 2])

    # ax2
    native_plot = ax2.imshow(
        np.reshape(natpop[0], (-1, args.length)),
        cmap="Blues",
        norm=mean_norm,
        animated=True,
    )

    ax2.set_title("Native Species")
    ax2.set_ylim(0, args.length - 1)
    ax2.set_xlim(0, args.length - 1)
    native_cbar = plt.colorbar(
        mpl.cm.ScalarMappable(norm=mean_norm, cmap="Blues"),
        ax=ax2,
        location="bottom",
        pad=0.05,
    )
    native_cbar.set_ticks([0, 250, 500, 750, 1000])

    # ax3
    invasive_plot = ax3.imshow(
        np.reshape(invpop[0], (-1, args.length)),
        cmap="Reds",
        norm=mean_norm,
        animated=True,
    )

    ax3.set_title("Invasive Species")
    ax3.set_ylim(0, args.length - 1)
    ax3.set_xlim(0, args.length - 1)
    invasive_cbar = plt.colorbar(
        mpl.cm.ScalarMappable(norm=mean_norm, cmap="Reds"),
        ax=ax3,
        location="bottom",
        pad=0.05,
    )
    invasive_cbar.set_ticks([0, 250, 500, 750, 1000])

    plt.setp([axs[1:]], xticks=[], yticks=[])
    for ax in axs[1:]:
        ax.grid(False)

    for cbar in [landscape_cbar, native_cbar, invasive_cbar]:
        cbar.ax.tick_params(axis="x", direction="out")

    def update(frame):
        text_gen.set_text(rf"$t = {frame}$")

        nat_meanplot.set_data(generations[: frame + 1], mean_nat[: frame + 1])
        inv_meanplot.set_data(generations[: frame + 1], mean_inv[: frame + 1])

        landscape_plot.set_data(
            np.reshape(landscape[frame], (-1, args.length)),
        )

        native_plot.set_data(np.reshape(natpop[frame], (-1, args.length)))
        invasive_plot.set_data(np.reshape(invpop[frame], (-1, args.length)))

        if args.rest:
            if np.any(frame == rest_gens):
                ax0.vlines(
                    frame,
                    0,
                    1150,
                    alpha=0.7,
                    animated=True,
                    color="tab:green",
                )

        if args.add_dist:
            if np.any(frame == add_dist_gens):
                ax0.vlines(
                    frame,
                    0,
                    1150,
                    alpha=0.7,
                    color="tab:orange",
                    animated=True,
                )

        return (
            text_gen,
            nat_meanplot,
            inv_meanplot,
            landscape_plot,
            native_plot,
            invasive_plot,
        )

    with alive_bar(**BAR_CONFIG["animation"]):
        ani = FuncAnimation(
            fig=fig,
            func=update,
            frames=args.gen,
            interval=10,
            blit=True,
            repeat=False,
        )
        ani.save(f"{args.name}.mp4", writer="ffmpeg")
