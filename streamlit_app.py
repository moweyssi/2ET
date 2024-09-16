import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import plotly.io as pio
st.set_page_config(layout="wide")
st.title("LOSEC Czechia Navigator")

# Sidebar for selecting variables
st.sidebar.header("Select Variables for Scatter Plot")

USD_to_czk = st.sidebar.number_input("USD to CZK",value=22.5)
color_discrete_map = {
    # Set 1
    'A02. Doprava': '#FFB3BA',  # Pastel red for transportation
    'A03. Budovy': '#FFDFBA',   # Pastel orange for buildings
    'A04. Výroba nízkoemisní elektřiny a paliv': '#FFFFBA',  # Pastel yellow for low-emission energy
    'A05. Ukládání energie': '#BAFFC9',  # Pastel green for energy storage
    'A06. Energetické sítě': '#BAE1FF',  # Pastel blue for energy grids
    'E01. Měřící a diagnostické přístroje; Monitoring': '#FFB3E6',  # Pastel pink for monitoring
    'A01. Výroba, nízkoemisní výrobní postupy': '#FFB3FF',  # Pastel magenta for low-emission manufacturing
    'B02. Cirkularita a odpady': '#E6FFB3',  # Pastel lime for circularity and waste

    # Set 2
    'A02c. Cyklistika a jednostopá': '#FFB3BA',  # Same pastel red for cycling
    'A03a. Snižování energetické náročnosti budov': '#FFDFBA',  # Same pastel orange for energy efficiency in buildings
    'A04f. Jádro': '#FFFFBA',  # Same pastel yellow for nuclear
    'A05b. Vodik a čpavek': '#BAFFC9',  # Same pastel green for hydrogen and ammonia
    'A06a. Distribuce a přenos elektřiny': '#BAE1FF',  # Same pastel blue for electricity distribution
    'A04a. Větrná': '#FFB3E6',  # Same pastel pink for wind energy
    'E0f. Měření v energetice a síťových odvětvích (HS9028 - 9030, 903210)': '#FFB3FF',  # Same pastel magenta for energy measurement
    'E01c. Měření okolního prostředí (HS9025)': '#E6FFB3',  # Same pastel lime for environmental measurement
    'E01i. Ostatní': '#FFB347',  # Pastel peach for "other"
    'A02a. Železniční (osobní i nákladní)': '#FFCCCB',  # Light pastel red for railways
    'E01h. Surveying / Zeměměřičství (HS 9015)': '#FFDAC1',  # Light pastel orange for surveying
    'A01a. Nízkoemisní výroba': '#FFFACD',  # Light pastel yellow for low-emission manufacturing
    'A04g. Efektivní využití plynu a vodíku': '#B0E57C',  # Pastel green for efficient gas and hydrogen usage
    'E01e. Chemická analýza (HS9027)': '#B2FFFF',  # Light pastel blue for chemical analysis
    'A04b. Solární': '#FFB347',  # Pastel peach for solar
    'A03b. Elektrifikace tepelného hospodářství': '#F1C0E8',  # Pastel lavender for heat electrification
    'A05a. Baterie': '#C9E7FF',  # Light pastel blue for batteries
    'E01d. Měření vlastností plynů a tekutnin (HS9026)': '#FFC9DE',  # Light pastel pink for gas & liquid measurement
    'E01a. Optická měření (HS 9000 - 9013, HS 903140)': '#FFD1BA',  # Pastel light orange for optical measurements
    'B02b. Cirkularita, využití odpadu': '#E5FFCC',  # Light pastel lime for waste circularity
    'A05c. Ostatní ukládání': '#FFE5B4',  # Light pastel peach for other storage
    'A01c. Elektrifikace výrobních postupů': '#FFC3A0',  # Pastel peach for electrification of processes
    'A03b. Elektrifikace domácností': '#FFDFD3',  # Light pastel pink for household electrification

    # Set 3
    'Díly a vybavení': '#FFB3BA',  # Same pastel red for parts and equipment
    'Zateplení, izolace': '#FFDFBA',  # Same pastel orange for insulation
    'Komponenty pro jadernou energetiku': '#FFFFBA',  # Same pastel yellow for nuclear components
    'Vodík (elektrolyzéry)': '#BAFFC9',  # Same pastel green for hydrogen electrolysis
    'Transformační stanice a další síťové komponenty': '#BAE1FF',  # Same pastel blue for network components
    'Komponenty pro větrnou energetiku': '#FFB3E6',  # Same pastel pink for wind components
    'Termostaty': '#FFB3FF',  # Same pastel magenta for thermostats
    'Termometry': '#E6FFB3',  # Same pastel lime for thermometers
    'Ostatní': '#FFB347',  # Same pastel peach for others
    'Nové lokomotivy a vozy': '#FFCCCB',  # Light pastel red for new locomotives
    'Surveying / Zeměměřičství': '#FFDAC1',  # Light pastel orange for surveying equipment
    'Nízkoemisní výroby ostatní': '#FFFACD',  # Light pastel yellow for other low-emission production
    'Komponenty pro výrobu energie z plynů': '#B0E57C',  # Pastel green for gas energy components
    'Spektrometry': '#B2FFFF',  # Light pastel blue for spectrometry
    'Komponenty pro solární energetiku': '#FFB347',  # Pastel peach for solar components
    'Tepelná čerpadla a HVAC': '#F1C0E8',  # Pastel lavender for heat pumps and HVAC
    'Infrastruktura (nové tratě a elektrifikace stávajících)': '#C9E7FF',  # Light pastel blue for infrastructure
    'Baterie': '#FFC9DE',  # Light pastel pink for batteries
    'Měření odběru a výroby plynů, tekutin, elektřiny': '#FFD1BA',  # Light pastel orange for energy measurements
    'Komponenty pro vodní energetiku': '#E5FFCC',  # Light pastel lime for water energy components
    'Měření vlastností plynů a tekutin': '#FFE5B4',  # Light pastel peach for gas & liquid measurements
    'Optická měření': '#FFC3A0',  # Pastel peach for optical measurements
    'Materiálové využití': '#FFDFD3',  # Light pastel pink for material use
    'Měření ionizujícího záření': '#FFB3BA',  # Pastel red for radiation measurements
    'Ostatní ukládání (přečerpávací vodní, ohřátá voda,…)': '#FFDFBA',  # Same pastel orange for other storage
    'Hydrometry': '#FFFFBA',  # Same pastel yellow for hydrometry
    'Elektrifikace ve výrobě': '#BAFFC9',  # Same pastel green for electrification in manufacturing
    'Domácí elektrické spotřebiče': '#BAE1FF',  # Same pastel blue for household appliances
    'Chromatografy': '#FFB3E6',  # Same pastel pink for chromatographs
    'Osciloskopy': '#FFB3FF',  # Same pastel magenta for oscilloscopes
}

# Load data
def load_data():
    # Replace with the path to your data file
    #df = pd.read_csv("Plna_databaze_produktu.csv")
    url                         = 'https://docs.google.com/spreadsheets/d/1M4_XVEXApUbnklbRwX1dqDVYIDStX4Uk/pub?gid=891291031&single=true&output=csv'
    df                          = pd.read_csv(url)
    df                          = df[df.Included == "IN"]
    df['stejna velikost']       = 0.02
    df['CZ_EU_podil_2022']      = 100 * df['CZ_EU_podil_2022'] 
    df['EU_svetovy_podil_2022'] = 100 * df['EU_svetovy_podil_2022'] 
    df['CZ_svetovy_podil_2022'] = 100 * df['CZ_svetovy_podil_2022'] 
    df['CZ_export_2022']        = USD_to_czk*df['CZ_export_2022'] 
    df['EU_Import_2022']        = USD_to_czk*df['EU_Import_2022'] 
    df['CZ_Import_2022']        = USD_to_czk*df['CZ_Import_2022'] 
    df['Svet_export_2022']      = USD_to_czk*df['Svet_export_2022'] 
    df['EU_export_2022']        = USD_to_czk*df['EU_export_2022'] 
    df['EU_Total_Export_25_30'] = USD_to_czk*df['EU_Total_Export_25_30'] 
    df['CZ_Total_Export_25_30'] = USD_to_czk*df['CZ_Total_Export_25_30'] 
    df['EU_2030_export']        = USD_to_czk*df['EU_2030_export'] 
    df['CZ_2030_export']        = USD_to_czk*df['CZ_2030_export'] 
    df['HS_ID']                 = df['HS_ID'].astype(str)

    return df

df = load_data()



# Column display names dictionary
column_display_names = {
    'Skupina': 'Skupina',
    'Podskupina': 'Podskupina',
    'Kategorie_vyrobku': 'Kategorie výrobku',
    'Pribuznost_CZ_2022': 'Příbuznost CZ 2022',
    'Vyhoda_CZ_2022': 'Výhoda CZ 2022',
    'Koncentrace_trhu_2022': 'Koncentrace světového trhu 2022',
    'EU_HHI_2022':'Koncentrace evropského exportu 2022',
    'Komplexita_vyrobku_2022': 'Komplexita výrobku 2022',
    'CZ_export_2022': 'CZ Export 2022 CZK',
    'EU_Import_2022': 'EU Import 2022 CZK',
    'CZ_Import_2022': 'CZ Import 2022 CZK',
    'Svet_export_2022': 'Světový export 2022 CZK',
    'EU_export_2022': 'EU Export 2022 CZK',
    'EU_svetovy_podil_2022': 'EU Světový Podíl 2022 %',
    'CZ_svetovy_podil_2022': 'CZ Světový Podíl 2022 %',
    'EU_Top_Exporter_2022':'EU Největší Exportér 2022',
    'CZ_EU_podil_2022': 'CZ-EU Podíl 2022 %',
    'CZ_2030_export': 'CZ 2030 Export CZK',
    'CZ_Total_Export_25_30': 'CZ Celkový Export 25-30 CZK',
    'EU_2030_export': 'EU 2030 Export CZK',
    'EU_Total_Export_25_30': 'EU Celkový Export 25-30 CZK',
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
    'Koncentrace světového trhu 2022',
    'Koncentrace evropského exportu 2022',
    'Komplexita výrobku 2022',
    'CZ Export 2022 CZK',
    'EU Import 2022 CZK',
    'CZ Import 2022 CZK',
    'Světový export 2022 CZK',
    'EU Export 2022 CZK',
    'EU Světový Podíl 2022 %',
    'CZ Světový Podíl 2022 %',
    'CZ-EU Podíl 2022 %',
    'CZ 2030 Export CZK',
    'CZ Celkový Export 25-30 CZK',
    'EU 2030 Export CZK',
    'EU Celkový Export 25-30 CZK',
    'CAGR 2022-2030 Předpověď',
    'Stejná Velikost'
]

hover_display_data = [
    'HS_ID',
    'Produkt_HS6',
    'Produkt_HS4',
    'Produkt_HS2',
    'CZ Celkový Export 25-30 CZK',
    'Příbuznost CZ 2022',
    'Výhoda CZ 2022',
    'Koncentrace světového trhu 2022',
    'Koncentrace evropského exportu 2022',
    'EU Největší Exportér 2022',
    'Komplexita výrobku 2022',
    'CZ Export 2022 CZK',
    'EU Import 2022 CZK',
    'CZ Import 2022 CZK',
    'Světový export 2022 CZK',
    'EU Export 2022 CZK',
    'EU Světový Podíl 2022 %',
    'CZ Světový Podíl 2022 %',
    'CZ-EU Podíl 2022 %',
    'CZ 2030 Export CZK',
    'CZ Celkový Export 25-30 CZK',
    'EU 2030 Export',
    'EU Celkový Export 25-30 CZK',
    'CAGR 2022-2030 Předpověď',
    'Zdroj',
    'IS_REALCAGR'
]

# Sidebar selection boxes using display names
x_axis_display      = st.sidebar.selectbox("Select X-axis variable", plot_display_names, index=0)
y_axis_display      = st.sidebar.selectbox("Select Y-axis variable", plot_display_names, index=2)
markersize_display  = st.sidebar.selectbox("Select size variable", plot_display_names, index=14)
color_display       = st.sidebar.selectbox("Select color variable", ji_display_names)
hover_info_display  = st.sidebar.multiselect("Select what info should appear on hover", hover_display_data, default='Produkt_HS6')

# Map display names back to column names
x_axis     = display_to_column[x_axis_display]
y_axis     = display_to_column[y_axis_display]
markersize = display_to_column[markersize_display]
color      = display_to_column[color_display]
hover_info = [display_to_column.get(col, col) for col in hover_info_display]

# Sidebar for filtering the color variable
color_values    = df[color].unique()
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

HS_select = st.multiselect("Filter HS6 Codes",filtered_df['Produkt_HS6'])
plotlystyle = st.sidebar.selectbox("Graph style",["plotly_dark","plotly","ggplot2","seaborn","simple_white","none"])
pio.templates.default = plotlystyle
# Define hover data
hover_data = {col: True for col in hover_info}
if HS_select == []:
    fig = px.scatter(filtered_df,
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=color_discrete_map,  # Hard-code the colors
                     labels={x_axis: x_axis_display, y_axis: y_axis_display},
                     title=f'{x_axis_display} vs {y_axis_display} barva podle {color_display}',
                     hover_data=hover_data,
                     height=700,
                     opacity=0.7,
                     size=markersize,
                     size_max=40)

else:
    fig = px.scatter(filtered_df[filtered_df['Produkt_HS6'].isin(HS_select)],
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=color_discrete_map,  # Hard-code the colors
                     labels={x_axis: x_axis_display, y_axis: y_axis_display},
                     title=f'{x_axis_display} vs {y_axis_display} barva podle {color_display}',
                     hover_data=hover_data,
                     height=700,
                     opacity=0.7,
                     size=markersize,
                     size_max=40
                     )

st.plotly_chart(fig)
st.subheader("Big picture:")


st.code("CZ Export 2022: "+ "{:,.0f}".format(sum(filtered_df['CZ_export_2022']))+" CZK\n"+
        "CZ 2025 - 2030 Export: "+ "{:,.0f}".format(sum(filtered_df['CZ_Total_Export_25_30']))+" CZK\n"+
        "EU 2025 - 2030 Export: "+ "{:,.0f}".format(sum(filtered_df['EU_Total_Export_25_30']))+" CZK")


mybuff = StringIO()
fig.write_html(mybuff, include_plotlyjs='cdn')
html_bytes = mybuff.getvalue().encode()
st.download_button(
    label = "Download HTML",
    data = html_bytes,
    file_name = "plot.html",
    mime="text/html"
)