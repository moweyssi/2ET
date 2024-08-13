import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide") 
# Load data
@st.cache
def load_data():
    # Replace with the path to your data file
    df = pd.read_csv("OEC_LSE_combined_v3_full navigator_JI_comments.csv")
    return df

df = load_data()
df = df[df.Included=="IN"]
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

x_axis = st.sidebar.selectbox("Select X-axis variable", plot_columns)
y_axis = st.sidebar.selectbox("Select Y-axis variable", plot_columns)
color = st.sidebar.selectbox("Select color variable", ji_columns)
hover_info = st.sidebar.multiselect("Select what info should appear on hover",hover_data)
# Plotting
st.header(f"Scatter Plot of {x_axis} vs {y_axis}")

fig = px.scatter(df, x=x_axis, y=y_axis, color=color, title=f'{x_axis} vs {y_axis} colored by {color}', hover_data=hover_info)

st.plotly_chart(fig)
