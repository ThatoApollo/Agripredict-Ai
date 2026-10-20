###### Yield\_model.py:



from preparation import df

import settings

import numpy as np

import joblib

from sklearn.linear\_model import LinearRegression

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean\_absolute\_error, mean\_squared\_error



\# Chronological split: earlier seasons train, the last four seasons test

train = df\[\~df\["season"].isin(settings.TEST\_SEASONS)]

test = df\[df\["season"].isin(settings.TEST\_SEASONS)]



X\_train = train\[settings.FEATURES].to\_numpy()

y\_train = train\[settings.TARGET].to\_numpy()

X\_test = test\[settings.FEATURES].to\_numpy()

y\_test = test\[settings.TARGET].to\_numpy()



print("Training seasons:", train\["season"].nunique(), "| Testing seasons:", test\["season"].nunique())

print("Training rows:", len(train), "| Testing rows:", len(test))

print()



def report(name, predictions):

&#x20;   mae = mean\_absolute\_error(y\_test, predictions)

&#x20;   rmse = np.sqrt(mean\_squared\_error(y\_test, predictions))

&#x20;   print(name, "MAE =", round(mae, 3), "| RMSE =", round(rmse, 3))



\# Historical baseline: each province's average yield over the training seasons

baseline = train.groupby("province")\[settings.TARGET].mean()

report("Historical baseline", test\["province"].map(baseline).to\_numpy())



linear = LinearRegression()

linear.fit(X\_train, y\_train)

report("Linear regression  ", linear.predict(X\_test))



forest = RandomForestRegressor(n\_estimators=200, random\_state=42)

forest.fit(X\_train, y\_train)

report("Random forest      ", forest.predict(X\_test))



\# Save the models so the dashboard can reuse them

joblib.dump(forest, "forest\_model")

joblib.dump(linear, "linear\_model")



\# Province by province errors for the random forest

test = test.copy()

test\["predicted"] = forest.predict(X\_test)

print()

print("Random forest error by province:")

for province in settings.PROVINCES:

&#x20;   rows = test\[test\["province"] == province]

&#x20;   print(province, "MAE =", round(mean\_absolute\_error(rows\[settings.TARGET], rows\["predicted"]), 3))

