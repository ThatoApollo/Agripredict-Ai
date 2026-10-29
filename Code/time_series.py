"""Describe annual maize yields. Run: python Code/time_series.py"""
import matplotlib
# Save charts without requiring a display window.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

import settings
from preparation import load_data


def main():
    data = load_data()
    results_dir = settings.PROJECT_DIR / 'Results'
    figures_dir = settings.PROJECT_DIR / 'Documentation' / 'Figures'
    results_dir.mkdir(exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    annual_summaries = []
    for year in sorted(data['year'].unique()):
        year_records = data[data['year'] == year]
        year_yields = year_records[settings.TARGET]
        annual_summaries.append({
            'year': year,
            'records': len(year_records),
            'mean_yield': year_yields.mean(),
            'median_yield': year_yields.median(),
            'standard_deviation': year_yields.std(),
            'minimum_yield': year_yields.min(),
            'maximum_yield': year_yields.max(),
            'zero_yields': int((year_yields == 0).sum()),
            'climate_zones': year_records['cz'].nunique(),
        })

    annual_summary = pd.DataFrame(annual_summaries)
    # Compare each year's mean with the previous recorded year's mean.
    annual_summary['mean_change'] = annual_summary['mean_yield'].diff()
    annual_summary.to_csv(results_dir / 'annual_yield_summary.csv', index=False)

    figure, axes = plt.subplots(figsize=(9, 4))
    axes.plot(annual_summary['year'], annual_summary['mean_yield'], marker='o',
            color='#17643c', label='Mean yield')
    axes.plot(annual_summary['year'], annual_summary['median_yield'], marker='s',
            color='#b76b16', label='Median yield')
    axes.set_ylabel('Yield (tonnes per hectare)')
    axes.set_ylim(bottom=0)
    axes.set_title('Recorded maize yields in the Kenyan sample, 2016–2020')
    axes.set_xlabel('Observation year')
    axes.set_xticks(annual_summary['year'])
    axes.legend(frameon=False)
    axes.grid(axis='y', alpha=0.2)
    axes.set_axisbelow(True)
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    figure.tight_layout()
    figure.savefig(figures_dir / 'annual_yield_trends.png', dpi=160)
    plt.close(figure)
    print(annual_summary.round(3).to_string(index=False))
    print('Saved annual summary and chart. No models fitted or changed.')


if __name__ == '__main__':
    main()
