from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / 'Dataset' / 'AgriPredict_Final_Dataset.csv'
# Keep this order: the dashboard and model uses it for prediction inputs.
FEATURES = ['lat', 'lon', 'elev', 'soil_clay', 'soil_pH', 'soil_orgC', 'hybrid']
SOIL_FEATURES = ['soil_clay', 'soil_pH', 'soil_orgC']
TARGET = 'yield_t_per_ha'
UNIT = 'tonnes per hectare'
TRAIN_YEARS = [2016, 2017, 2018]
VALIDATION_YEAR = 2019
TEST_YEAR = 2020
