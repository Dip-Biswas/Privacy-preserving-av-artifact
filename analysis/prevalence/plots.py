from typing import Optional, Callable

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import upsetplot
from upsetplot import UpSet

from .avp import COLUMN_NAMES
from .interpret import count_sites_with_at_least_one_provider

plt.style.use("seaborn-v0_8-colorblind")
plt.rcParams.update(
    {
        "font.family": "Latin Modern Roman",
        # "font.family": "serif",
        "font.size": 18,
    }
)


def plot_counts_side_by_side(
    frames: dict[str, pd.DataFrame],
    providers: list[str] | None = None,
    title="Detection counts",
    production: bool = True,
    df_filter: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
    top_k: int = 20,
    figure_size: tuple[int, int] = (15, 8),
) -> plt.Figure:
    """
    Create a bar chart showing counts from each DataFrame side by side for each provider.
    """
    regions = list(frames.keys())

    combined = pd.concat(frames, ignore_index=True)

    if production:
        # drop cols that never appear in any of the original dfs
        combined = filter_insignificant_cols(combined)

        # should hopefully make it use the body font for the pgf versions
        plt.rcParams.update({"font.family": "serif"})

    candidate_cols = list(providers) if providers is not None else COLUMN_NAMES
    present_cols = [c for c in candidate_cols if c in combined.columns]

    # sort cols first based on the counts in `frame[0]`
    df = list(frames.values())[0]  # pick the first one arbitrarily
    if df_filter is not None:
        df = df_filter(df)
    sum_series = df[present_cols].sum().astype(int)
    sum_dict = dict(list(sum_series.items()))
    present_cols = sorted(present_cols, key=lambda p: sum_dict[p], reverse=True)

    if production:
        present_cols = present_cols[:top_k]  # top `top_k` based on `frames[0]`

    counts_data = {}
    for i, df in enumerate(frames.values()):
        if df_filter is not None:
            df = df_filter(df)

        sum_series = df[present_cols].sum().astype(int)
        sum_dict = dict(list(sum_series.items()))

        counts_data[regions[i]] = [sum_dict[p] for p in present_cols]

    fig, ax = plt.subplots(figsize=figure_size)

    x = range(len(present_cols))
    width = 0.8 / len(frames)

    for i, (state, provider_counts) in enumerate(counts_data.items()):
        offset = (i - len(frames) / 2 + 0.5) * width
        ax.bar(
            [xi + offset for xi in x],
            provider_counts,
            width,
            label=state.upper(),
            alpha=0.8,
        )

    ax.set_ylabel("Number of websites")
    ax.set_xlabel("Provider")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(present_cols, rotation=45, ha="right")
    ax.legend()

    fig.tight_layout()
    return fig


def plot_rta_vs_non_rta(
    frames: dict[str, pd.DataFrame],
    providers: list[str] | None = None,
    title="Detection counts across states",
    production: bool = True,
    df_filter: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
    figure_size: tuple[int, int] = (15, 8),
) -> plt.Figure:
    regions = list(frames.keys())

    if production:
        # should hopefully make it use the body font for the pgf versions
        plt.rcParams.update({"font.family": "serif"})

    def have_rta(df):
        return df["rta"] == 1

    def do_not_have_rta(df):
        return df["rta"] == 0

    rta_counts = {
        s: count_sites_with_at_least_one_provider(df, condition=have_rta)
        for s, df in frames.items()
    }
    non_rta_counts = {
        s: count_sites_with_at_least_one_provider(df, condition=do_not_have_rta)
        for s, df in frames.items()
    }

    fig, (ax_top, ax_bottom) = plt.subplots(
        2, 1, sharey=True, figsize=figure_size, gridspec_kw={"hspace": 0.05}
    )

    bar_height = 0.1

    assert rta_counts.keys() == non_rta_counts.keys()

    colors = colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    rta_positions = [i * -bar_height for i in range(len(regions))]
    # non_rta_positions = [
    #    -bar_height + (len(regions) + i) * -bar_height for i in range(len(regions))
    # ]

    ax_top.barh(
        rta_positions,
        rta_counts.values(),
        height=bar_height,
        color=colors,
        alpha=0.8,
        label=[s.upper() for s in rta_counts.keys()],
    )
    ax_top.set_title("Sites with RTA")
    ax_top.xaxis.set_label_position("bottom")
    ax_top.xaxis.tick_top()
    ax_top.set_xlabel("Number of websites")

    ax_bottom.barh(
        rta_positions,
        non_rta_counts.values(),
        height=bar_height,
        color=colors,
        alpha=0.8,
        # alpha=0.5,
    )

    ax_bottom.set_title("Sites without RTA")
    ax_bottom.xaxis.set_label_position("top")
    ax_bottom.xaxis.tick_bottom()
    ax_bottom.set_xlabel("Number of websites")

    ax_top.set_yticks(rta_positions)
    ax_top.set_yticklabels([r.upper() for r in regions])

    ax_bottom.set_yticks(rta_positions)
    ax_bottom.set_yticklabels([r.upper() for r in regions])

    fig.tight_layout()
    return fig


def providers_cdf(
    frames: dict[str, pd.DataFrame],
    providers: list[str],
    production: bool = True,
    preprocessing: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
) -> plt.Figure:
    regions = list(frames.keys())

    num_plots = len(regions)
    fig, axs = plt.subplots(1, num_plots, figsize=(90, 90 / num_plots))

    for ax, (region, df) in zip(axs, frames.items()):
        if production:
            df = filter_insignificant_cols(df)

        if preprocessing is not None:
            df = preprocessing(df)

        names = []
        sums = []

        for col in providers:
            if col in df.columns:
                names.append(col)
                sums.append(df[col].sum())

        sums = np.array(sums)

        sums_names = sorted(zip(sums, names), key=lambda t: t[0], reverse=True)
        sums = np.array([cs for cs, _ in sums_names])
        names = [n for _, n in sums_names]

        freqs = sums / sums.sum()
        cumsums = np.cumsum(freqs)

        ax.set_title(region)
        ax.tick_params(axis="x", labelrotation=45)
        ax.step(names, cumsums)

    return fig


def upset_plot(frame: pd.DataFrame, providers: list[str]) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.axis("off")

    upset = UpSet(
        upsetplot.from_indicators(
            lambda df: df[providers].astype(bool, copy=False), data=frame
        ),
        orientation="vertical",
        min_degree=2,
        min_subset_size=5,
        show_counts=True,
    )
    upset.plot(fig)

    return fig


def filter_insignificant_cols(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:, df.any()]
