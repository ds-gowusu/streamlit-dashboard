import pandas as pd
import plotly.express as px
import streamlit as st

from utils import growth_summary




file_path = r"data/provenance_analytics.csv"

df = pd.read_csv(file_path)


st.header("Growth Trends")


growth_summary = growth_summary(df)

col1, col2 = st.columns(2)

with col1:

	fig = px.line(
		growth_summary,
		x='Age',
		y='DBH',
		markers=True,
		title="Mean DBH Growth by Age"
	)

	st.plotly_chart(fig, use_container_width=True)

with col2:

	fig = px.line(
		growth_summary,
		x='Age',
		y='Total_height',
		markers=True,
		title="Mean Total Height Growth by Age"
	)

	st.plotly_chart(fig, use_container_width=True)


st.divider()

dbh_increment = (
	growth_summary
	.assign(
		dbh_increment=lambda x: x['DBH'].diff()
	)
)

st.subheader("Mean Annual DBH Increment")

st.dataframe(
	dbh_increment[['Age', 'DBH', 'dbh_increment']]
)



latest_age = df['Age'].max()

top_growth = (
	df[df['Age'] == latest_age].groupby('Provenance2').agg({
			"DBH": "mean",
			"Total_height": "mean"
		}).sort_values(
			"DBH",
			ascending=False
		)
)


st.subheader(f"Top Provenances at Age {latest_age}")

st.dataframe(top_growth)
