"""Describe historical maize yield patterns without using the final test seasons."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import settings
from preparation import train, validation


def main():
    results = settings.PROJECT_DIR / "Results"
    figures = settings.PROJECT_DIR / "Documentation" / "Figures"
    results.mkdir(exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    # The final test period is excluded from this exploratory analysis.
    history = pd.concat([train, validation], ignore_index=True)
    history = history.sort_values(["province", "harvest_year"]).reset_index(drop=True)
    for province in settings.PROVINCES:
        years = history.loc[history["province"] == province, "harvest_year"]
        if len(years) < 3 or not np.all(np.diff(years) == 1):
            raise ValueError("Each province needs at least three consecutive seasons.")

    grouped = history.groupby("province")[settings.TARGET]
    # Includes the current observed season: smoothing, not a future prediction.
    history["moving_average_3_seasons"] = grouped.transform(
        lambda values: values.rolling(3, min_periods=3).mean()
    )
    history["yield_change"] = grouped.diff()
    history["yield_change_pct"] = grouped.pct_change(fill_method=None) * 100
    history[["province", "season", "harvest_year", settings.TARGET,
             "moving_average_3_seasons", "yield_change", "yield_change_pct"]].to_csv(
        results / "time_series_values.csv", index=False
    )

    summaries = []
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True, sharey=True)
    for ax, province in zip(axes, settings.PROVINCES):
        rows = history[history["province"] == province]
        low = rows.loc[rows[settings.TARGET].idxmin()]
        high = rows.loc[rows[settings.TARGET].idxmax()]
        summaries.append({
            "province": province, "seasons": len(rows),
            "mean_yield": rows[settings.TARGET].mean(),
            "minimum_yield": low[settings.TARGET], "minimum_season": low["season"],
            "maximum_yield": high[settings.TARGET], "maximum_season": high["season"],
            "first_3_seasons_mean": rows.head(3)[settings.TARGET].mean(),
            "last_3_seasons_mean": rows.tail(3)[settings.TARGET].mean(),
        })
        ax.axvspan(settings.TRAIN_END_YEAR + 0.5,
                   history["harvest_year"].max() + 0.5, color="#e6edf3",
                   label="Validation period")
        ax.plot(rows["harvest_year"], rows[settings.TARGET], color="#246b45",
                marker="o", markersize=4, linewidth=1.5, label="Observed yield")
        ax.plot(rows["harvest_year"], rows["moving_average_3_seasons"],
                color="#bd6b18", linewidth=2, label="3-season moving average")
        ax.set_title(province, loc="left", fontsize=12)
        ax.set_ylabel("t / planted ha")
        ax.grid(axis="y", alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)
    ticks = sorted(history["harvest_year"].unique())[::3]
    axes[-1].set_xticks(ticks, [f"{year-1}/{str(year)[-2:]}" for year in ticks])
    axes[-1].set_xlabel("Agricultural season")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
    fig.suptitle("Provincial maize yield trends, 2000/01–2019/20", fontsize=15)
    fig.tight_layout(rect=(0, 0.045, 1, 0.96))
    fig.savefig(figures / "time_series_yield_trends.png", dpi=160)
    plt.close(fig)

    summary = pd.DataFrame(summaries)
    summary.to_csv(results / "time_series_summary.csv", index=False)
    report = [
        "# Time Series Analysis", "",
        "This analysis examines maize yields for the three provinces from 2000/01 to "
        "2019/20. It uses 60 training and validation records across 20 seasons. "
        "The final test seasons, 2020/21–2023/24, are excluded.", "",
        "## Historical Patterns", "",
        "| Province | Average yield | Lowest yield (season) | Highest yield (season) |",
        "| --- | --- | --- | --- |",
    ]
    for row in summaries:
        report.append(f"| {row['province']} | {row['mean_yield']:.2f} | "
                      f"{row['minimum_yield']:.2f} ({row['minimum_season']}) | "
                      f"{row['maximum_yield']:.2f} ({row['maximum_season']}) |")
    report += ["", "All yields are in tonnes per planted hectare.", "",
               "![Provincial yield trends](Figures/time_series_yield_trends.png)", "",
               "The three-season moving average smooths short-term changes to make "
               "the longer-term pattern easier to see. Each average includes the "
               "current season and the previous two seasons, so it is a description "
               "of observed yields rather than a forecast.", ""]
    for row in summaries:
        report.append(f"- {row['province']}: the average was "
                      f"{row['first_3_seasons_mean']:.2f} t/ha in the first three seasons "
                      f"(2000/01–2002/03), compared with {row['last_3_seasons_mean']:.2f} "
                      "t/ha in the last three (2017/18–2019/20).")
    report += ["", "## What This Means", "",
               "Yields fluctuate between seasons. Comparing early and later averages "
               "helps describe change, but does not establish a steady trend or explain "
               "its causes. These patterns support considering time-related features "
               "in later modelling; they do not prove those features will improve predictions.", "",
               "The records are annual, with one observation per province per season. "
               "They cannot show monthly planting or growing-season patterns. Provincial "
               "averages also hide differences between individual farms.", "",
               "No new prediction model was fitted in this task, and the earlier model "
               "scores remain unchanged. Future model development needs a separate "
               "chronological evaluation plan because the original test results have "
               "already been inspected.", "",
               "## Run the Analysis", "", "From the repository root:", "",
               "```bash", "python -m pip install matplotlib", "python Code/time_series.py", "```", "",
               "The script creates the chart in `Documentation/Figures/` and the "
               "summary and season-by-season values in `Results/`.", ""]
    (settings.PROJECT_DIR / "Documentation" / "time_series_analysis.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False, float_format=lambda value: f"{value:.3f}"))
    print("Saved time series chart, two CSV files and documentation.")


if __name__ == "__main__":
    main()
