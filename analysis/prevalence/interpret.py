import os
import json
from functools import reduce
from typing import Callable, Optional
from collections import Counter

import pandas as pd

import prevalence.avp as avp
from .avp import PROVIDER_NAMES


def load_dfs(base: str, region_list: list[str]) -> dict[str, pd.DataFrame]:
    csv_paths = {region: os.path.join(base, f"{region}.csv") for region in region_list}
    return {region: pd.read_csv(p, index_col=0) for region, p in csv_paths.items()}


def process_dfs(
    frames: dict[str, pd.DataFrame],
) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    site_name_sets = [set(df["name"]) for df in frames.values()]
    shared_site_names = reduce(set.intersection, site_name_sets)

    processed_frames = {}
    meta_frames = {}
    for region, df in frames.items():
        pdf = df

        # exclude controls
        pdf = pdf[~pdf["name"].str.startswith("_")]

        # subset to sites shared across all frames
        pdf = pdf[pdf["name"].isin(shared_site_names)]

        # some "meta_info" cols are read as NaN for some reason...
        pdf["meta_info"] = pdf["meta_info"].fillna("{}")

        meta_df = parse_meta_infos(pdf)

        # remove patterns with high false positive rates
        unyoti = list(
            meta_df[meta_df["Yoti"] == '["subdomain_or_path_catchall"]']["name"]
        )
        pdf.loc[pdf["name"].isin(unyoti), "Yoti"] = 0

        processed_frames[region] = pdf
        meta_frames[region] = meta_df

    assert len(set([len(df) for df in processed_frames])) == 1

    return processed_frames, meta_frames


def parse_meta_infos(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame[["name", "meta_info"]]

    def parse_meta_info(json_blob: str):
        m: dict[str, list[str]] = json.loads(json_blob)
        return {k: json.dumps(v) for k, v in m.items()}

    expanded = frame["meta_info"].apply(parse_meta_info).apply(pd.Series)

    frame = pd.concat([frame, expanded], axis=1)
    frame.fillna("[]", inplace=True)  # some things are NaN for some reason

    return frame


def count_sites_with_at_least_one_provider(
    df, condition: Optional[Callable[tuple[pd.DataFrame], pd.Series]] = None
) -> int:
    avp_rows_provider_cols = (
        df.loc[condition, PROVIDER_NAMES] == 1
        if condition is not None
        else df[PROVIDER_NAMES] == 1
    )

    return avp_rows_provider_cols.sum(axis=1).astype(bool).sum()


def pattern_stats(df: pd.DataFrame, provider: avp.ADetector) -> Counter[str]:
    df_provider_with_meta = df[df[provider.name()] == 1][["name", "meta_info"]]
    df_provider_with_detectors = df_provider_with_meta["meta_info"].apply(
        lambda s: json.loads(s)[provider.name()]
    )

    # print("total count for provider:", len(df_provider_with_detectors))

    counter = Counter()

    for detector_list in df_provider_with_detectors:
        counter.update(detector_list)

    return counter


def sites_for_provider(df: pd.DataFrame, provider: avp.ADetector) -> set[str]:
    provider_sites = df[df[provider.name()] == 1]["name"]
    return set(provider_sites)


def sites_for_pattern_in_provider(
    df: pd.DataFrame, provider: avp.ADetector, pattern: str
) -> set[str]:
    df_provider_metas = df[df[provider.name()] == 1][["name", "meta_info"]]
    df_provider_metas["meta_info"] = df_provider_metas["meta_info"].apply(
        lambda s: json.loads(s)[provider.name()]
    )
    df_pattern_of_provider_df = df_provider_metas[
        df_provider_metas["meta_info"].apply(lambda ds: pattern in ds)
    ]

    return set(df_pattern_of_provider_df["name"])


def top_k_providers_cover_x_percent_sites(
    df: pd.DataFrame, k: int = 20, bottom: bool = False
) -> tuple[float, int, list[str]]:
    sum_series = df[PROVIDER_NAMES].sum().astype(int)
    sum_dict = dict(list(sum_series.items()))

    present_cols = sorted(PROVIDER_NAMES, key=lambda p: sum_dict[p], reverse=True)

    if bottom:
        present_cols = present_cols[-k:]
    else:
        present_cols = present_cols[:k]

    count_top_k = (df[present_cols] == 1).sum(axis=1).astype(bool).sum()
    total_count = (df[PROVIDER_NAMES] == 1).sum(axis=1).astype(bool).sum()

    return float(count_top_k / total_count * 100), int(count_top_k), present_cols


def sites_with_avp(df: pd.DataFrame) -> set[str]:
    return set(df[(df[PROVIDER_NAMES].sum(axis=1).astype(bool))]["name"])


def rta_sites_with_avp(df: pd.DataFrame) -> set[str]:
    return set(
        df[(df["rta"] == 1) & (df[PROVIDER_NAMES].sum(axis=1).astype(bool))]["name"]
    )


def rta_sites_with_provider(df: pd.DataFrame, provider: avp.ADetector) -> list[str]:
    rta_sites = list(df.loc[df["rta"] == 1, "name"])
    return list(
        df.loc[(df["name"].isin(rta_sites)) & (df[provider.name()] == 1), "name"]
    )


def non_rta_sites_with_provider(df: pd.DataFrame, provider: avp.ADetector) -> list[str]:
    non_rta_sites = list(df.loc[df["rta"] == 0, "name"])
    return list(
        df.loc[(df["name"].isin(non_rta_sites)) & (df[provider.name()] == 1), "name"]
    )


def avp_site_ranks(df: pd.DataFrame, top_list: pd.DataFrame) -> pd.DataFrame:
    sites_with_avp = df.loc[df[PROVIDER_NAMES].sum(axis=1).astype(bool), "name"]
    sites_with_avp_list = list(sites_with_avp)

    return top_list.loc[top_list["origin"].isin(sites_with_avp_list)]


def included_sites_with_ranks(df: pd.DataFrame, top_list: pd.DataFrame) -> pd.DataFrame:
    sites = df["name"]
    sites_list = list(sites)

    return top_list.loc[top_list["origin"].isin(sites_list)]


def rta_sites(df: pd.DataFrame) -> set[str]:
    return set(df.loc[df["rta"] == 1, "name"])


def have_rta(df: pd.DataFrame) -> pd.Series:
    return df["rta"] == 1


def non_rta_sites_with_avp(df: pd.DataFrame) -> set[str]:
    return set(
        df[(df["rta"] == 0) & (df[PROVIDER_NAMES].sum(axis=1).astype(bool))]["name"]
    )
