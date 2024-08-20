import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide") 
# Load data
@st.cache
def load_data():
    # Replace with the path to your data file
    df = pd.read_csv("Plna_databaze_produktu.csv")
    df = df[df.Included=="IN"]
    df['stejna velikost'] = 0.02

    return df

df = load_data()

st.title("LOSEC Czechia Navigator")

# Sidebar for selecting variables
st.sidebar.header("Select Variables for Scatter Plot")

# Columns for (JI) groups
ji_columns = ['Skupina',
              'Podskupina',
              'Kategorie_vyrobku',
              ]

# Columns for plotting
plot_columns = [
'Pribuznost_CZ_2022',
'Vyhoda_CZ_2022',
'Koncentrace_trhu_2022',
'Komplexita_vyrobku_2022',
'CZ_export_2022',
'EU_Import_2022',
'CZ_Import_2022',
'Svet_export_2022',
'EU_export_2022',
'EU_svetovy_podil_2022',
'CZ_svetovy_podil_2022',
'CZ_EU_podil_2022',
'CZ_2030_export',
'CZ_Total_Export_25_30',
'EU_2030_export',
'EU_Total_Export_25_30',
'CAGR_2022_30_FORECAST',
'stejna velikost'
]
hover_data = ['HS_ID', 
              'Produkt_HS6',
              'Produkt_HS4',
              'Produkt_HS2',
              'EU_Total_Export_25_30',
              'CZ_Total_Export_25_30',
              'Zdroj',
              'IS_REALCAGR'
              ]

x_axis = st.sidebar.selectbox("Select X-axis variable", plot_columns,index=0)
y_axis = st.sidebar.selectbox("Select Y-axis variable", plot_columns,index=2)
markersize = st.sidebar.selectbox("Select size variable", plot_columns,index=14)
color = st.sidebar.selectbox("Select color variable", ji_columns)
hover_info = st.sidebar.multiselect("Select what info should appear on hover",hover_data,default='Produkt_HS6')

# Sidebar for filtering the color variable
color_values = df[color].unique()
selected_colors = st.sidebar.multiselect(f"Filter by {color}", options=color_values, default=color_values)

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

# Display existing filters
for i, filter in enumerate(st.session_state.filters):
    filter_col = st.sidebar.selectbox(f"Filter {i+1} column", plot_columns, key=f"filter_col_{i}")
    filter_min, filter_max = df[filter_col].min(), df[filter_col].max()
    filter_range = st.sidebar.slider(f"Filter {i+1} range", float(filter_min), float(filter_max), (float(filter_min), float(filter_max)), key=f"filter_range_{i}")
    st.session_state.filters[i]['column'] = filter_col
    st.session_state.filters[i]['range'] = filter_range

# Apply filters to dataframe
filtered_df = df.copy()
# Apply color filter
filtered_df = filtered_df[filtered_df[color].isin(selected_colors)]

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
st.header(f"Scatter Plot of {x_axis} vs {y_axis}")

fig = px.scatter(filtered_df,
                 x=x_axis,
                 y=y_axis,
                 color=color,
                 title=f'{x_axis} vs {y_axis} colored by {color}',
                 hover_data=hover_info,
                 height=700,
                 opacity=0.7,
                 size=markersize,
                 size_max=15)

st.plotly_chart(fig)

st.subheader("CZ 2025 - 2030 Export: "+ "${:,.0f}".format(sum(filtered_df['CZ_Total_Export_25_30']))+" $")