###### Settings.py:



\# Shared settings for the AgriPredict AI prototype



PROVINCES = \["Free State", "Mpumalanga", "North West"]



\# Inputs used by the models and the target they predict

FEATURES = \["rainfall\_mm", "avg\_temp\_c", "harvested\_area\_ha", "prev\_yield"]

TARGET = "yield\_t\_per\_ha"

UNIT = "tonnes per hectare"



\# The last four seasons are held back and never used for training

TEST\_SEASONS = \["2021/22", "2022/23", "2023/24", "2024/25"]

