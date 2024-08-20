import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    # Replace with the path to your data file
    df = pd.read_csv("Plna_databaze_produktu.csv")
    df = df[df.Included == "IN"]
    df['stejna velikost'] = 0.02

    return df

df = load_data()

st.title("LOSEC Czechia Navigator")

# Sidebar for selecting variables
st.sidebar.header("Select Variables for Scatter Plot")

# Column display names dictionary
column_display_names = {
    'Skupina': 'Skupina',
    'Podskupina': 'Podskupina',
    'Kategorie_vyrobku': 'Kategorie výrobku',
    'Pribuznost_CZ_2022': 'Příbuznost CZ 2022',
    'Vyhoda_CZ_2022': 'Výhoda CZ 2022',
    'Koncentrace_trhu_2022': 'Koncentrace trhu 2022',
    'Komplexita_vyrobku_2022': 'Komplexita výrobku 2022',
    'CZ_export_2022': 'CZ Export 2022 $',
    'EU_Import_2022': 'EU Import 2022 $',
    'CZ_Import_2022': 'CZ Import 2022 $',
    'Svet_export_2022': 'Světový export 2022 $',
    'EU_export_2022': 'EU Export 2022 $',
    'EU_svetovy_podil_2022': 'EU Světový Podíl 2022',
    'CZ_svetovy_podil_2022': 'CZ Světový Podíl 2022',
    'CZ_EU_podil_2022': 'CZ-EU Podíl 2022',
    'CZ_2030_export': 'CZ 2030 Export $',
    'CZ_Total_Export_25_30': 'CZ Celkový Export 25-30 $',
    'EU_2030_export': 'EU 2030 Export',
    'EU_Total_Export_25_30': 'EU Celkový Export 25-30 $',
    'CAGR_2022_30_FORECAST': 'CAGR 2022-2030 Předpověď',
    'stejna velikost': 'Stejná Velikost'
}

# Invert the dictionary to map display names back to column names
display_to_column = {v: k for k, v in column_display_names.items()}

# Create lists of display names for the sidebar
ji_display_names = ['Skupina', 'Podskupina', 'Kategorie výrobku']
plot_display_names = [
    'Příbuznost CZ 2022',
    'Výhoda CZ 2022',
    'Koncentrace trhu 2022',
    'Komplexita výrobku 2022',
    'CZ Export 2022 $',
    'EU Import 2022 $',
    'CZ Import 2022 $',
    'Světový export 2022 $',
    'EU Export 2022 $',
    'EU Světový Podíl 2022',
    'CZ Světový Podíl 2022',
    'CZ-EU Podíl 2022',
    'CZ 2030 Export $',
    'CZ Celkový Export 25-30 $',
    'EU 2030 Export',
    'EU Celkový Export 25-30 $',
    'CAGR 2022-2030 Předpověď',
    'Stejná Velikost'
]

hover_display_data = [
    'HS_ID',
    'Produkt_HS6',
    'Produkt_HS4',
    'Produkt_HS2',
    'EU Celkový Export 25-30 $',
    'CZ Celkový Export 25-30 $',
    'Zdroj',
    'IS_REALCAGR'
]

# Sidebar selection boxes using display names
x_axis_display = st.sidebar.selectbox("Select X-axis variable", plot_display_names, index=0)
y_axis_display = st.sidebar.selectbox("Select Y-axis variable", plot_display_names, index=2)
markersize_display = st.sidebar.selectbox("Select size variable", plot_display_names, index=14)
color_display = st.sidebar.selectbox("Select color variable", ji_display_names)
hover_info_display = st.sidebar.multiselect("Select what info should appear on hover", hover_display_data, default='Produkt_HS6')

# Map display names back to column names
x_axis = display_to_column[x_axis_display]
y_axis = display_to_column[y_axis_display]
markersize = display_to_column[markersize_display]
color = display_to_column[color_display]
hover_info = [display_to_column.get(col, col) for col in hover_info_display]

# Sidebar for filtering the color variable
color_values = df[color].unique()
selected_colors = st.sidebar.multiselect(f"Filter by {color_display}", options=color_values, default=color_values)

# Filter section
if 'filters' not in st.session_state:
    st.session_state.filters = []

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Add a filter"):
        st.session_state.filters.append({'column': None, 'range': None})
with col2:
    if st.button("Clear filters"):
        st.session_state.filters = []

# Display existing filters using display names
for i, filter in enumerate(st.session_state.filters):
    filter_col_display = st.sidebar.selectbox(f"Filter {i+1} column", plot_display_names, key=f"filter_col_{i}")
    filter_col = display_to_column[filter_col_display]
    filter_min, filter_max = df[filter_col].min(), df[filter_col].max()
    filter_range = st.sidebar.slider(f"Filter {i+1} range", float(filter_min), float(filter_max), (float(filter_min), float(filter_max)), key=f"filter_range_{i}")
    st.session_state.filters[i]['column'] = filter_col
    st.session_state.filters[i]['range'] = filter_range

# Apply filters to dataframe
filtered_df = df.copy()

# Apply color filter
filtered_df = filtered_df[filtered_df[color].isin(selected_colors)]

# Apply numerical filters
for filter in st.session_state.filters:
    if filter['column'] is not None and filter['range'] is not None:
        filtered_df = filtered_df[
            (filtered_df[filter['column']] >= filter['range'][0]) &
            (filtered_df[filter['column']] <= filter['range'][1])
        ]

# Replace negative values in markersize column with zero
filtered_df[markersize] = filtered_df[markersize].clip(lower=0)

# Remove NA values
filtered_df = filtered_df.dropna(subset=[x_axis, y_axis, color, markersize])

# Plotting
st.header(f"Scatter Plot of {x_axis_display} vs {y_axis_display}")

fig = px.scatter(filtered_df,
                 x=x_axis,
                 y=y_axis,
                 color=color,
                 title=f'{x_axis_display} vs {y_axis_display} colored by {color_display}',
                 hover_data=hover_info,
                 height=700,
                 opacity=0.7,
                 size=markersize,
                 size_max=15)

st.plotly_chart(fig)

st.subheader("CZ 2025 - 2030 Export: "+ "${:,.0f}".format(sum(filtered_df['CZ_Total_Export_25_30'])))
st.subheader("EU 2025 - 2030 Export: "+ "${:,.0f}".format(sum(filtered_df['EU_Total_Export_25_30'])))