import streamlit as st
import pandas as pd
import pydeck as pdk
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(
    page_title="WM | By Project Number",
    page_icon="https://www.waremalcomb.com/wp-content/themes/wm4.75/img/favicon/favicon-16x16.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after{visibility: visible; content: 'Powered by Ware Malcomb IT and Copyright Ⓒ Ware Malcomb 2022'; display:block; position:relative; color:#3c3835;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("""
<style>
    header[data-testid="stHeader"] {background: none;}
</style>
""",unsafe_allow_html=True,)

st.markdown("""
<style>
    .css-18e3th9 {margin-top: -6rem;
    }
</style>
""",unsafe_allow_html=True,)

st.image("data/anniversary_small.png", width=400)
 
df_offices = st.cache(pd.read_csv)(r'R:\ITSupport\PowerBI\Data\Office_Locations.csv', sep=',', header=None)
df_offices.columns = ["Office", "Address", "City_State", "latitude", "longitude"]
df_og = st.cache(pd.read_csv)(r'R:\ITSupport\PowerBI\Data\ProjectGIS.csv', sep=',', decimal='.', header=None)
df_og.columns = ["Project_Number", "Project_Name", "Office", "Organization", "Client", "Project_Manager", "Project_Type", "Project_Type_2", "Site_Plan", "File_Path", "latitude", "longitude"]
df = df_og[~df_og['Project_Number'].isin(['BLACKW112006', '201 ODGEN - SUITE 100', 'PRI-6008-04', 'TEST', 'IRVIMPROVMNTS', 'INTSTUDIO', 'BUILDING MASTER'])]
df.loc[0:, "Organization"].replace({"00-Do not use": "*No info in Vantagepoint*"}, inplace=True)
df.loc[0:, "Office"].replace({"Corporate": "Irvine", "Default": "Irvine", "Graphic Design": "Irvine"}, inplace=True)
df.loc[0:, "Project_Number"].replace({"PRI7-6014-01": "PRI17-6014-01", "ETW II – 6TH FLOOR WASHROOMS": "CHI12-6036-C5", "ETW II – SUITE 220": "CHI12-6036-C1", "73-629-02": "973-629-02", "CHD7-6019-24": "CHD17-6019-24"}, inplace=True)
df["Project_Name"].replace({"CHI12-6036-C5": "ETW II – 6TH FLOOR WASHROOMS", "CHI12-6036-C1": "ETW II – SUITE 220"}, inplace=True)
df[['Project_Type', 'Project_Type_2', 'Site_Plan', 'File_Path']] = df[['Project_Type', 'Project_Type_2', 'Site_Plan', 'File_Path']].fillna('*No info in Vantagepoint*')
df.reset_index(drop=True)
df = df.dropna()

st.sidebar.subheader('Use controls below to add data to map')
select_projnum = sorted(df["Project_Number"].unique())
select_projnum_dropdown = st.sidebar.multiselect('Start typing below to autofill:', select_projnum)
selected_projnum_year = df[(df.Project_Number.isin(select_projnum_dropdown))]
view_state = pdk.ViewState(longitude=-100.10, latitude=35, zoom=2.5, min_zoom=1.5, max_zoom=17, bearing=0, pitch=0)
view_offices = df_offices[(df_offices.Office.isin(select_projnum_dropdown))]

tooltip = {
"html":
    "<b>Project Number:</b> {Project_Number} <br/>"
    "<b>Office:</b> {Office} <br/>"
    "<b>Client:</b> {Client} <br/>"
    "<b>Project Name:</b> {Project_Name} <br/>"
    "<b>Path:</b> {File_Path} <br/>",
"style": {
    "backgroundColor": "3c3835",
    "color": "white",
    }
}

splay = pdk.Layer(type='ScatterplotLayer', data=df[(df.Project_Number.isin(select_projnum_dropdown))], get_position=["longitude", "latitude"], pickable=True, opacity=0.5, stroked=True, filled=True, radius_scale=15, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[224, 68, 3], get_line_color=[224, 68, 3])
officelay = pdk.Layer(type='ScatterplotLayer', data=view_offices, get_position=["longitude", "latitude"], pickable=False, opacity=0.8, stroked=True, filled=True, radius_scale=20, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[0, 120, 235], get_line_color=[0, 120, 235])
textlay = pdk.Layer(type="TextLayer", data=df[(df.Project_Number.isin(select_projnum_dropdown))], pickable=True, get_position=["longitude", "latitude"], get_text="name", get_size=300, sizeUnits='meters', get_color=[0, 0, 0], get_angle=0, getTextAnchor= '"middle"', get_alignment_baseline='"bottom"')

mapstyle = st.sidebar.selectbox('Change Base Map Background:', options=['Atlas', 'Dark Tones', 'Grey Tones', 'Roads', 'Satellite'], index=3)

if mapstyle == 'Dark Tones':
    pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.MAPBOX_DARK, layers=[splay, officelay, textlay], tooltip=tooltip)
elif mapstyle == 'Grey Tones':
    pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.LIGHT, layers=[splay, officelay, textlay], tooltip=tooltip)
elif mapstyle == 'Satellite':
    pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.MAPBOX_SATELLITE, layers=[splay, officelay, textlay], tooltip=tooltip)
elif mapstyle == 'Roads':
    pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.CARTO_ROAD, layers=[splay, officelay, textlay], tooltip=tooltip)
elif mapstyle == 'Atlas':
    pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.ROAD, layers=[splay, officelay, textlay], tooltip=tooltip)

with st.sidebar.expander('About this application', expanded=False):
    st.info('If your project is not appearing, or information is missing, please update the project in Vantagepoint. Either an address or latitude & longitude (in decimal format, not degree/minute/seconds) is required to populate data on the map and data table at right. Updates may take up to 24 hours to post.')
    
col1, col2 = st.columns([2,1])

with col1:
    st.subheader('Search By Project Number') 
    st.write('Displaying ', str(selected_projnum_year.shape[0]) + ' of ', str(df.shape[0]) + ' Project(s) On Map Below')
    st.pydeck_chart(pp)
    
col3, col4 = st.columns([2,1])

with col3:
    st.write('🟠 marker denotes project location by project number.')
    gb = GridOptionsBuilder.from_dataframe(selected_projnum_year.reset_index(drop=True))
    gb.configure_pagination(paginationPageSize=20)
    gridOptions = gb.build()
    AgGrid(selected_projnum_year.reset_index(drop=True), gridOptions=gridOptions)