import matplotlib

from .avp import PROVIDER_NAMES
from .interpret import load_dfs, process_dfs
from .plots import (
    plot_counts_side_by_side,
    plot_rta_vs_non_rta,
)

if __name__ == "__main__":
    BASE = "./data"
    REGION_LIST = ["ga", "tx", "ny"]

    og_frames = load_dfs(BASE, REGION_LIST)
    frames, meta_frames = process_dfs(og_frames)

    tx = frames["tx"]

    matplotlib.use("pgf")
    matplotlib.rcParams.update(
        {
            "font.family": "serif",
            "text.usetex": True,
            "pgf.texsystem": "pdflatex",
            "pgf.rcfonts": False,
        }
    )

    providers = PROVIDER_NAMES

    RTA_VS_NON_RTA = True
    BAR = False
    BAR_RTA = False
    BAR_NON_RTA = False

    if RTA_VS_NON_RTA:
        rta_vs_non_rta_fig = plot_rta_vs_non_rta(frames, providers, figure_size=(8, 5))
        rta_vs_non_rta_fig.savefig("figures/rta-vs-non-rta.pgf")

    if BAR:
        bar_fig = plot_counts_side_by_side(
            frames, providers, top_k=6, figure_size=(8, 6)
        )
        bar_fig.savefig("figures/bar.pgf")

    if BAR_RTA:
        bar_fig_rta_sites_only = plot_counts_side_by_side(
            frames,
            providers,
            title="Detection counts (sites with RTA meta tag)",
            df_filter=lambda df: df.loc[df["rta"] == 1],
            top_k=6,
            figure_size=(8, 6),
        )
        bar_fig_rta_sites_only.savefig("figures/bar-rta.pgf")

    if BAR_NON_RTA:
        bar_fig_non_rta_sites_only = plot_counts_side_by_side(
            frames,
            providers,
            title="Detection counts (sites without RTA meta tag)",
            df_filter=lambda df: df.loc[df["rta"] == 0],
            top_k=6,
            figure_size=(8, 6),
        )
        bar_fig_non_rta_sites_only.savefig("figures/bar-non-rta.pgf")
