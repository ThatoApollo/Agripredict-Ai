"""Reconstruct the prepared CSV from the published One Acre Fund dataset.

Run from the project root: python Code/prepare_dataset.py
Source: https://zenodo.org/records/11122388 (version 2)
This is a reconstructed script, not the unavailable original script.
"""
import pandas as pd

import settings
from preparation import load_data

RAW_FILE = settings.PROJECT_DIR / 'Dataset' / 'One_Acre_Fund_MEL_maize_survey_data_2016-2022.csv'


def prepare_dataset(raw_file=RAW_FILE):
    data = pd.read_csv(raw_file)

    # The header is CSV row 1, so the first observation is row 2.
    data['source_row'] = data.index + 2
    data = data[data['country'] == 'kenya'].copy()

    selected_columns = ['source_row', 'year', 'country', 'season', 'cz']
    selected_columns += settings.FEATURES + ['yield_kg_ha']
    data = data[selected_columns].copy()

    hybrid_values = data['hybrid'].astype('string').str.lower()
    if not hybrid_values.isin(['true', 'false']).all():
        raise ValueError('Hybrid status must be True or False.')
    data['hybrid'] = hybrid_values.map({'true': True, 'false': False}).astype(bool)

    data['yield_t_per_ha'] = data['yield_kg_ha'] / 1000
    data['split'] = data['year'].map({
        2016: 'Training',
        2017: 'Training',
        2018: 'Training',
        2019: 'Validation',
        2020: 'Test',
    })
    data = data.sort_values(['year', 'source_row']).reset_index(drop=True)

    # Keep zero yields and missing soil values. Model pipelines impute soil.
    return data


def main():
    data = prepare_dataset()

    # Validate before replacing the prepared dataset.
    temporary_file = settings.DATA_FILE.with_suffix('.temporary.csv')
    try:
        data.to_csv(temporary_file, index=False)
        load_data(temporary_file)
        temporary_file.replace(settings.DATA_FILE)
    finally:
        temporary_file.unlink(missing_ok=True)

    print(f'Saved {len(data):,} Kenyan observations to {settings.DATA_FILE}')
    print(data.groupby(['year', 'split']).size().to_string())


if __name__ == '__main__':
    main()
