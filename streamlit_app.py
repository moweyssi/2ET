import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache
def load_data():
    # Replace with the path to your data file
    df = pd.read_excel("OEC_LSE_combined_v3_full navigator_JI_comments.xlsx")
    return df

df = load_data()

st.title("Data Visualization App")

# Sidebar for selecting variables
st.sidebar.header("Select Variables for Scatter Plot")

# Columns for (JI) groups
ji_columns = ['Activity group (JI)', 'Activity subgroup (JI)', 'Item category (JI)', 'Included']

# Columns for plotting
plot_columns = [
    'Product Number', 'HS6', 'HS4', 'HS2', 'Country', 'Environmental category',
    'Environmental benefit', 'Green ex-out', 'Product complexity index', 'Market concentration (HHI)',
    'Current RCA', '2022 Trade Value', '2022 Trade Value Relatedness', '2022 Trade Value RCA', '2022 HHI',
    '2022 Market share', 'PCI Rank', 'PCI', 'TradeValueCAGR', 'Market Value CAGR', 'Market Share CAGR',
    'HHI CAGR', 'CAGR Start Year'
]

x_axis = st.sidebar.selectbox("Select X-axis variable", plot_columns)
y_axis = st.sidebar.selectbox("Select Y-axis variable", plot_columns)
color = st.sidebar.selectbox("Select color variable", ji_columns)

# Plotting
st.header(f"Scatter Plot of {x_axis} vs {y_axis}")

fig = px.scatter(df, x=x_axis, y=y_axis, color=color, title=f'{x_axis} vs {y_axis} colored by {color}')
st.plotly_chart(fig)
