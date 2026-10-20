import numpy as np
import pandas as pd

import settings


# Load the final dataset: one record per province and agricultural season.
df = pd.read_csv(settings.DATA_FILE)

required = ["province", "season", "harvest_year", "yield_t_per_planted_ha"]
required += settings.WEATHER_FEATURES
missing_columns = set(required) - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing dataset columns: {sorted(missing_columns)}")

# Report problems rather than silently deleting historical records.
if df[required].isna().any().any():
    raise ValueError("The dataset has missing required values.")
if df.duplicated(["province", "season"]).any():
    raise ValueError("The dataset has duplicate province-season records.")
if not df["province"].isin(settings.PROVINCES).all():
    raise ValueError("The dataset contains an unsupported province.")

numeric_columns = settings.WEATHER_FEATURES + [
    "harvest_year", "yield_t_per_planted_ha"
]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="raise")
if not np.isfinite(df[numeric_columns].to_numpy()).all():
    raise ValueError("Numeric values must be finite.")

df = df.sort_values(["province", "harvest_year"]).reset_index(drop=True)

# Yield is already calculated from production divided by planted area.
# Use the prototype's target name without rounding the training values.
df[settings.TARGET] = df["yield_t_per_planted_ha"]

# Fixed province categories keep the same numeric columns in every split.
province = pd.Categorical(df["province"], categories=settings.PROVINCES)
province_columns = pd.get_dummies(
    province, prefix="province", drop_first=True, dtype=int
)
province_columns.columns = province_columns.columns.str.replace(" ", "_")
df = pd.concat([df, province_columns], axis=1)

# Keep all provinces from each season together, in chronological order.
train = df[df["harvest_year"] <= settings.TRAIN_END_YEAR].copy()
validation = df[df["season"].isin(settings.VALIDATION_SEASONS)].copy()
test = df[df["season"].isin(settings.TEST_SEASONS)].copy()
if len(train) + len(validation) + len(test) != len(df):
    raise ValueError("Some records do not match the agreed evaluation periods.")
if (
    set(train["season"]) & set(validation["season"])
    or set(train["season"]) & set(test["season"])
    or set(validation["season"]) & set(test["season"])
):
    raise ValueError("Evaluation periods overlap.")

# Separate the model inputs from the yield target.
X_train = train[settings.FEATURES]
y_train = train[settings.TARGET]
X_validation = validation[settings.FEATURES]
y_validation = validation[settings.TARGET]
X_test = test[settings.FEATURES]
y_test = test[settings.TARGET]

# Fit any scaler later, inside the model's training pipeline.
if __name__ == "__main__":
    print("Prepared records:", len(df))
    print("Training rows:", len(train))
    print("Validation rows:", len(validation))
    print("Testing rows:", len(test))
    print("Model inputs:", settings.FEATURES)

