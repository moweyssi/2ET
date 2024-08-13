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

st.title("OECxLSE Commander")

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
# Plotting
st.header(f"Scatter Plot of {x_axis} vs {y_axis}")
df = df.dropna(markersize)

# Replace negative values in markersize column with zero
df[markersize] = df[markersize].clip(lower=0)

fig = px.scatter(df,
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
