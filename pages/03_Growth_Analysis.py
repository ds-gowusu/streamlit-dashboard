import pandas as pd
import plotly.express as px
import streamlit as st

from utils import growth_summary




file_path = r"data/provenance_analytics.csv"

df = pd.read_csv(file_path)

growth_summary = growth_summary(df)

fig = px.line(
	growth_summary,
	x='Age',
	y='DBH',
	markers=True,
	title="Mean DBH Growth by Age"
)

st.plotly_chart(fig, use_container_width=True)


