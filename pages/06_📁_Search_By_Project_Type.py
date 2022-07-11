import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(
    page_title="WM | By Project Type",
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
 
msd = st.sidebar.checkbox('View all Multistory Distribution Projects')

if msd:
    df_offices = st.cache(pd.read_csv)(r'R:\ITSupport\PowerBI\Data\Office_Locations.csv', sep=',', header=None)
    df_offices.columns = ["Office", "Address", "City_State", "latitude", "longitude"]
    df_msd = (pd.read_csv)(r'R:\ITSupport\PowerBI\Data\MSD.csv', sep=',', decimal='.', header=None)
    df_msd.columns = ["Project_Number", "Project_Name", "Office", "Organization", "Client", "Project_Manager", "Project_Type", "Project_Type_2", "Site_Plan", "File_Path", "latitude", "longitude", "Status", "Site_Acreage", "F.A.R.", "Parking", "Floors", "Floor_Area_1", "Floor_Area_2", "Floor_Area_3", "Description"]
    df_msd['Floor_Area_3'] = df_msd[['Floor_Area_3']].fillna('*No info in Vantagepoint*')
    df_msd.reset_index(drop=True)
    new = df_msd['Project_Number'].str.split("-", n = 1, expand = True)
    df_msd.loc[0:, 'Get_Year']= new[0]
    df_msd.loc[0:, 'New'] = df_msd["Get_Year"].astype(str).str[-2:]
    df_msd.loc[0:, 'Year'] = pd.to_datetime(df_msd['New'], format="%y")
    df_msd.loc[0:, 'Year'] = df_msd['Year'].dt.year
    df_msd.loc[0:, 'Site_Acreage'] = df_msd['Site_Acreage'].fillna('*No info in Vantagepoint*')
    df_msd.loc[0:, 'F.A.R.'] = df_msd['F.A.R.'].fillna('*No info in Vantagepoint*')
    df_msd.loc[0:, 'Parking'] = df_msd['Parking'].fillna('*No info in Vantagepoint*')
    df_msd.loc[0:, 'Floors'] = df_msd['Floors'].fillna('*No info in Vantagepoint*')
    df_msd.loc[0:, 'Floor_Area_1'] = df_msd['Floor_Area_1'].fillna('*No info in Vantagepoint*')
    df_msd.loc[0:, 'Floor_Area_2'] = df_msd['Floor_Area_2'].fillna('*No info in Vantagepoint*')
    df_msd.loc[0:, 'Floor_Area_3'] = df_msd['Floor_Area_3'].fillna('*No info in Vantagepoint*')
    df_msd.loc[0:, 'Description'] = df_msd['Description'].fillna('*No info in Vantagepoint*')
    del df_msd["Get_Year"]
    del df_msd["New"]

    cd = ['Construction Documents']
    select_cd = df_msd[df_msd['Status'].isin(cd)]
    cs = ['Constructed']
    select_cs = df_msd[df_msd['Status'].isin(cs)]
    uc = ['Under Construction']
    select_uc = df_msd[df_msd['Status'].isin(uc)]
    ucd = ['Under Contract for DWGs']
    select_ucd = df_msd[df_msd['Status'].isin(ucd)]
    st.sidebar.subheader('Use controls below to add data to map')
    select_year_range = reversed(sorted(df_msd['Year'].unique()))
    yearmax = df_msd['Year'].max()
    yearmin = df_msd['Year'].min()
    select_year_slider = st.sidebar.select_slider('Use slider to display year range:', options=select_year_range, value=(yearmax, yearmin))
    startyear, endyear = list(select_year_slider)[0], list(select_year_slider)[1]   
    select_status = sorted(df_msd["Status"].unique())
    select_status_dropdown = st.sidebar.multiselect('Select one or more Status to display data:', select_status, select_status)
    selected_status_year = df_msd[(df_msd.Status.isin(select_status_dropdown)) & ((df_msd.Year <= startyear) & (df_msd.Year >= endyear))]
    view_state = pdk.ViewState(longitude=-95, latitude=40, zoom=3.5, min_zoom=1.5, max_zoom=17, bearing=0, pitch=0)
    view_offices = df_offices[(df_offices.Office.isin(select_status_dropdown))]

    tooltip = {
    "html":
        "<b>Status:</b> {Status} <br/>"
        "<b>Project Number:</b> {Project_Number} <br/>"
        "<b>Site Acreage:</b> {Site_Acreage} <br/>"
        "<b>F.A.R.:</b> {F.A.R.} <br/>"
        "<b>Parking:</b> {Parking} <br/>"
        "<b>Floors:</b> {Floors} <br/>"
        "<b>1st Floor Area:</b> {Floor_Area_1} <br/>"
        "<b>2nd Floor Area:</b> {Floor_Area_2} <br/>"
        "<b>3rd Floor Area:</b> {Floor_Area_3} <br/>"
        "<b>Description:</b> {Description} <br/>",
    "style": {
        "backgroundColor": "3c3835",
        "color": "white",
        }
    }

    cdlay = pdk.Layer(type='ScatterplotLayer', data=select_cd, get_position=["longitude", "latitude"], pickable=True, opacity=1, stroked=True, filled=True, radius_scale=15, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[0, 211, 106], get_line_color=[0, 211, 106])
    cslay = pdk.Layer(type='ScatterplotLayer', data=select_cs, get_position=["longitude", "latitude"], pickable=True, opacity=1, stroked=True, filled=True, radius_scale=15, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[224, 68, 3], get_line_color=[224, 68, 3])
    uclay = pdk.Layer(type='ScatterplotLayer', data=select_uc, get_position=["longitude", "latitude"], pickable=True, opacity=1, stroked=True, filled=True, radius_scale=15, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[0, 117, 186], get_line_color=[0, 117, 186])
    ucdlay = pdk.Layer(type='ScatterplotLayer', data=select_ucd, get_position=["longitude", "latitude"], pickable=True, opacity=1, stroked=True, filled=True, radius_scale=15, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[252, 214, 61], get_line_color=[252, 214, 61])
    # udlay = pdk.Layer(type='ScatterplotLayer', data=df_msd[(df_msd.Status.isin(select_status_dropdown) == 'Under Contract For DWGs') & ((df_msd.Year <= startyear) & (df_msd.Year >= endyear))], get_position=["longitude", "latitude"], pickable=True, opacity=0.5, stroked=True, filled=True, radius_scale=15, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[0, 255, 0], get_line_color=[0, 255, 0])
    # officelay = pdk.Layer(type='ScatterplotLayer', data=view_offices, get_position=["longitude", "latitude"], pickable=False, opacity=0.8, stroked=True, filled=True, radius_scale=20, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[0, 120, 235], get_line_color=[0, 120, 235])
    textlay = pdk.Layer(type="TextLayer", data=df_msd[(df_msd.Status.isin(select_status_dropdown)) & ((df_msd.Year <= startyear) & (df_msd.Year >= endyear))], pickable=True, get_position=["longitude", "latitude"], get_text="name", get_size=300, sizeUnits='meters', get_color=[255, 0, 0], get_angle=0, getTextAnchor= '"middle"', get_alignment_baseline='"bottom"')

    mapstyle = st.sidebar.selectbox('Change Base Map Background:', options=['Atlas', 'Dark Tones', 'Grey Tones', 'Roads', 'Satellite'], index=2)

    if mapstyle == 'Dark Tones':
        pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.MAPBOX_DARK, layers=[cdlay, cslay, uclay, ucdlay, textlay], tooltip=tooltip)
    elif mapstyle == 'Grey Tones':
        pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.LIGHT, layers=[cdlay, cslay, uclay, ucdlay, textlay], tooltip=tooltip)
    elif mapstyle == 'Satellite':
        pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.MAPBOX_SATELLITE, layers=[cdlay, cslay, uclay, ucdlay, textlay], tooltip=tooltip)
    elif mapstyle == 'Roads':
        pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.CARTO_ROAD, layers=[cdlay, cslay, uclay, ucdlay, textlay], tooltip=tooltip)
    elif mapstyle == 'Atlas':
        pp = pdk.Deck(initial_view_state=view_state, map_provider='mapbox', map_style=pdk.map_styles.ROAD, layers=[cdlay, cslay, uclay, ucdlay, textlay], tooltip=tooltip)

    with st.sidebar.expander('About this application', expanded=False):
        st.info('If your project is not appearing, or information is missing, please update the project in Vantagepoint. Either an address or latitude & longitude (in decimal format, not degree/minute/seconds) is required to populate data on the map and data table at right. Updates may take up to 24 hours to post.')
        
    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader('Projects: Multistory Distribution') 
        st.write('Displaying ', str(selected_status_year.shape[0]) + ' of ', str(df_msd.shape[0]) + ' Multistory Distribution Projects On Map & Chart Below')
        st.pydeck_chart(pp)
                
    with col2:
        st.subheader('Insights: Multistory Distribution')
        rb1 = st.radio(label = 'Select Chart Type:', options = ['Horizontal','Vertical'], index=1); st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if rb1 == 'Horizontal':
            fig1 = px.histogram(selected_status_year, y='Year', color_discrete_sequence=['rgb(224,68,3)'], text_auto=True)
            fig1.update_layout(bargap=0.3)
            fig1.update_layout(barmode='relative')
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig1.update_xaxes(categoryorder='category ascending')
            fig1.update_layout(xaxis={'visible': False, 'showticklabels': False})
        elif rb1 == 'Vertical':
            fig1 = px.histogram(selected_status_year, x='Year', color_discrete_sequence=['rgb(224,68,3)'], text_auto=True)
            fig1.update_layout(bargap=0.3)
            fig1.update_layout(barmode='relative')
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig1.update_yaxes(categoryorder='category ascending')
            fig1.update_layout(yaxis={'visible': False, 'showticklabels': False})
        st.plotly_chart(fig1, use_container_width=True)
        
    col3, col4 = st.columns([2,1])

    with col3:
        st.write('🟠 = Constructed, 🟢 = Construction Documents, 🔵 = Under Construction, 🟡 = Under Contract for Drawings')
        gb = GridOptionsBuilder.from_dataframe(selected_status_year.reset_index(drop=True))
        gb.configure_pagination(paginationPageSize=20)
        gridOptions = gb.build()
        AgGrid(selected_status_year.reset_index(drop=True), gridOptions=gridOptions)

    with col4:
        rb = st.radio(label = 'Multistory Distribution Information by:', options = ['By Office','By Floors','By Year'], index=0)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if rb == 'By Office':
            fig2 = px.sunburst(data_frame=selected_status_year, path=["Office", 'Floors', 'Year'], color="Office", color_discrete_sequence=['rgb(224,68,3)'])
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        elif rb == 'By Floors':
            fig2 = px.sunburst(data_frame=selected_status_year, path=["Floors", 'Office', 'Year'], color="Floors", color_discrete_sequence=['rgb(224,68,3)'])
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        elif rb == 'By Year':
            fig2 = px.sunburst(data_frame=selected_status_year, path=["Year", 'Office', 'Floors'], color="Year", color_discrete_sequence=['rgb(224,68,3)'])
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

else:
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
    new = df['Project_Number'].str.split("-", n = 1, expand = True) 
    df.loc[0:, 'Get_Year']= new[0]
    df.loc[0:8183, 'Old'] = df["Get_Year"].astype(str).str[:2]
    df.loc[8184:, 'New'] = df["Get_Year"].astype(str).str[-2:]
    df.loc[0:, 'Year'] = df["Old"].str.cat(df[["New"]], na_rep='')
    df.loc[0:, 'Year'] = pd.to_datetime(df['Year'], format="%y")
    df.loc[0:, 'Year'] = df['Year'].dt.year
    df.loc[0:, 'Old'] = df['Old'].fillna('*No info in Vantagepoint*')
    df.loc[0:, 'New'] = df['New'].fillna('*No info in Vantagepoint*')
    del df["Get_Year"]
    del df["Old"]
    del df["New"]
    df = df.dropna()

    st.sidebar.subheader('Use controls below to add data to map')
    select_year_range = reversed(sorted(df['Year'].unique()))
    yearmax = df['Year'].max()
    yearmin = df['Year'].min()
    select_year_slider = st.sidebar.select_slider('Use slider to display year range:', options=select_year_range, value=(yearmax, yearmin))
    startyear, endyear = list(select_year_slider)[0], list(select_year_slider)[1]   
    select_projtype = sorted(df["Project_Type"].unique())
    select_projtype_dropdown = st.sidebar.multiselect('Select one or more Project Types to display data:', select_projtype)
    selected_projtype_year = df[(df.Project_Type.isin(select_projtype_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))]
    # select_projtype2 = sorted(df["Project_Type_2"].unique())
    # select_projtype2_dropdown = st.sidebar.multiselect('Select one or more Project Types 2 to display data:', select_projtype2)
    # selected_projtype2_year = df[(df.Project_Type_2.isin(select_projtype2_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))]
    view_state = pdk.ViewState(longitude=-100.10, latitude=35, zoom=2.5, min_zoom=1.5, max_zoom=17, bearing=0, pitch=0)
    view_offices = df_offices[(df_offices.Office.isin(select_projtype_dropdown))]

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

    splay = pdk.Layer(type='ScatterplotLayer', data=df[(df.Project_Type.isin(select_projtype_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))], get_position=["longitude", "latitude"], pickable=True, opacity=0.5, stroked=True, filled=True, radius_scale=15, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[224, 68, 3], get_line_color=[224, 68, 3])
    officelay = pdk.Layer(type='ScatterplotLayer', data=view_offices, get_position=["longitude", "latitude"], pickable=False, opacity=0.8, stroked=True, filled=True, radius_scale=20, radius_min_pixels=5, radius_max_pixels=100, line_width_min_pixels=1, get_fill_color=[0, 120, 235], get_line_color=[0, 120, 235])
    textlay = pdk.Layer(type="TextLayer", data=df[(df.Office.isin(select_projtype_dropdown)) & ((df.Year <= startyear) & (df.Year >= endyear))], pickable=True, get_position=["longitude", "latitude"], get_text="name", get_size=300, sizeUnits='meters', get_color=[0, 0, 0], get_angle=0, getTextAnchor= '"middle"', get_alignment_baseline='"bottom"')

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
        st.subheader('Projects: By Type & Year Selected') 
        st.write('Displaying ', str(selected_projtype_year.shape[0]) + ' of ', str(df.shape[0]) + ' Projects On Map & Chart Below')
        st.pydeck_chart(pp)
                
    with col2:
        st.subheader('Insights: Project Type & Year Selected')
        rb1 = st.radio(label = 'Select Chart Type:', options = ['Horizontal','Vertical'], index=0); st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if rb1 == 'Horizontal':
            fig1 = px.histogram(selected_projtype_year, y='Year', color_discrete_sequence=['rgb(224,68,3)'], text_auto=True)
            fig1.update_layout(bargap=0.3)
            fig1.update_layout(barmode='relative')
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig1.update_xaxes(categoryorder='category ascending')
            fig1.update_layout(xaxis={'visible': False, 'showticklabels': False})
        elif rb1 == 'Vertical':
            fig1 = px.histogram(selected_projtype_year, x='Year', color_discrete_sequence=['rgb(224,68,3)'], text_auto=True)
            fig1.update_layout(bargap=0.3)
            fig1.update_layout(barmode='relative')
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig1.update_yaxes(categoryorder='category ascending')
            fig1.update_layout(yaxis={'visible': False, 'showticklabels': False})
        st.plotly_chart(fig1, use_container_width=True)
        
    col3, col4 = st.columns([2,1])

    with col3:
        st.write('🟠 markers denote project locations & 🔵 markers denote Ware Malcomb office location(s).')
        gb = GridOptionsBuilder.from_dataframe(selected_projtype_year.reset_index(drop=True))
        gb.configure_pagination(paginationPageSize=20)
        gridOptions = gb.build()
        AgGrid(selected_projtype_year.reset_index(drop=True), gridOptions=gridOptions)

    with col4:
        rb = st.radio(label = 'Project Types by:', options = ['By Project Type','By Office','By Org','By Year'], index=0)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if rb == 'By Project Type':
            fig2 = px.sunburst(data_frame=selected_projtype_year, path=["Project_Type", 'Office', 'Organization'], color="Project_Type", color_discrete_sequence=['rgb(224,68,3)'],)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        elif rb == 'By Office':
            fig2 = px.sunburst(data_frame=selected_projtype_year, path=["Office", 'Organization', 'Project_Type'], color="Office", color_discrete_sequence=['rgb(224,68,3)'],)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        elif rb == 'By Org':
            fig2 = px.sunburst(data_frame=selected_projtype_year, path=["Organization", 'Office', 'Project_Type'], color="Organization", color_discrete_sequence=['rgb(224,68,3)'],)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        elif rb == 'By Year':
            fig2 = px.sunburst(data_frame=selected_projtype_year, path=["Year", 'Office', 'Organization', 'Project_Type'], color="Year", color_discrete_sequence=px.colors.sequential.RdBu)
            fig2.update_layout(xaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(yaxis={'visible': False, 'showticklabels': False})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)