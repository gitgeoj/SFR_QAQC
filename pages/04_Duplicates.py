import pandas as pd
import streamlit as st
import plotly_express as px
import base64

#Logo 
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


# Subheading
st.header('Duplicate Perforomance')
st.subheader('Select a duplicate dataset from the dropdown lists below')

## Web app stuff



#Duplicate Data
#Error Message - displays error message if user hasn't loaded in required data for viewing
try:
    df =df_duplicates =st.session_state['df_duplicates']
except KeyError:
    st.error("Please load some Duplicate data for viewing (vwQCDuplicates)")

start_date= st.session_state['start']
end_date= st.session_state['end']

# Sidebar text displaying selected date range
with st.sidebar:
    st.write("### :calendar: Selected Date Range:")
    st.write(f"{start_date} \u2B0c {end_date}")
    
#Dataframe filters
duplicate_list = df_duplicates['QC_Category'].drop_duplicates().sort_values()
elements_list=df_duplicates.loc[:,['Cu_ppm', 'Ag_ppm', 'Pb_ppm', 'Zn_ppm', 'S_pct', 'Bi_ppm', 'Co_ppm', 'Fe_pct', 'Sb_ppm']]


# QC Pairs and Duplicate DF_Pairs
pairs =[
    ['Ag_ppm','Ag_ppm_QC'],
    ['Al_pct','Al_pct_QC'],
    ['As_ppm','As_ppm_QC'],
    ['Ba_ppm','Ba_ppm_QC'],
    ['Be_ppm','Be_ppm_QC'],
    ['Bi_ppm','Bi_ppm_QC'],
    ['Ca_pct','Ca_pct_QC'],
    ['Cd_ppm','Cd_ppm_QC'],
    ['Co_ppm','Co_ppm_QC'],
    ['Cr_ppm','Cr_ppm_QC'],
    ['Cu_ppm','Cu_ppm_QC'],
    ['Fe_pct','Fe_pct_QC'],
    ['Ga_ppm','Ga_ppm_QC'],
    ['K_pct','K_pct_QC'],
    ['La_ppm','La_ppb_QC'],
    ['Mg_pct','Mg_pct_QC'],
    ['Mn_ppm','Mn_ppm_QC'],
    ['Mo_ppm','Mo_ppm_QC'],
    ['Na_pct','Na_pct_QC'],
    ['Ni_ppm','Ni_ppm_QC'],
    ['P_ppm','P_ppm_QC'],
    ['Pb_ppm','Pb_ppm_QC'],
    ['S_pct','S_pct_QC'],
    ['Sb_ppm','Sb_ppm_QC'],
    ['Sc_ppm','Sc_ppm_QC'],
    ['Sr_ppm','Sr_ppm_QC'],
    ['Th_ppm','Th_ppm_QC'],
    ['Ti_pct','Ti_pct_QC'],
    ['Tl_ppm','Tl_ppm_QC'],
    ['U_ppm','U_ppm_QC'],
    ['V_ppm','V_ppm_QC'],
    ['W_ppm','W_ppm_QC'],
    ['Zn_ppm','Zn_ppm_QC']
]
df_pairs = pd.DataFrame(pairs, columns=['Orig','QC'])

# Standard and Element Selection
l_col, r_col = st.columns(2)
selected_duplicate = l_col.selectbox('Select Duplicate Data', options=duplicate_list)
selected_element = r_col.selectbox('Select Element', options=df_pairs["Orig"])
#Filtered Dataframe
df_qc_duplicate = df_duplicates.loc[df_duplicates['QC_Category']==selected_duplicate]
df_qc_duplicate=df_qc_duplicate.loc[(df_qc_duplicate['Assay_Date'].dt.date >=start_date)
                                              & (df_qc_duplicate['Assay_Date'].dt.date <=end_date)]

qc_element = df_pairs.loc[df_pairs['Orig']==selected_element, 'QC']

#Defining Duplicate Plot Function
def duplicate_plot(dataframe, duplicate, element, qc_element):
    x_axis_values = df_qc_duplicate['column_name']=element
    y_axis_values = df_qc_duplicate['column_name']=qc_element

    plot = px.scatter(dataframe, x_axis_values, y_axis_values, title =f"<b>{selected_element} {selected_duplicate} Pairs", hover_name='SampleID',
    hover_data={'variable':False, 'Batch_no':True,'Orig_SampleID':True, 'SampleID':True})
    
    
    plot.update_layout(
        xaxis_title=f"<b>{element} (Original)", yaxis_title=f"<b>{element}_QC (Duplicate)",
        title={'y':0.95,
            'x':0.35,
            'xanchor': 'left',
            'yanchor': 'top'},
        autosize=False,
        width=900,
        height=900,
        showlegend=False
        )
    plot.update_xaxes(rangemode="tozero",scaleanchor = "x", scaleratio = 1, ticksuffix="ppm")
    plot.update_yaxes(rangemode="tozero", ticksuffix="ppm")
    st.plotly_chart(plot)


# Plot
duplicate_plot(df_qc_duplicate,selected_duplicate, selected_element, qc_element)


