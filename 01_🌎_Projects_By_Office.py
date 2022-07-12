import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

st.set_page_config(
    page_title="WM | Projects By Office",
    page_icon="https://www.waremalcomb.com/wp-content/themes/wm4.75/img/favicon/favicon-16x16.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

hide_st_style = """
            <style>
            MainMenu {visibility: visbile;}
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

df_offices = (pd.read_csv)(r'R:\ITSupport\PowerBI\Data\Office_Locations.csv', sep=',', header=None)
df_offices.columns = ["Office", "Address", "City_State", "latitude", "longitude"]
df_og = st.cache(pd.read_csv)(r'R:\ITSupport\PowerBI\Data\ProjectGIS.csv', sep=',', decimal='.', header=None)
df_og.columns = ["Project_Number", "Project_Name", "Office", "Organization", "Client", "Project_Manager", "Project_Type", "Project_Type_2", "Site_Plan", "File_Path", "latitude", "longitude"]
df = df_og[~df_og['Project_Number'].isin(['BLACKW112006', '201 ODGEN - SUITE 100', 'PRI-6008-04', 'TEST', 'IRVIMPROVMNTS', 'INTSTUDIO', 'BUILDING MASTER'])]
df["Organization"].replace({"00-Do not use": "*No info in Vantagepoint*"}, inplace=True)
df["Office"].replace({"Corporate": "Irvine", "Default": "Irvine", "Graphic Design": "Irvine"}, inplace=True)
df["Project_Number"].replace({"PRI7-6014-01": "PRI17-6014-01", "ETW II – 6TH FLOOR WASHROOMS": "CHI12-6036-C5", "ETW II – SUITE 220": "CHI12-6036-C1", "73-629-02": "973-629-02", "CHD7-6019-24": "CHD17-6019-24"}, inplace=True)
df["Project_Name"].replace({"CHI12-6036-C5": "ETW II – 6TH FLOOR WASHROOMS", "CHI12-6036-C1": "ETW II – SUITE 220"}, inplace=True)
df[['Project_Type', 'Project_Type_2', 'Site_Plan', 'File_Path']] = df[['Project_Type', 'Project_Type_2', 'Site_Plan', 'File_Path']].fillna('*No info in Vantagepoint*')
df.reset_index(drop=True)
new = df["Project_Number"].str.split("-", n = 1, expand = True) 
df.loc[0:, "Get_Year"]= new[0]
df.loc[0:8183, 'Old'] = df["Get_Year"].astype(str).str[:2]
df.loc[8184:, 'New'] = df["Get_Year"].astype(str).str[-2:]
df.loc[0:, "Year"] = df["Old"].str.cat(df[["New"]], na_rep='')
df.loc[0:, 'Year'] = pd.to_datetime(df['Year'], format="%y")
df.loc[0:, 'Year'] = df['Year'].dt.year
df.loc[0:, "Country"] = df.loc[0:, "Office"]
df.loc[0:, "Country"].replace({"Toronto": "All Canada Offices", "Vaughan": "All Canada Offices", "Ottawa": "All Canada Offices"}, inplace=True)
df.loc[0:, "Country"].replace({"MEX-US": "All Mexico Offices", "Mexico": "All Mexico Offices", "Monterrey": "All Mexico Offices"}, inplace=True)
df.loc[0:, "Country"].replace({"PAN-US": "All South America Offices", "Panama": "All South America Offices", "Sao Paulo": "All South America Offices"}, inplace=True)
df.loc[0:, "Country"].replace({"Atlanta": "All US Offices", "Chicago": "All US Offices", "Chicago Downtown": "All US Offices", "Columbus": "All US Offices", "Dallas": "All US Offices", "Denver": "All US Offices", "Denver Civil": "All US Offices", "Houston": "All US Offices", "Inland Empire": "All US Offices", "Irvine": "All US Offices", "Los Angeles": "All US Offices", "Miami": "All US Offices", "Nashville": "All US Offices", "New Jersey": "All US Offices", "New York": "All US Offices", "Northern California": "All US Offices", "Phoenix": "All US Offices", "Princeton": "All US Offices", "Sacramento": "All US Offices", "San Diego": "All US Offices", "San Diego Downtown": "All US Offices", "San Francisco": "All US Offices", "Seattle": "All US Offices", "Washington D.C.": "All US Offices"}, inplace=True)
df_offices["Country"] = df_offices.loc[0:, "Office"]
df_offices["Country"].replace({"Toronto": "All Canada Offices", "Vaughan": "All Canada Offices", "Ottawa": "All Canada Offices"}, inplace=True)
df_offices["Country"].replace({"MEX-US": "All Mexico Offices", "Mexico": "All Mexico Offices", "Monterrey": "All Mexico Offices"}, inplace=True)
df_offices["Country"].replace({"Atlanta": "All US Offices", "Chicago": "All US Offices", "Chicago Downtown": "All US Offices", "Columbus": "All US Offices", "Dallas": "All US Offices", "Denver": "All US Offices", "Denver Civil": "All US Offices", "Houston": "All US Offices", "Inland Empire": "All US Offices", "Irvine": "All US Offices", "Los Angeles": "All US Offices", "Miami": "All US Offices", "Nashville": "All US Offices", "New Jersey": "All US Offices", "New York": "All US Offices", "Northern California": "All US Offices", "Phoenix": "All US Offices", "Princeton": "All US Offices", "Sacramento": "All US Offices", "San Diego": "All US Offices", "San Diego Downtown": "All US Offices", "San Francisco": "All US Offices", "Seattle": "All US Offices", "Washington D.C.": "All US Offices"}, inplace=True)
df_offices["Country"].replace({"PAN-US": "All South America Offices", "Panama": "All South America Offices", "Sao Paulo": "All South America Offices"}, inplace=True)
df[['Old']] = df[['Old']].fillna('*No info in Vantagepoint*')
df[['New']] = df[['New']].fillna('*No info in Vantagepoint*')
del df["Get_Year"]
del df["Old"]
del df["New"]
df = df.dropna()
st.session_state['df'] = df
st.session_state['df_offices'] = df_offices

country = st.sidebar.checkbox('View Projects By Countries & Year')
st.sidebar.subheader('Use controls below to add data to map')

if country:
    select_year_range = reversed(sorted(df['Year'].unique()))
    yearmax = df['Year'].max()
    yearmin = df['Year'].min()
    select_year_slider = st.sidebar.select_slider('Use slider to display year range:', options=select_year_range, value=(yearmax, yearmin))
    startyear, endyear = list(select_year_slider)[0], list(select_year_slider)[1]
    select_country = sorted(df["Country"].unique())
    select_country_dropdown = st.sidebar.multiselect('Select one or multiple countries to display data:', select_country)
    selected_country_year = df[(df.Country.isin(select_country_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))]
    view_state = pdk.ViewState(longitude=-81.25, latitude=17.00, zoom=2, min_zoom=1.5, max_zoom=17, bearing=0, pitch=0)
    view_offices_country = df_offices[(df_offices.Country.isin(select_country_dropdown))]

    tooltip = {
    "html":
        "<b>Project Number:</b> {Project_Number} <br/>"
        "<b>Office:</b> {Office} <br/>"
        "<b>Client:</b> {Client} <br/>"
        "<b>Project Type:</b> {Project_Type} <br/>"
        "<b>Path:</b> {File_Path} <br/>",
    "style": {
        "backgroundColor": "3c3835",
        "color": "white",
        }
    }

    splay = pdk.Layer(type='ScatterplotLayer', data=df[(df.Country.isin(select_country_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))], get_position=["longitude", "latitude"], pickable=True, opacity=0.5, stroked=True, filled=True, radius_scale=15, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[208, 80, 43], get_line_color=[208, 80, 43])
    officelay = pdk.Layer(type='ScatterplotLayer', data=view_offices_country, get_position=["longitude", "latitude"], pickable=False, opacity=0.8, stroked=True, filled=True, radius_scale=20, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[0, 120, 235], get_line_color=[0, 120, 235])
    textlay = pdk.Layer(type="TextLayer", data=df[(df.Country.isin(select_country_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))], get_position=["longitude", "latitude"], get_text="name", get_size=300, sizeUnits='meters', get_color=[0, 0, 0], get_angle=0, getTextAnchor= '"middle"', get_alignment_baseline='"bottom"')

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
        
    fig1 = px.histogram(selected_country_year, x='Year', color_discrete_sequence=['rgb(224,68,3)'])
    fig1.update_layout(bargap=0.3)
    fig1.update_layout(barmode='stack')
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig1.update_yaxes(categoryorder='category descending')

    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader('Projects: Country & Year Selected') 
        st.write('Displaying ', str(selected_country_year.shape[0]) + ' of ', str(df.shape[0]) + ' Projects On Map & Chart Below')
        st.pydeck_chart(pp)
                
    with col2:
        st.subheader('Insights: Country & Year Selected')
        rb1 = st.radio(label = 'Select chart layout style:', options = ['Horizontal','Vertical'], index=0); st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if rb1 == 'Horizontal':
            fig1 = px.histogram(selected_country_year, y='Year', color_discrete_sequence=['rgb(224,68,3)'], text_auto=True)
            fig1.update_layout(bargap=0.3)
            fig1.update_layout(barmode='relative')
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig1.update_xaxes(categoryorder='category ascending')
            fig1.update_layout(xaxis={'visible': False, 'showticklabels': False})
        elif rb1 == 'Vertical':
            fig1 = px.histogram(selected_country_year, x='Year', color_discrete_sequence=['rgb(224,68,3)'], text_auto=True)
            fig1.update_layout(bargap=0.3)
            fig1.update_layout(barmode='relative')
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig1.update_yaxes(categoryorder='category ascending')
            fig1.update_layout(yaxis={'visible': False, 'showticklabels': False})
        st.plotly_chart(fig1, use_container_width=True)

    col3, col4 = st.columns([2,1])

    with col3:
        st.write('🟠 markers denote project locations & 🔵 markers denote Ware Malcomb office location(s).')
        gb = GridOptionsBuilder.from_dataframe(selected_country_year.reset_index(drop=True))
        gb.configure_pagination(paginationPageSize=20)
        gridOptions = gb.build()
        AgGrid(selected_country_year.reset_index(drop=True), gridOptions=gridOptions)

    with col4:
        rb = st.radio(label = 'Select chart layout style:', options = ['By Country','By Org','By Year'], index=0)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if rb == 'By Country':
            fig2 = px.sunburst(data_frame=selected_country_year, path=["Country", 'Organization', 'Project_Type'], color="Country", color_discrete_sequence=['rgb(224,68,3)'],)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        elif rb == 'By Org':
            fig2 = px.sunburst(data_frame=selected_country_year, path=["Organization", 'Country', 'Office', 'Project_Type'], color="Organization", color_discrete_sequence=['rgb(224,68,3)'],)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        elif rb == 'By Year':
            fig2 = px.sunburst(data_frame=selected_country_year, path=["Year", 'Country', 'Office', 'Organization', 'Project_Type'], color="Year", color_discrete_sequence=px.colors.sequential.RdBu_r)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

else:
    select_year_range = reversed(sorted(df['Year'].unique()))
    yearmax = df['Year'].max()
    yearmin = df['Year'].min()
    select_year_slider = st.sidebar.select_slider('Use slider to display year range:', options=select_year_range, value=(yearmax, yearmin))
    startyear, endyear = list(select_year_slider)[0], list(select_year_slider)[1]   
    select_office = sorted(df["Office"].unique())
    select_office_dropdown = st.sidebar.multiselect('Select one or more office(s) to display project data:', select_office)
    selected_office_year = df[(df.Office.isin(select_office_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))]
    view_state = pdk.ViewState(longitude=-100.10, latitude=35, zoom=2.5, min_zoom=1.5, max_zoom=17, bearing=0, pitch=0)
    view_offices = df_offices[(df_offices.Office.isin(select_office_dropdown))]

    tooltip = {
    "html":
        "<b>Project Number:</b> {Project_Number} <br/>"
        "<b>Office:</b> {Office} <br/>"
        "<b>Client:</b> {Client} <br/>"
        "<b>Project Type:</b> {Project_Type} <br/>"
        "<b>Path:</b> {File_Path} <br/>",
    "style": {
        "backgroundColor": "3c3835",
        "color": "white",
        }
    }

    splay = pdk.Layer(type='ScatterplotLayer', data=df[(df.Office.isin(select_office_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))], get_position=["longitude", "latitude"], pickable=True, opacity=0.5, stroked=True, filled=True, radius_scale=15, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[224, 68, 3], get_line_color=[224, 68, 3])
    officelay = pdk.Layer(type='ScatterplotLayer', data=view_offices, get_position=["longitude", "latitude"], pickable=False, opacity=0.8, stroked=True, filled=True, radius_scale=20, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[0, 120, 235], get_line_color=[0, 120, 235])
    textlay = pdk.Layer(type="TextLayer", data=df[(df.Office.isin(select_office_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))], pickable=True, get_position=["longitude", "latitude"], get_text="name", get_size=300, sizeUnits='meters', get_color=[0, 0, 0], get_angle=0, getTextAnchor= '"middle"', get_alignment_baseline='"bottom"')

    mapstyle = st.sidebar.selectbox('Change Base Map Background:', options=['Atlas', 'Dark Tones', 'Grey Tones', 'Roads', 'Satellite'], index=3)

    if mapstyle == 'Dark Tones':
        pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.CARTO_DARK, layers=[splay, officelay, textlay], tooltip=tooltip)
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
    with st.sidebar.expander('Frequently asked questions', expanded=False):
        st.info('If your project is not appearing, or information is missing, please update the project in Vantagepoint. Either an address or latitude & longitude (in decimal format, not degree/minute/seconds) is required to populate data on the map and data table at right. Updates may take up to 24 hours to post.')
    with st.sidebar.expander('Help', expanded=False):
        st.info('If your project is not appearing, or information is missing, please update the project in Vantagepoint. Either an address or latitude & longitude (in decimal format, not degree/minute/seconds) is required to populate data on the map and data table at right. Updates may take up to 24 hours to post.')

    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader('Projects: Office & Year Selected') 
        st.write('Displaying ', str(selected_office_year.shape[0]) + ' of ', str(df.shape[0]) + ' Projects On Map & Chart Below')
        st.pydeck_chart(pp)
                
    with col2:
        st.subheader('Insights: Office & Year Selected')
        rb1 = st.radio(label = 'Select chart layout style:', options = ['Horizontal','Vertical'], index=0); st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if rb1 == 'Horizontal':
            fig1 = px.histogram(selected_office_year, y='Year', color_discrete_sequence=['rgb(224,68,3)'], text_auto=True)
            fig1.update_layout(bargap=0.3)
            fig1.update_layout(barmode='relative')
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig1.update_xaxes(categoryorder='category ascending')
            fig1.update_layout(xaxis={'visible': False, 'showticklabels': False})
        elif rb1 == 'Vertical':
            fig1 = px.histogram(selected_office_year, x='Year', color_discrete_sequence=['rgb(224,68,3)'], text_auto=True)
            fig1.update_layout(bargap=0.3)
            fig1.update_layout(barmode='relative')
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig1.update_yaxes(categoryorder='category ascending')
            fig1.update_layout(yaxis={'visible': False, 'showticklabels': False})
        st.plotly_chart(fig1, use_container_width=True)
        
    col3, col4 = st.columns([2,1])

    with col3:
        st.write('🟠 markers denote project locations & 🔵 markers denote Ware Malcomb office location(s).')
        gb = GridOptionsBuilder.from_dataframe(selected_office_year.reset_index(drop=True))
        gb.configure_pagination(paginationPageSize=20)
        # gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children")
        gridOptions = gb.build()
        AgGrid(selected_office_year.reset_index(drop=True), gridOptions=gridOptions)

    with col4:
        rb = st.radio(label = 'Select chart layout style:', options = ['By Office','By Org','By Year'], index=0)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if rb == 'By Office':
            fig2 = px.sunburst(data_frame=selected_office_year, path=["Office", 'Organization', 'Project_Type'], color="Office", color_discrete_sequence=['rgb(224,68,3)'],)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        elif rb == 'By Org':
            fig2 = px.sunburst(data_frame=selected_office_year, path=["Organization", 'Office', 'Project_Type'], color="Organization", color_discrete_sequence=['rgb(224,68,3)'],)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        elif rb == 'By Year':
            fig2 = px.sunburst(data_frame=selected_office_year, path=["Year", 'Office', 'Organization', 'Project_Type'], color="Year", color_discrete_sequence=px.colors.sequential.RdBu)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)