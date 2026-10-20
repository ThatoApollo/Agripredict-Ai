###### Deep\_learning.py:



from preparation import df

import settings

import numpy as np

from sklearn.neural\_network import MLPRegressor

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import mean\_absolute\_error, mean\_squared\_error



train = df\[\~df\["season"].isin(settings.TEST\_SEASONS)]

test = df\[df\["season"].isin(settings.TEST\_SEASONS)]



X\_train = train\[settings.FEATURES].to\_numpy()

y\_train = train\[settings.TARGET].to\_numpy()

X\_test = test\[settings.FEATURES].to\_numpy()

y\_test = test\[settings.TARGET].to\_numpy()



\# A neural network needs its inputs on a similar scale

scaler = StandardScaler()

X\_train = scaler.fit\_transform(X\_train)

X\_test = scaler.transform(X\_test)



\# A small experimental feed-forward network

network = MLPRegressor(hidden\_layer\_sizes=(16, 8), max\_iter=5000, random\_state=42)

network.fit(X\_train, y\_train)



predictions = network.predict(X\_test)

print("Neural network MAE  =", round(mean\_absolute\_error(y\_test, predictions), 3))

print("Neural network RMSE =", round(np.sqrt(mean\_squared\_error(y\_test, predictions)), 3))

print()

print("With only a few seasons of data the network is expected to do no better than the simpler models.")

print("It is kept as an experimental comparison, as set out in the project scope.")

