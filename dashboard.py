import streamlit as st 
import pandas as pd
import plotly.express as px

from utils import * 

st.set_page_config(page_title='Teak Provenances Analysis',layout='wide')


# Load data
file_path = r"data/provenance_analytics.csv"

df = pd.read_csv(file_path)

# ---------------------------------------
# Sidebar
# ---------------------------------------
st.sidebar.header("Filters")
selected_age = st.sidebar.multiselect(
	"Select Age",
	options=sorted(df['Age'].unique()),
	default=sorted(df['Age'].unique())
)

selected_provenance = st.sidebar.multiselect(
	"Select Provenance",
	options=sorted(df['Provenance2'].unique()),
	default=sorted(df['Provenance2'].unique())
)

filtered_df = df[
	(df['Age'].isin(selected_age))
	& (df['Provenance2'].isin(selected_provenance))
]

# -------------------------------------
# Title
# -------------------------------------

st.title("Teak Provenance Analytics Dashboard")
st.markdown(
	"""
	Monitoring growth performance and productivity of
	 provenance trials using PSP data.  
	"""
)

st.divider()

# -----------------------------------------
# KPI Section
# -----------------------------------------

total_trees = len(filtered_df)

total_plots = filtered_df['Plot'].nunique()

total_provenances = filtered_df['Provenance2'].nunique()

avg_dbh = filtered_df['DBH'].mean()

avg_height = filtered_df['Total_height'].mean()

avg_basal_area = filtered_df['basal_area_m2'].mean()

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
	"Trees",
	f"{total_trees:,}"
)

col2.metric(
	"Plots",
	f"{total_plots:,}"
)

col3.metric(
	"Provenances",
	f"{total_provenances:,}"
)

col4.metric(
	"Mean DBH (cm)",
	f"{avg_dbh:.2f}"
)

col5.metric(
	"Mean Height (m)",
	f"{avg_height:.2f}"
)

col6.metric(
	"Mean Basal Area (m2)",
	f"{avg_basal_area:.4f}"
)

st.divider()

# ------------------------------------------
# Charts
# ------------------------------------------

col1, col2 =  st.columns(2)

# Provenance Distribution

with col1:
	prov_counts = (
		filtered_df['Provenance2']
		.value_counts()
		.reset_index()
	)

	prov_counts.columns = [
		"Provenance",
		"Tree Count"
	]

	fig = px.bar(
		prov_counts,
		x="Provenance",
		y="Tree Count",
		title="Tree Distribution by Provenance"
	)

	st.plotly_chart(
		fig,
		use_container_width=True
	)

# Age Distribution
with col2:
	age_counts = (
		filtered_df['Age']
		.value_counts()
		.sort_index()
		.reset_index()
	)

	age_counts.columns = [
		"Age",
		"Tree Count",
	]

	fig = px.bar(
		age_counts,
		x="Age",
		y="Tree Count",
		title="Tree Distribution by Age"
	)

	st.plotly_chart(
		fig,
		use_container_width=True
	)
st.divider()


# compute plot dimension (21m x 21m) into hectare
plot_size = (21*21)/10000

# Basal Area 
ba_df = calculate_basal_area_per_hectare(df, plot_size)
ba_df = aggregate_basal_area_per_hectare_by_provenance(ba_df)

# Stems Per Hectare
spha_df = calculate_stems_per_hectare(df, plot_size)
spha_df = aggregate_stems_per_hectare_by_provenance(spha_df)

ba_age = calculate_basal_area_per_hectare_by_age_and_provenance(df, plot_size)


# ----------------------------------
# Streamlit Layouts
# ----------------------------------

# Layout into 2 columns
col1, col2 = st.columns(2, gap='medium')

with col1:
    st.markdown("##### Basal Area Per Provenances")

    st.bar_chart(
        data=ba_df,
        x='Provenance2', 
        y='ba_per_ha', 
        x_label='Provenance',
        y_label='Basal Area (m2/ha)'
    )

with col2:
    st.markdown("##### Stands Per Hectare")

    st.bar_chart(
        data=spha_df,
        x='Provenance2',
        y='stems_per_ha',
        x_label='Provenance',
        y_label='Stems Per Hectare'
    )


# Basal Area Based on Age 
with st.container():
    st.markdown("#### Basal Area Per Provenances Based on Age")

    ages = sorted(ba_age['Age'].unique())
    age_option = st.segmented_control(
        "Select Age",
        options=["All"] + list(ages),
        default="All"
    )
    
    filtered_df = None 

    if age_option == "All":
        filtered_df = ba_age
    else:
        filtered_df = filter_basal_for_age(ba_age, age_option)

    #filtered_df

    # --------------------
    # Plot view
    # --------------------
    st.bar_chart(
        data=filtered_df,
        x='Provenance2',
        y='ba_per_ha',
        x_label="Provenance",
        y_label="Basal Area (m2/ha)"
    )



# ---------------------------------
# Raw Data Preview
# ---------------------------------

st.subheader("Dataset Preview")

st.dataframe(
	filtered_df.head(10),
	use_container_width=True
)
