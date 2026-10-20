###### Dashboard.py:



import joblib

import streamlit as st

import settings

import chatbot

from preparation import df



st.title("AgriPredict AI")

st.write("Provincial maize yield estimates in", settings.UNIT)



province = st.selectbox("Choose a province", settings.PROVINCES)

rows = df\[df\["province"] == province]



st.subheader("Historical yield trend")

st.line\_chart(rows.set\_index("season")\[settings.TARGET])



\# Estimate for the coming season, using the average of the last three seasons

model = joblib.load("forest\_model")

latest = rows.iloc\[-1]

recent = rows.tail(3)

inputs = \[\[

&#x20;   recent\["rainfall\_mm"].mean(),

&#x20;   recent\["avg\_temp\_c"].mean(),

&#x20;   latest\["harvested\_area\_ha"],

&#x20;   latest\[settings.TARGET],

]]

estimate = model.predict(inputs)\[0]



st.metric("Estimate for the coming season", f"{round(estimate, 2)} t/ha")

st.caption("This is a provincial average, not a prediction for an individual farm.")



st.subheader("Provincial comparison")

st.bar\_chart(df.groupby("province")\[settings.TARGET].mean())



st.subheader("Model performance")

st.write("Each model is compared with a historical baseline using MAE and RMSE on the last four seasons.")

st.write("Run yield\_model.py to print the latest figures and paste them here for the record.")



st.subheader("Text assistant")

question = st.text\_input("Ask about yields, the data or the limitations")

if question:

&#x20;   st.write(chatbot.respond(question))



st.caption("AgriPredict AI supports planning decisions only and does not guarantee a harvest.")

