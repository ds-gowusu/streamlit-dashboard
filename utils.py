# Stems per Hectare
def calculate_stems_per_hectare(df, plot_size):
    spha = df.groupby(['Provenance2', 'Plot']).size().reset_index(name='stems_per_plot')
    spha['stems_per_ha'] = spha['stems_per_plot'] /plot_size

    return spha

def aggregate_stems_per_hectare_by_provenance(df):
    v_spha = df.groupby('Provenance2')['stems_per_ha'].mean().reset_index()

    return v_spha


# Basal Area 
def calculate_basal_area_per_hectare(df, plot_size):
    ba_ha = df.groupby(['Provenance2', 'Plot'])['basal_area_m2'].sum().reset_index()

    ba_ha['ba_per_ha'] = ba_ha['basal_area_m2'] / plot_size 

    return ba_ha

def aggregate_basal_area_per_hectare_by_provenance(df):
    ba_prov = df.groupby('Provenance2')['ba_per_ha'].mean().reset_index()

    return ba_prov


# Basal Area per Provenances by Ages
def calculate_basal_area_per_hectare_by_age_and_provenance(df, plot_size):
    ba_age = df.groupby(['Age', 'Provenance2'])['basal_area_m2'].sum().reset_index()
    ba_age['ba_per_ha'] = ba_age['basal_area_m2'] / plot_size
    
    return ba_age

def filter_basal_for_age(df, selected_age):
    ba = df[df['Age'] == selected_age]

    return ba

# Mean Growth by Age
def growth_summary(df):
	df = df.groupby('Age').agg({
		"DBH": "mean",
		"Total_height": "mean",
		"Merchantable_height": "mean"
		}).reset_index()
	return df	
