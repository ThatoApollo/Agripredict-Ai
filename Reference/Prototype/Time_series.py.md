###### Time\_series.py:



import pandas as pd

import numpy as np

import settings

from preparation import df



\# Trend analysis for each province, over the full clean record

for province in settings.PROVINCES:

&#x20;   rows = df\[df\["province"] == province]

&#x20;   yields = rows\["yield\_t\_per\_ha"].to\_numpy()

&#x20;   seasons = np.arange(1, len(yields) + 1)



&#x20;   # A three season moving average smooths out one-off good or bad seasons

&#x20;   moving\_avg = pd.Series(yields).rolling(3).mean().round(2).tolist()



&#x20;   # Straight line fit: the slope is the change in yield per season

&#x20;   slope, intercept = np.polyfit(seasons, yields, 1)

&#x20;   next\_season = slope \* (len(seasons) + 1) + intercept



&#x20;   print("Province:", province)

&#x20;   print("Yields:", list(yields))

&#x20;   print("Moving average:", moving\_avg)

&#x20;   print("Trend per season:", round(slope, 3))

&#x20;   print("Trend estimate for the next season:", round(next\_season, 2), settings.UNIT)

&#x20;   if slope < -0.1:

&#x20;       print("Note: the trend is falling, so review procurement plans")

&#x20;   print()

