"""
Generate a side-by-side bar chart of the top AV providers for UK and Australia.
Run from the analysis/ directory:

    uv run python3 prevalence/provider_barchart.py

Output: data/provider_barchart.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

from provider_counts import combine, PROVIDER_KEYWORDS

DATA = Path(__file__).parent.parent / "data"
OUT  = DATA / "provider_barchart.png"

# Providers to exclude from the chart
EXCLUDE = {"ID.me", "Sumsub"}

# Explicit top-5 ordering per jurisdiction (edit as needed)
UK_TOP5 = ["AgeVerif", "Yoti", "VerifyMyAge", "AgeGo", "GoCam"]
AU_TOP5 = ["AgeGo", "Yoti", "AgeVerif", "GoCam", "Incode"]


def get_counts(csv_path, ods_path, providers):
    domain_providers = combine(csv_path, ods_path)
    total = len(domain_providers)
    counts = {}
    for ps in domain_providers.values():
        for p in ps:
            counts[p] = counts.get(p, 0) + 1
    return {p: counts.get(p, 0) for p in providers}, total

"""
def annotate_bars(ax, bars):
    for bar in bars:
        h = bar.get_height()
        ax.annotate(
            f"{h:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )
"""

def annotate_bars(ax, bars):
    for bar in bars:
        h = bar.get_height()
        ax.annotate(
            f"{h}",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

if __name__ == "__main__":
    uk_counts, uk_total = get_counts(
        DATA / "results10k-lon-v2.csv",
        DATA / "manual check.ods",
        UK_TOP5,
    )
    au_counts, au_total = get_counts(
        DATA / "results10k-aus-v2.csv",
        DATA / "manual check aus.ods",
        AU_TOP5,
    )

    #uk_vals = [uk_counts[p] / uk_total * 100 for p in UK_TOP5]
    #au_vals = [au_counts[p] / au_total * 100 for p in AU_TOP5]
    uk_vals = [uk_counts[p] for p in UK_TOP5]
    au_vals = [au_counts[p] for p in AU_TOP5]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    fig.suptitle("Most Common Age Verification Providers (top 10k sites)", fontsize=13)

    bars1 = ax1.bar(UK_TOP5, uk_vals, color="#2196F3", zorder=3)
    ax1.set_title("United Kingdom", fontsize=12)
    ax1.set_ylabel("Number of confirmed AV sites", fontsize=10)
    ax1.yaxis.grid(True, linestyle="--", alpha=0.7, zorder=0)
    ax1.set_axisbelow(True)
    ax1.set_ylim(0, max(uk_vals) * 1.2)
    annotate_bars(ax1, bars1)

    bars2 = ax2.bar(AU_TOP5, au_vals, color="#FF9800", zorder=3)
    ax2.set_title("Australia", fontsize=12)
    ax2.set_ylabel("Number of confirmed AV sites", fontsize=10)
    ax2.yaxis.grid(True, linestyle="--", alpha=0.7, zorder=0)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, max(au_vals) * 1.2)
    annotate_bars(ax2, bars2)

    plt.tight_layout()
    plt.savefig(OUT, dpi=150, bbox_inches="tight")
    print(f"Saved to {OUT}")
