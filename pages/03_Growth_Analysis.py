import pandas as pd
import plotly.express as px
import streamlit as st

from utils import growth_summary, prov_growth




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


fig = px.line(
	growth_summary,
	x='Age',
	y='Total_height',
	markers=True,
	title="Mean Total Height Growth by Age"
)

st.plotly_chart(fig, use_container_width=True)


prov_growth = prov_growth(df)

fig = px.line(
	prov_growth,
	x='Age',
	y='Provenance2',
	markers=True,
	title="DBH Growth by Provenance"
)

st.plotly_chart(fig, use_container_width=True)
