"""Reconstruct the prepared dataset from the published source.

Source: https://zenodo.org/records/11122388 (version 2)
This reconstructs the preparation process; it is not the original script.
"""
import pandas as pd

import settings
from preparation import load_data

RAW_FILE = (
    settings.PROJECT_DIR
    / 'Dataset'
    / 'One_Acre_Fund_MEL_maize_survey_data_2016-2022.csv'
)

def prepare_dataset(raw_file=RAW_FILE):
    data = pd.read_csv(raw_file)

    # Preserve original CSV row numbers, including the header.
    data['source_row'] = data.index + 2

    columns = ['source_row', 'year', 'country', 'season', 'cz']
    columns += settings.FEATURES + ['yield_kg_ha']
    data = data.loc[data['country'].eq('kenya'), columns].copy()

    hybrid = data['hybrid'].astype('string').str.lower()
    if not hybrid.isin(['true', 'false']).all():
        raise ValueError('Hybrid status must be True or False.')
    data['hybrid'] = hybrid.map({'true': True, 'false': False}).astype(bool)

    data['yield_t_per_ha'] = data['yield_kg_ha'] / 1000
    data['split'] = data['year'].map({
        2016: 'Training',
        2017: 'Training',
        2018: 'Training',
        2019: 'Validation',
        2020: 'Test',
    })

    # Keep zero yields and missing soil values for pipeline imputation.
    return data.sort_values(['year', 'source_row']).reset_index(drop=True)

def main():
    data = prepare_dataset()
    temporary_file = settings.DATA_FILE.with_suffix('.temporary.csv')

    # Replace the prepared dataset only after validation succeeds.
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
