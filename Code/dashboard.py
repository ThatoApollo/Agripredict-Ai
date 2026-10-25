"""Run from the project root: streamlit run Code/dashboard.py"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

import chatbot
import settings
from preparation import df, train, validation

st.set_page_config(page_title="AgriPredict AI", page_icon="🌽", layout="wide")
st.markdown("""
<style>
.stApp {background: #f6f8fa;}
.block-container {padding-top: 1.5rem; max-width: 1500px;}
.agri-header {background: #12452f; color: white; padding: 18px 24px;
 border-radius: 10px; margin-bottom: 28px; font-size: 22px; font-weight: 600;}
.agri-header span {color: #c8e3d4; font-weight: 400;}
[data-testid="stVerticalBlockBorderWrapper"] {background: white; border-radius: 14px;}
h1, h2, h3 {color: #101b2e;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="agri-header">🌽 AgriPredict AI <span>· Maize yields</span></div>',
            unsafe_allow_html=True)


def read_metrics(filename):
    path = settings.PROJECT_DIR / "Results" / filename
    try:
        data = pd.read_csv(path)
        if not {"split", "model", "MAE", "RMSE"}.issubset(data.columns):
            return None
        data = data[data["split"] == "Test"].copy()
        for column in ["MAE", "RMSE"]:
            data[column] = pd.to_numeric(data[column], errors="raise")
        if data.empty or not np.isfinite(data[["MAE", "RMSE"]]).all().all():
            return None
        if (data[["MAE", "RMSE"]] < 0).any().any():
            return None
        return data
    except (OSError, ValueError, TypeError, pd.errors.ParserError):
        return None


left, right = st.columns([3, 1])
with left:
    st.title("Provincial Maize Overview")
    st.caption("Provincial maize yield information to help plan procurement and storage.")
with right:
    province = st.selectbox("Choose a province", settings.PROVINCES)

rows = df[df["province"] == province].sort_values("harvest_year")
history = pd.concat([train, validation], ignore_index=True)
baseline = float(history.loc[history["province"] == province, settings.TARGET].mean())
latest_season = rows.iloc[-1]["season"]
for column, label, value in zip(st.columns(4),
        ["Provinces", "Seasons covered", "Latest recorded season", "Average yield"],
        [str(df["province"].nunique()), str(rows["season"].nunique()), latest_season,
         f"{rows[settings.TARGET].mean():.2f} t/ha"]):
    with column:
        with st.container(border=True):
            st.metric(label, value)
st.caption("Yield is measured in tonnes per planted hectare. The average covers all recorded seasons for the selected province.")

chart_column, scenario_column = st.columns([2, 1])
with chart_column:
    with st.container(border=True):
        st.subheader(f"Historical yield — {province}")
        fig, ax = plt.subplots(figsize=(10, 4.5))
        ax.plot(rows["harvest_year"], rows[settings.TARGET], color="#168345",
                marker="o", markersize=4, label="Observed yield")
        ax.plot(rows["harvest_year"], rows[settings.TARGET].rolling(3).mean(),
                color="#dc8c22", linestyle="--", label="Average of the last 3 seasons")
        years = rows["harvest_year"].tolist()[::3]
        ax.set_xticks(years, [f"{y-1}/{str(y)[-2:]}" for y in years], rotation=35, ha="right")
        ax.set_ylabel("Tonnes per planted hectare")
        ax.grid(alpha=.2, linestyle="--")
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(frameon=False, fontsize=9)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption("The green line shows each season’s recorded yield.")
        st.caption("The orange dashed line averages three seasons to make the overall pattern easier to see.")
with scenario_column:
    with st.container(border=True):
        st.subheader("Historical Average for Planning")
        st.metric("Average yield per planted hectare:", f"{baseline:.2f} t/ha")
        st.write("Calculated from the selected province’s yields between 2000/01 and 2019/20. This average is used in the production planning calculation.")
        st.caption("This average is based on past yields and does not use this season’s weather to predict the harvest.")
   with st.container(border=True):
    st.subheader("Planning scenario")

    area = st.number_input(
        "Enter planted area (hectares)",
        min_value=0.0,
        max_value=10000000.0,
        value=None,
        step=1.0,
        placeholder="Type your planted area"
    )

    if area is not None:
        volume = baseline * area
        st.metric(
            "Estimated production for this scenario",
            f"{volume:,.0f} tonnes"
        )

comparison_column, performance_column = st.columns(2)
with comparison_column:
    with st.container(border=True):
        st.subheader("Provincial comparison")
        means = df.groupby("province")[settings.TARGET].mean().reindex(settings.PROVINCES)
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(means.index, means.values, color=["#17643c", "#168345", "#6da813"])
        ax.set_ylabel("Tonnes per planted hectare")
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", alpha=.2)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption("This graph compares the average maize yield per planted hectare across the three provinces over 24 seasons, from 2000/01 to 2023/24.")
with performance_column:
    with st.container(border=True):
        st.subheader("How the models performed")
        st.caption("Historical test period: 2020/21–2023/24, covering 12 province-season records. Models were fitted on earlier seasons.")
        scores = read_metrics("model_metrics.csv")
        if scores is None:
            st.warning("Model results are unavailable. Run python Code/yield_model.py from the project root.")
        else:
            table = scores[["model", "MAE", "RMSE"]].rename(columns={"model": "Approach"})
            st.dataframe(table, hide_index=True, width="stretch")
        neural = read_metrics("neural_network_metrics.csv")
        if neural is not None:
            st.caption("Experimental neural network — exploratory comparison using the previously inspected test period:")
            table = neural[neural["model"] == "Experimental neural network"]
            st.dataframe(table[["model", "MAE", "RMSE"]].rename(columns={"model": "Approach"}),
                         hide_index=True, width="stretch")
        st.caption("MAE is the average absolute error; RMSE gives more weight to large errors. Both use tonnes per planted hectare. Lower is better.")
        st.write("The historical baseline had the lowest validation error in our comparison and remains the preferred approach. None of these results guarantees future accuracy.")

with st.container(border=True):
    st.subheader("AgriPredict Assistant")
    st.caption("Ask one question about the platform or a supported maize farming topic. Replies are predefined; the assistant does not use earlier messages as context.")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content":
            "Hello! Ask about model performance, maize planting, soil, irrigation, fertiliser or crop rotation."}]
    if st.button("Clear conversation"):
        st.session_state.messages = st.session_state.messages[:1]
    with st.container(height=320):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    question = st.chat_input("Ask about AgriPredict or maize farming", max_chars=1000)
    if question:
        st.session_state.messages.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": chatbot.respond(question)},
        ])
        st.rerun()

st.caption("AgriPredict AI · Student prototype · Small dataset, simplified weather coverage and provincial estimates. Sources and assumptions are documented in the project documentation.")
