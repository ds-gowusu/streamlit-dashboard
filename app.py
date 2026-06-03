import streamlit as st 
import pandas as pd

from utils import * 

st.set_page_config(layout='wide')


# Load data
#file_path = r"~/Desktop/projects/Python/py_envs/forest_ml/provenance_psp_data.csv"
#file_path = r"C:\Users\GILBERT FG\Desktop\Projects\portfolio\streamlit_proj\data\provenance_psp_data.csv"

file_path = r"/data/provenance_psp_data.csv"

df = pd.read_csv(file_path)

# compute plot dimension (21m x 21m) into hectare
plot_size = (21*21)/10000

# Basal Area 
ba_df = calculate_basal_area_per_hectare_by_plot(df, plot_size)
ba_df = aggregate_basal_area_per_hectare_by_provenance(ba_df)

# Stems Per Hectare
spha_df = calculate_stems_per_hectare_by_plot(df, plot_size)
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

