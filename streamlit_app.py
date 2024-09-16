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
    # Doprava (Transportation) - Various shades of orange/red
    'A02. Doprava': '#E63946',  # Bright red for transportation in general
    'A02c. Cyklistika a jednostopá': '#FF6F61',  # Lighter red for cycling
    'A02a. Železniční (osobní i nákladní)': '#C0362C',  # Deep red for railways
    'Nové lokomotivy a vozy': '#FF8B74',  # Lighter shade for new trains

    # Budovy (Buildings) - Shades of brown and earth tones
    'A03. Budovy': '#8D8741',  # Earthy brown for buildings
    'A03a. Snižování energetické náročnosti budov': '#BDB76B',  # Olive green for energy efficiency
    'Zateplení, izolace': '#A1887F',  # Soft brown for insulation
    'A03b. Elektrifikace tepelného hospodářství': '#D4A373',  # Lighter brown for heat management
    'A03b. Elektrifikace domácností': '#F4A261',  # Warm tone for household electrification

    # Výroba nízkoemisní elektřiny a paliv (Low-emission energy & fuels) - Green/Blue palette
    'A04. Výroba nízkoemisní elektřiny a paliv': '#2A9D8F',  # Green for clean energy production
    'A04a. Větrná': '#3AAFA9',  # Turquoise for wind energy
    'A04b. Solární': '#E9C46A',  # Yellow for solar energy
    'A04c. Vodní': '#0096C7',  # Blue for hydro energy
    'A04f. Jádro': '#264653',  # Dark blue for nuclear
    'A04g. Efektivní využití plynu a vodíku': '#00B4D8',  # Light blue for gas and hydrogen
    'Komponenty pro větrnou energetiku': '#48CAE4',  # Sky blue for wind components
    'Komponenty pro solární energetiku': '#F4A261',  # Orange for solar components
    'Komponenty pro vodní energetiku': '#0096C7',  # Blue for water components
    'Komponenty pro jadernou energetiku': '#264653',  # Nuclear components

    # Ukládání energie (Energy storage) - Purples for storage and related technology
    'A05. Ukládání energie': '#9B5DE5',  # Purple for energy storage
    'A05a. Baterie': '#D45D79',  # Magenta for batteries
    'A05b. Vodik a čpavek': '#7209B7',  # Deep purple for hydrogen storage
    'A05c. Ostatní ukládání': '#3A0CA3',  # Dark purple for other storage
    'Ostatní ukládání (přečerpávací vodní, ohřátá voda,…)': '#7B2CBF',  # Storage alternatives

    # Energetické sítě (Energy networks) - Dark greens
    'A06. Energetické sítě': '#2C6E49',  # Dark green for energy grids
    'A06a. Distribuce a přenos elektřiny': '#377771',  # Medium green for distribution
    'Transformační stanice a další síťové komponenty': '#55A630',  # Bright green for components

    # Měření a diagnostické přístroje (Measurement and diagnostics) - Blues and teals
    'E01. Měřící a diagnostické přístroje; Monitoring': '#4A90E2',  # Light blue for measurement
    'E01a. Optická měření (HS 9000 - 9013, HS 903140)': '#00B4D8',  # Light blue for optical measurements
    'E0f. Měření v energetice a síťových odvětvích (HS9028 - 9030, 903210)': '#0077B6',  # Blue for energy measurements
    'E01c. Měření okolního prostředí (HS9025)': '#2A9D8F',  # Greenish-blue for environment measurement
    'E01d. Měření vlastností plynů a tekutin (HS9026)': '#168AAD',  # Aqua for gas and liquid measurement
    'E01e. Chemická analýza (HS9027)': '#9C89B8',  # Light purple for chemical analysis
    'E01h. Surveying / Zeměměřičství (HS 9015)': '#4C3A51',  # Dark purple for surveying
    'Surveying / Zeměměřičství': '#4C3A51',  # Same for consistency
    'E01i. Ostatní (HS 903x, a další)': '#757575',  # Grey for "Other" category

    # Cirkularita a odpady (Circularity and waste) - Browns and earthy tones
    'B02. Cirkularita a odpady': '#6A994E',  # Greenish brown for circularity
    'B02b. Cirkularita, využití odpadu': '#8A9A5B',  # Olive green for waste use
    'Materiálové využití': '#8D8741',  # Brown for material use

    # Výroba (Low-emission manufacturing) - Shades of gray and steel tones
    'A01. Výroba, nízkoemisní výrobní postupy': '#5C5C5C',  # Steel gray for manufacturing
    'A01a. Nízkoemisní výroba': '#4F4F4F',  # Darker gray for low-emission manufacturing
    'A01c. Elektrifikace výrobních postupů': '#6E6E6E',  # Lighter gray for electrification of processes
    'Elektrifikace ve výrobě': '#8A8D8F',  # Light gray for manufacturing electrification
    'Nízkoemisní výroby ostatní': '#555555',  # Dark steel gray for other low-emission production

    # Miscellaneous
    'Díly a vybavení': '#FFBF69',  # Peach for parts and equipment
    'Termostaty': '#F28F3B',  # Orange for thermostats
    'Termometry': '#F4A261',  # Light orange for thermometers
    'Spektrometry': '#B5838D',  # Muted purple for spectrometry
    'Měření ionizujícího záření': '#B5179E',  # Bright pink for radiation measurement
    'Osciloskopy': '#7209B7',  # Purple for oscilloscopes
    'Měření odběru a výroby plynů, tekutin, elektřiny': '#457B9D',  # Light blue for gas and fluid measurement
    'Chromatografy': '#B07D62',  # Warm brown for chromatography
    'Domácí elektrické spotřebiče': '#F4A261',  # Warm orange for household appliances
    'Hydrometry': '#0096C7',  # Blue for hydrometry
    'Ostatní': '#6D6875',  # Neutral gray for "other"
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
st.text(color_values)
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