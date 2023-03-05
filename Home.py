import pandas as pd
import streamlit as st
import plotly_express as px
import base64
import datetime
from datetime import date
from datetime import datetime
from streamlit_extras.echo_expander import echo_expander


# Initial Page Configuration
st.set_page_config(page_title='TEX QA/QC Dashboard',
layout='wide')

# Displaying SFR Logo 
@st.cache_data()
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def build_markup_for_logo(
    png_file,
    background_position="50% 0%",
    margin_top="15%",
    image_width="60%",
    image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )

def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

add_logo("SFR.png")

# Title and Intro Text
st.title('Tshukudu Exploration QA/QC Dashboard')

with st.expander(":pushpin: Click here to learn more"):

    st.write('### This web app allows you to visualise and explore a variety of QA/QC Data.')
    st.write("#### Home")
    st.write("""The Home Page is where csv files containing relevant QA/QC data are uploaded to the webapp. The Sidebar contains two date selectors to allow you to filter your data by date range.
                
        Date Range Selector - the date filter will be applied to all datasets on the respective pages. If you wish to change the date range of your data, 
        simply return to the Home page and reselect the date range.
        Note - the default date range is [2023/01/01 - Today]""")
    st.write("#### Standards")
    st.write("The Standard page allows you to view the performance of Certified Reference Materials (CRMs) using a standard +/- 3 Std Dev Chart. Two drop-down selector boxes allow you to choose a CRM and Element for viewing."
                " A number of dynamic summary cards are displayed below the chart, summarising the perforomance of the selected CRM for the Element in view.")
    st.write("#### Blanks")
    st.write("The Blank page allows you to view the performance of Blank Samples. Two drop-down selector boxes allow you to choose a Blank and Element for viewing."
                " A number of dynamic summary cards are displayed below the chart, summarising the perforomance of the selected Blank for the Element in view.")
    st.write("#### Duplicates")
    st.write("The Duplicates page allows you to view the performance of Duplicate samples, including Field Duplicates, Pulp Duplicates and Lab Duplicates. Two drop-down selector boxes allow you to choose a Duplicate type and Element for viewing."
                " A standard scatter plot is shown to highlight the correlation between primary and QC sample pairs.")
    st.write("#### Lithogeochem")
    st.write("The Lithogeochem page allows you to view the performance of CRMs using a standard +/- 3 Std Dev Chart. Two drop-down selector boxes allow you to choose a CRM and Element for viewing."
                " A number of dynamic summary cards are displayed below the chart, summarising the perforomance of the selected CRM for the Element in view.")
    st.write("#### Surface")
    st.write("The Surface page allows you to view the performance of CRMs used in Soil Sampling programs, using a standard +/- 3 Std Dev Chart. Two drop-down selector boxes allow you to choose a CRM and Element for viewing."
                " A number of dynamic summary cards are displayed below the chart, summarising the perforomance of the selected CRM for the Element in view.")
    st.write("#### Interactive Charts")
    st.write("""Each of the charts used in this webapp are interactive. Hovering over the top right corner of each chart will reveal a number of tools that will allow you to interact with the chart.
            
    Downloading - Each plot can be downloaded by selecting the camera icon in the top right corner        
    Zooming - Zooming in and out on the plot can be done using the zoom buttons or by interactively selecting an area of interest on the plot
    Panning - The Pan tool will allow you to move around within a zoomed plot
    Autoscale - The Autoscale button will return you to the default view encompassing all data
    Hover Info - Hovering your mouse over each data point will reveal sample and assay information        
            """)


# Initialize session state for date range
if 'start' not in st.session_state:
    st.session_state['start'] = date(2023,1,1)

if 'end' not in st.session_state:
    st.session_state['end'] = date(2023,12,31)

# Sidebar Text and Date Selector Components
with st.sidebar:
    st.header(":calendar: Date Range Selector")
    
start_date = st.sidebar.date_input(
    "Start date:",
    date(2023,1,1)
)
  
end_date = st.sidebar.date_input(
    "End date:",
    date.today()
)

# Update date range session states with selected dates
st.session_state.start=start_date
st.session_state.end=end_date

# File Uploader 1
st.subheader('Upload your Standard & Blank Data (vwDHStandardAssays) here:')
upload_file_standards = st.file_uploader('CSV file format required', key = "standards")

# File Previewer 1
with st.expander(":pushpin: File Preview"):
    if upload_file_standards is not None:
        # Read the file to a dataframe using pandas
        df_standardassay = pd.read_csv(upload_file_standards, encoding='latin1', parse_dates=['Assay_Date'], dayfirst=True)

        st.session_state['df_standardassay']=df_standardassay

        st.dataframe(df_standardassay)

# Markdown gap
st.markdown("---")    
    
# File Uploader 2
st.subheader('Upload your duplicate QC Data (vwDHQCDuplicates) here:')
upload_file_duplicates = st.file_uploader('CSV file format required', key = "duplicates")

# File Previewer 2
with st.expander(":pushpin: File Preview"):
    if upload_file_duplicates is not None:
        # Read the file to a dataframe using pandas
        df_duplicates = pd.read_csv(upload_file_duplicates, encoding='latin1', parse_dates=['Assay_Date'], dayfirst=True)

        st.session_state['df_duplicates']=df_duplicates

        st.dataframe(df_duplicates)
    
# Markdown gap
st.markdown("---") 

# File Uploader 3
st.subheader('Upload your lithogeochem (vwDHLithogeochemStandardsBlanks) here:')
upload_file_lithogeochem = st.file_uploader('CSV file format required', key = "lithogeochem")

# File Previewer 3
with st.expander(":pushpin: File Preview"):
    if upload_file_lithogeochem is not None:
        # Read the file to a dataframe using pandas
        df_lithogeochem = pd.read_csv(upload_file_lithogeochem, encoding='latin1', parse_dates=['Assay_Date'], dayfirst=True)

        st.session_state['df_lithogeochem']=df_lithogeochem

        st.dataframe(df_lithogeochem)
    
# Markdown gap
st.markdown("---") 

# File Uploader 4
st.subheader('Upload your surface sampling (vwSSStandardsBlanks) here:')
upload_file_surface = st.file_uploader('CSV file format required', key = "surface")

# File Previewer 4
with st.expander(":pushpin: File Preview"):
    if upload_file_surface is not None:
        # Read the file to a dataframe using pandas
        df_surface = pd.read_csv(upload_file_surface, encoding='latin1', parse_dates=['Lab_Job_Date'], dayfirst=True)

        st.session_state['df_surface']=df_surface

        st.dataframe(df_surface)
    
# Markdown gap
st.markdown("---") 