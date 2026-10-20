###### Preparation.py:



import pandas as pd



\# Load the historical maize records (one row per province per season)

df = pd.read\_csv("maize\_yield\_data.csv")

df = df.dropna()

df = df.sort\_values(\["province", "season"]).reset\_index(drop=True)



\# Yield is derived from production and harvested area, in tonnes per hectare

df\["yield\_t\_per\_ha"] = (df\["production\_t"] / df\["harvested\_area\_ha"]).round(2)



\# Lagged feature: the province's yield in the previous season

df\["prev\_yield"] = df.groupby("province")\["yield\_t\_per\_ha"].shift(1)



\# The first season of each province has no previous season, so it is dropped

df = df.dropna().reset\_index(drop=True)

