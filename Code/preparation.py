"""Load, validate and split data; provide unfitted model preprocessing."""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import settings


def load_data(path=settings.DATA_FILE):
    data = pd.read_csv(path)
    required_columns = ['source_row', 'year', 'country', 'season', 'split', settings.TARGET]
    required_columns += settings.FEATURES
    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f'Missing column: {column}')
    if data.empty:
        raise ValueError('The dataset is empty.')
    if data[['source_row', 'year', 'country', 'season', 'split']].isna().any().any():
        raise ValueError('Required metadata contains missing values.')
    if not data['country'].eq('kenya').all():
        raise ValueError('Only Kenyan records are supported.')
    if not data['season'].eq('first season').all():
        raise ValueError('Unexpected growing season.')
    if data['source_row'].duplicated().any():
        raise ValueError('Source-row references must be unique.')
    if not data['year'].isin(settings.TRAIN_YEARS + [settings.VALIDATION_YEAR, settings.TEST_YEAR]).all():
        raise ValueError('Unexpected observation year.')
    # Accept only explicit boolean values, never truthiness of arbitrary strings.
    hybrid_values = data['hybrid'].astype('string').str.lower()
    if not hybrid_values.isin(['true', 'false']).all():
        raise ValueError('Hybrid status must be True or False.')
    data['hybrid'] = hybrid_values.map({'true': 1, 'false': 0}).astype(int)
    numeric_columns = settings.FEATURES + [settings.TARGET]
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='raise')
    if np.isinf(data[numeric_columns].to_numpy()).any():
        raise ValueError('Infinite numeric values are not supported.')
    non_missing_columns = ['lat', 'lon', 'elev', 'hybrid', settings.TARGET]
    if data[non_missing_columns].isna().any().any():
        raise ValueError('Missing values are permitted only in soil inputs.')
    if data[settings.TARGET].lt(0).any():
        raise ValueError('Yield cannot be negative.')
    if not data['lat'].between(-90, 90).all() or not data['lon'].between(-180, 180).all():
        raise ValueError('Invalid geographic coordinates.')
    for column, minimum, maximum in [('soil_clay', 0, 100), ('soil_pH', 0, 14)]:
        values = data[column].dropna()
        if not values.between(minimum, maximum).all():
            raise ValueError(f'Invalid values in {column}.')
    if data['soil_orgC'].dropna().lt(0).any():
        raise ValueError('Soil organic carbon cannot be negative.')
    expected_splits = data['year'].map({
        2016: 'Training', 2017: 'Training', 2018: 'Training',
        2019: 'Validation', 2020: 'Test'
    })
    if not data['split'].eq(expected_splits).all():
        raise ValueError('Split labels do not match observation years.')
    return data.sort_values(['year', 'source_row']).reset_index(drop=True)


def split_data(data):
    train = data[data['year'].isin(settings.TRAIN_YEARS)].copy()
    validation = data[data['year'] == settings.VALIDATION_YEAR].copy()
    test = data[data['year'] == settings.TEST_YEAR].copy()

    if train.empty or validation.empty or test.empty:
        raise ValueError('Each evaluation period must contain records.')
    for column in settings.SOIL_FEATURES:
        if train[column].isna().all():
            raise ValueError(f'No observed training values in {column}.')
    return train, validation, test


def model_data(rows):
    # Explicit selection prevents metadata and yield columns entering the model.
    features = rows[settings.FEATURES].copy()
    target = rows[settings.TARGET].copy()
    return features, target


def make_preprocessor(scale=False):
    # Create a fresh, unfitted transformer for each model or evaluation fold.
    # Fit on training features only; transform validation/test without refitting.
    imputer = SimpleImputer(strategy='median')
    if scale:
        return make_pipeline(imputer, StandardScaler())
    return imputer


def main():
    data = load_data()
    train, validation, test = split_data(data)
    training_features, _ = model_data(train)
    preprocessor = make_preprocessor()
    preprocessor.fit(training_features)
    for name, rows in [('Training', train), ('Validation', validation), ('Test', test)]:
        features, _ = model_data(rows)
        prepared_features = preprocessor.transform(features)
        if not np.isfinite(prepared_features).all():
            raise ValueError(f'Non-finite prepared inputs in {name}.')
        print(f'{name}: {len(rows)} records, {int(features.isna().sum().sum())} missing input cells before imputation')
    print('Training soil medians:')
    medians = pd.Series(preprocessor.statistics_, index=settings.FEATURES)
    for column in settings.SOIL_FEATURES:
        print(f'  {column}: {medians[column]}')
    print('Inputs:', ', '.join(settings.FEATURES))
    print('Target unit:', settings.UNIT)
    print('Checks complete. No models trained and no dataset values overwritten.')


if __name__ == '__main__':
    main()
