from pathlib import Path

# Keep Code and Dataset as folders inside the same project folder.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "Dataset" / "AgriPredict_AI_Final_Dataset.csv"

PROVINCES = ["Free State", "Mpumalanga", "North West"]

WEATHER_FEATURES = [
    "rain_oct_dec_mm",
    "rain_jan_mm",
    "tmean_oct_jan_c",
]

# Free State is the reference category, so two columns represent province.
FEATURES = WEATHER_FEATURES + ["province_Mpumalanga", "province_North_West"]
TARGET = "yield_t_per_ha"
UNIT = "tonnes per planted hectare"

TRAIN_END_YEAR = 2016
VALIDATION_SEASONS = ["2016/17", "2017/18", "2018/19", "2019/20"]
TEST_SEASONS = ["2020/21", "2021/22", "2022/23", "2023/24"]

