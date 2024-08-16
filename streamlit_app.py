import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide") 
# Load data
@st.cache
def load_data():
    # Replace with the path to your data file
    df = pd.read_csv("OEC_LSE_combined_v3_full navigator_JI_comments.csv")
    df = df[df.Included=="IN"]
    df['equal size'] = 0.02

    return df

df = load_data()

st.title("LOSEC Czechia Navigator")

# Sidebar for selecting variables
st.sidebar.header("Select Variables for Scatter Plot")

# Columns for (JI) groups
ji_columns = ['Activity group (JI)',
              'Activity subgroup (JI)',
              'Item category (JI)',
              'Environmental category',
              ]

# Columns for plotting
plot_columns = [
    'Product complexity index',
    'Market concentration (HHI)',
    'Current RCA',
    '2022 Trade Value',
    '2022 Trade Value Relatedness',
    '2022 Trade Value RCA',
    '2022 HHI',
    '2022 Market share',
    'PCI Rank',
    'PCI',
    'TradeValueCAGR',
    'Market Value CAGR', 
    'Market Share CAGR',
    'HHI CAGR',
    'equal size'
]
hover_data = ['Product Number', 
              'HS6', 
              'HS4', 
              'HS2', 
              'Country', 
              'Environmental benefit', 
              'Green ex-out',
              'CAGR Start Year', 
              'CAGR End Year']

x_axis = st.sidebar.selectbox("Select X-axis variable", plot_columns,index=0)
y_axis = st.sidebar.selectbox("Select Y-axis variable", plot_columns,index=2)
markersize = st.sidebar.selectbox("Select size variable", plot_columns,index=14)
color = st.sidebar.selectbox("Select color variable", ji_columns)
hover_info = st.sidebar.multiselect("Select what info should appear on hover",hover_data,default='HS6')

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