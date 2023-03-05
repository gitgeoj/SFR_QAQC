import pandas as pd
import streamlit as st
import plotly_express as px
import base64
import datetime
from datetime import date
from streamlit_extras.metric_cards import style_metric_cards

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
st.header('Surface Sampling Standards')
st.subheader('Select a Standard and analytical element from the dropdown lists below')

# Web app stuff

# Standard Details & Dataframes
CRM = [
['OREAS 22h', 'Al_pct', 0.101, 0.077, 0.125, 0.008],
['OREAS 22h', 'Ba_ppm', 5.24, 3.17, 7.31, 0.69],
['OREAS 22h', 'Ca_pct', 0.009, 0.006, 0.012, 0.001],
['OREAS 22h', 'Ce_ppm', 2.11, 1.15, 3.07, 0.32],
['OREAS 22h', 'Co_ppm', 0.53, 0.35, 0.71, 0.06],
['OREAS 22h', 'Cs_ppm', 0.09, 0.069, 0.111, 0.007],
['OREAS 22h', 'Cu_ppm', 6.2, 5.108, 7.292, 0.364],
['OREAS 22h', 'Fe_pct', 0.357, 0.267, 0.447, 0.03],
['OREAS 22h', 'Ga_ppm', 0.23, 0.11, 0.35, 0.04],
['OREAS 22h', 'Hf_ppm', 0.21, 0.09, 0.33, 0.04],
['OREAS 22h', 'La_ppm', 1.02, 0.6, 1.44, 0.14],
['OREAS 22h', 'Li_ppm', 14.9, 12.17, 17.63, 0.91],
['OREAS 22h', 'Mn_pct', 0.007, 0.007, 0.007, 0],
['OREAS 22h', 'Mo_ppm', 0.6, 0.3, 0.9, 0.1],
['OREAS 22h', 'Nb_ppm', 0.68, 0.41, 0.95, 0.09],
['OREAS 22h', 'Ni_ppm', 4.66, 2.62, 6.7, 0.68],
['OREAS 22h', 'Pb_ppm', 0.83, 0.32, 1.34, 0.17],
['OREAS 22h', 'Rb_ppm', 0.37, 0.22, 0.52, 0.05],
['OREAS 22h', 'Sb_ppm', 0.16, 0.1, 0.22, 0.02],
['OREAS 22h', 'Sc_ppm', 0.1, 0.01, 0.19, 0.03],
['OREAS 22h', 'Sn_ppm', 0.41, 0.17, 0.65, 0.08],
['OREAS 22h', 'Sr_ppm', 0.75, 0.39, 1.11, 0.12],
['OREAS 22h', 'Th_ppm', 0.62, 0.458, 0.782, 0.054],
['OREAS 22h', 'Ti_pct', 0.024, 0.012, 0.036, 0.004],
['OREAS 22h', 'U_ppm', 0.12, 0.03, 0.21, 0.03],
['OREAS 22h', 'W_ppm', 0.17, 0.05, 0.29, 0.04],
['OREAS 22h', 'Y_ppm', 0.61, 0.457, 0.763, 0.051],
['OREAS 22h', 'Zn_ppm', 2.69, 0.65, 4.73, 0.68],
['OREAS 22h', 'Zr_ppm', 7.07, 3.02, 11.12, 1.35],

['OREAS 25a', 'Al_pct', 8.87, 7.595, 10.145, 0.425],
['OREAS 25a', 'Ba_ppm', 147, 132, 162, 5],
['OREAS 25a', 'Bi_ppm', 0.35, 0.248, 0.452, 0.034],
['OREAS 25a', 'Ca_pct', 0.309, 0.285, 0.333, 0.008],
['OREAS 25a', 'Ce_ppm', 48.9, 40.77, 57.03, 2.71],
['OREAS 25a', 'Co_ppm', 8.2, 6.211, 10.189, 0.663],
['OREAS 25a', 'Cr_ppm', 115, 91, 139, 8],
['OREAS 25a', 'Cs_ppm', 6.46, 5.458, 7.462, 0.334],
['OREAS 25a', 'Cu_ppm', 33.9, 27.03, 40.77, 2.29],
['OREAS 25a', 'Fe_pct', 6.6, 6.129, 7.071, 0.157],
['OREAS 25a', 'Ga_ppm', 25.9, 20.59, 31.21, 1.77],
['OREAS 25a', 'Hf_ppm', 4.53, 2.94, 6.12, 0.53],
['OREAS 25a', 'K_pct', 0.482, 0.44, 0.524, 0.014],
['OREAS 25a', 'La_ppm', 21.8, 15.74, 27.86, 2.02],
['OREAS 25a', 'Li_ppm', 36.7, 32.68, 40.72, 1.34],
['OREAS 25a', 'Mg_pct', 0.327, 0.276, 0.378, 0.017],
['OREAS 25a', 'Mn_pct', 0.047, 0.041, 0.053, 0.002],
['OREAS 25a', 'Mo_ppm', 2.55, 2.076, 3.024, 0.158],
['OREAS 25a', 'Na_pct', 0.134, 0.122, 0.146, 0.004],
['OREAS 25a', 'Nb_ppm', 22.4, 17.27, 27.53, 1.71],
['OREAS 25a', 'Ni_ppm', 45.8, 33.65, 57.95, 4.05],
['OREAS 25a', 'P_pct', 0.048, 0.042, 0.054, 0.002],
['OREAS 25a', 'Pb_ppm', 25.2, 19.59, 30.81, 1.87],
['OREAS 25a', 'Rb_ppm', 61, 49.3, 72.7, 3.9],
['OREAS 25a', 'Sn_ppm', 4.06, 3.472, 4.648, 0.196],
['OREAS 25a', 'Sr_ppm', 48.5, 42.53, 54.47, 1.99],
['OREAS 25a', 'Ta_ppm', 1.6, 1.198, 2.002, 0.134],
['OREAS 25a', 'Th_ppm', 15.8, 12.89, 18.71, 0.97],
['OREAS 25a', 'Ti_pct', 0.977, 0.8, 1.154, 0.059],
['OREAS 25a', 'Tl_ppm', 0.35, 0.26, 0.44, 0.03],
['OREAS 25a', 'U_ppm', 2.94, 2.676, 3.204, 0.088],
['OREAS 25a', 'V_ppm', 157, 133, 181, 8],
['OREAS 25a', 'W_ppm', 2.1, 1.497, 2.703, 0.201],
['OREAS 25a', 'Y_ppm', 12.3, 6, 18.6, 2.1],
['OREAS 25a', 'Zn_ppm', 44.4, 36.6, 52.2, 2.6],

['OREAS 45h', 'Ag_ppm', 0.147, 0.063, 0.231, 0.028],
['OREAS 45h', 'Al_pct', 7.99, 7.207, 8.773, 0.261],
['OREAS 45h', 'As_ppm', 16.9, 13.15, 20.65, 1.25],
['OREAS 45h', 'Ba_ppm', 332, 293, 371, 13],
['OREAS 45h', 'Be_ppm', 1.09, 0.64, 1.54, 0.15],
['OREAS 45h', 'Bi_ppm', 0.17, 0.125, 0.215, 0.015],
['OREAS 45h', 'Ca_pct', 0.135, 0.105, 0.165, 0.01],
['OREAS 45h', 'Ce_ppm', 23.6, 18.71, 28.49, 1.63],
['OREAS 45h', 'Co_ppm', 88, 76.6, 99.4, 3.8],
['OREAS 45h', 'Cr_ppm', 602, 452, 752, 50],
['OREAS 45h', 'Cs_ppm', 2.29, 1.918, 2.662, 0.124],
['OREAS 45h', 'Cu_ppm', 767, 713, 821, 18],
['OREAS 45h', 'Dy_ppm', 2.42, 1.859, 2.981, 0.187],
['OREAS 45h', 'Er_ppm', 1.44, 1.134, 1.746, 0.102],
['OREAS 45h', 'Eu_ppm', 0.65, 0.41, 0.89, 0.08],
['OREAS 45h', 'Fe_pct', 19.52, 17.546, 21.494, 0.658],
['OREAS 45h', 'Ga_ppm', 21.3, 16.59, 26.01, 1.57],
['OREAS 45h', 'Gd_ppm', 2.34, 1.911, 2.769, 0.143],
['OREAS 45h', 'Hf_ppm', 3.6, 2.748, 4.452, 0.284],
['OREAS 45h', 'Ho_ppm', 0.48, 0.387, 0.573, 0.031],
['OREAS 45h', 'K_pct', 0.205, 0.187, 0.223, 0.006],
['OREAS 45h', 'La_ppm', 12.4, 9.73, 15.07, 0.89],
['OREAS 45h', 'Li_ppm', 13.1, 10.25, 15.95, 0.95],
['OREAS 45h', 'Lu_ppm', 0.21, 0.153, 0.267, 0.019],
['OREAS 45h', 'Mg_pct', 0.238, 0.202, 0.274, 0.012],
['OREAS 45h', 'Mn_pct', 0.038, 0.035, 0.041, 0.001],
['OREAS 45h', 'Mo_ppm', 1.55, 0.86, 2.24, 0.23],
['OREAS 45h', 'Na_pct', 0.09, 0.075, 0.105, 0.005],
['OREAS 45h', 'Nb_ppm', 14.8, 12.22, 17.38, 0.86],
['OREAS 45h', 'Nd_ppm', 11.2, 8.02, 14.38, 1.06],
['OREAS 45h', 'Ni_ppm', 423, 363, 483, 20],
['OREAS 45h', 'P_pct', 0.023, 0.017, 0.029, 0.002],
['OREAS 45h', 'Pb_ppm', 11.9, 9.38, 14.42, 0.84],
['OREAS 45h', 'Pr_ppm', 2.91, 2.466, 3.354, 0.148],
['OREAS 45h', 'Rb_ppm', 22.5, 19.11, 25.89, 1.13],
['OREAS 45h', 'S_pct', 0.035, 0.023, 0.047, 0.004],
['OREAS 45h', 'Sb_ppm', 0.63, 0.42, 0.84, 0.07],
['OREAS 45h', 'Sc_ppm', 57, 46.2, 67.8, 3.6],
['OREAS 45h', 'Se_ppm', 2.02, 0.85, 3.19, 0.39],
['OREAS 45h', 'Sm_ppm', 2.5, 2.035, 2.965, 0.155],
['OREAS 45h', 'Sn_ppm', 1.93, 1.45, 2.41, 0.16],
['OREAS 45h', 'Sr_ppm', 27.1, 22.66, 31.54, 1.48],
['OREAS 45h', 'Ta_ppm', 1.08, 0.72, 1.44, 0.12],
['OREAS 45h', 'Tb_ppm', 0.39, 0.288, 0.492, 0.034],
['OREAS 45h', 'Th_ppm', 7.26, 4.92, 9.6, 0.78],
['OREAS 45h', 'Ti_pct', 0.878, 0.797, 0.959, 0.027],
['OREAS 45h', 'Tl_ppm', 0.15, 0.111, 0.189, 0.013],
['OREAS 45h', 'Tm_ppm', 0.23, 0.17, 0.29, 0.02],
['OREAS 45h', 'U_ppm', 1.68, 1.248, 2.112, 0.144],
['OREAS 45h', 'V_ppm', 263, 236, 290, 9],
['OREAS 45h', 'W_ppm', 0.99, 0.726, 1.254, 0.088],
['OREAS 45h', 'Y_ppm', 10.4, 8.27, 12.53, 0.71],
['OREAS 45h', 'Yb_ppm', 1.44, 1.092, 1.788, 0.116],
['OREAS 45h', 'Zn_ppm', 39.7, 34.27, 45.13, 1.81],
['OREAS 45h', 'Zr_ppm', 131, 113, 149, 6],

['OREAS 46', 'Ag_ppm', 0.038, 0.017, 0.059, 0.007],
['OREAS 46', 'Al_pct', 6.26, 5.78, 6.74, 0.16],
['OREAS 46', 'As_ppm', 1.01, 0.29, 1.73, 0.24],
['OREAS 46', 'Ba_ppm', 473, 437, 509, 12],
['OREAS 46', 'Be_ppm', 0.91, 0.679, 1.141, 0.077],
['OREAS 46', 'Bi_ppm', 0.054, 0.036, 0.072, 0.006],
['OREAS 46', 'Ca_pct', 2.4, 2.274, 2.526, 0.042],
['OREAS 46', 'Cd_ppm', 0.059, 0.017, 0.101, 0.014],
['OREAS 46', 'Ce_ppm', 36.4, 31.36, 41.44, 1.68],
['OREAS 46', 'Co_ppm', 9.83, 8.639, 11.021, 0.397],
['OREAS 46', 'Cr_ppm', 45.7, 20.2, 71.2, 8.5],
['OREAS 46', 'Cs_ppm', 0.64, 0.535, 0.745, 0.035],
['OREAS 46', 'Cu_ppm', 23.1, 21.3, 24.9, 0.6],
['OREAS 46', 'Dy_ppm', 2.03, 1.694, 2.366, 0.112],
['OREAS 46', 'Er_ppm', 1.13, 0.917, 1.343, 0.071],
['OREAS 46', 'Eu_ppm', 0.89, 0.734, 1.046, 0.052],
['OREAS 46', 'Fe_pct', 2.61, 2.409, 2.811, 0.067],
['OREAS 46', 'Ga_ppm', 14, 12.47, 15.53, 0.51],
['OREAS 46', 'Gd_ppm', 2.66, 2, 3.32, 0.22],
['OREAS 46', 'Hf_ppm', 1.82, 1.358, 2.282, 0.154],
['OREAS 46', 'Ho_ppm', 0.39, 0.327, 0.453, 0.021],
['OREAS 46', 'K_pct', 1.19, 1.1, 1.28, 0.03],
['OREAS 46', 'La_ppm', 18.9, 15.51, 22.29, 1.13],
['OREAS 46', 'Li_ppm', 10.4, 9.02, 11.78, 0.46],
['OREAS 46', 'Lu_ppm', 0.15, 0.117, 0.183, 0.011],
['OREAS 46', 'Mg_pct', 0.943, 0.865, 1.021, 0.026],
['OREAS 46', 'Mn_pct', 0.049, 0.043, 0.055, 0.002],
['OREAS 46', 'Mo_ppm', 0.77, 0.575, 0.965, 0.065],
['OREAS 46', 'Na_pct', 2.61, 2.358, 2.862, 0.084],
['OREAS 46', 'Nb_ppm', 4.56, 3.327, 5.793, 0.411],
['OREAS 46', 'Nd_ppm', 18.5, 16.82, 20.18, 0.56],
['OREAS 46', 'Ni_ppm', 26.8, 23.68, 29.92, 1.04],
['OREAS 46', 'P_pct', 0.054, 0.048, 0.06, 0.002],
['OREAS 46', 'Pb_ppm', 7.02, 6.447, 7.593, 0.191],
['OREAS 46', 'Pr_ppm', 4.84, 4.174, 5.506, 0.222],
['OREAS 46', 'Rb_ppm', 33.5, 28.73, 38.27, 1.59],
['OREAS 46', 'Sb_ppm', 0.1, 0.04, 0.16, 0.02],
['OREAS 46', 'Sc_ppm', 8.75, 7.676, 9.824, 0.358],
['OREAS 46', 'Sm_ppm', 3.32, 2.78, 3.86, 0.18],
['OREAS 46', 'Sn_ppm', 0.78, 0.582, 0.978, 0.066],
['OREAS 46', 'Sr_ppm', 408, 369, 447, 13],
['OREAS 46', 'Ta_ppm', 0.27, 0.15, 0.39, 0.04],
['OREAS 46', 'Tb_ppm', 0.36, 0.285, 0.435, 0.025],
['OREAS 46', 'Th_ppm', 3.26, 2.6, 3.92, 0.22],
['OREAS 46', 'Ti_pct', 0.207, 0.177, 0.237, 0.01],
['OREAS 46', 'Tl_ppm', 0.21, 0.162, 0.258, 0.016],
['OREAS 46', 'Tm_ppm', 0.15, 0.117, 0.183, 0.011],
['OREAS 46', 'U_ppm', 0.7, 0.574, 0.826, 0.042],
['OREAS 46', 'V_ppm', 57, 50.7, 63.3, 2.1],
['OREAS 46', 'W_ppm', 0.21, 0.09, 0.33, 0.04],
['OREAS 46', 'Y_ppm', 10.5, 9.42, 11.58, 0.36],
['OREAS 46', 'Yb_ppm', 1.01, 0.83, 1.19, 0.06],
['OREAS 46', 'Zn_ppm', 35.5, 31.42, 39.58, 1.36],
['OREAS 46', 'Zr_ppm', 61, 46.9, 75.1, 4.7]
]

crm_df = pd.DataFrame(CRM, columns=['Standard','Element','Expected Value', 'Min 3sd', 'Max 3sd', 'Standard Deviation'])

#Error Message - displays error message if user hasn't loaded in required data for viewing
try:
    df_surface_assay =st.session_state['df_surface']
except KeyError:
    st.error("Please load Surface Sampling data for viewing (vwSSStandardsBlanks)")

start_date= st.session_state['start']
end_date= st.session_state['end']

# Sidebar text displaying selected date range
with st.sidebar:
    st.write("### :calendar: Selected Date Range:")
    st.write(f"{start_date} \u2B0c {end_date}")

#Dataframe filters
standards = ['OREAS 22h','OREAS 25a','OREAS 45h','OREAS 46']
surface_standard_df = df_surface_assay[df_surface_assay['StandardID'].isin(standards)]
standard_list = surface_standard_df['StandardID'].drop_duplicates().sort_values()
elements_list=surface_standard_df.loc[:,['Ag_ppm', 'Al_pct', 'As_ppm', 'Ba_ppm', 'Be_ppm', 'Bi_ppm', 'Ca_pct', 'Ce_ppm', 'Co_ppm', 'Cr_ppm','Cs_ppm', 'Cu_ppm', 'Fe_pct', 'Ga_ppm', 'Hf_ppm', 
                                         'K_pct', 'La_ppm', 'Li_ppm', 'Mg_pct', 'Mo_ppm', 'Na_pct', 'Nb_ppm', 'Ni_ppm', 'Rb_ppm', 'S_pct', 'Sb_ppm', 'Sc_ppm', 'Se_ppm', 'Sn_ppm', 'Sr_ppm', 
                                         'Ta_ppm', 'Th_ppm', 'Ti_pct', 'Tl_ppm', 'U_ppm', 'V_ppm', 'W_ppm', 'Y_ppm', 'Zn_ppm', 'Zr_ppm']]

# Standard and Element Selection
l_col, r_col = st.columns(2)
selected_std = l_col.selectbox('Select Standard', options=standard_list)
selected_element = r_col.selectbox('Select Element', options=elements_list.columns)
    
#Filtered Dataframe
df_selected_standard = df_surface_assay.loc[df_surface_assay['StandardID']==selected_std].sort_values(['Lab_Job_Date', 'SampleID'])

df_selected_standard=df_selected_standard.loc[(df_selected_standard['Lab_Job_Date'].dt.date >=start_date)
                                              & (df_selected_standard['Lab_Job_Date'].dt.date <=end_date)]
# Markdown gap
st.markdown("---")

#Defining the Standard Plot Function
def surface_standard_plot(dataframe, standard, element):
    x_axis_val = df_selected_standard['SampleID']
    y_axis_val = df_selected_standard['column_name']=element
    
    filt_df= crm_df.loc[crm_df['Standard']==standard]
    expected_val = filt_df.loc[filt_df['Element'] == element, 'Expected Value'].item()
    plus_3sd = filt_df.loc[filt_df['Element']== element, 'Max 3sd'].item()
    minus_3sd = filt_df.loc[filt_df['Element']== element, 'Min 3sd'].item()
    sd = filt_df.loc[filt_df['Element']== element, 'Standard Deviation'].item()
    plus_2sd = expected_val + (2*sd)
    minus_2sd = expected_val - (2*sd)
  
    plot = px.line(dataframe, x= x_axis_val, y = y_axis_val, markers=True, title=f"<b>{standard}</b> - {element}(expected value = {expected_val})", template="none", hover_name=x_axis_val, hover_data=['Batch_No'])
    plot.update_traces(marker=dict(color='black'))
    plot.update_layout(
    title={
        'y':0.85,
        'x':0.4,
        'xanchor': 'left',
        'yanchor': 'top'})
    
    plot.add_hline(y = expected_val, line_width=0.5, line_color='black', line_dash="dot")
    plot.add_hline(y = plus_3sd, line_width=3, line_color='red', line_dash="dash", annotation_text="+3SD")
    plot.add_hline(y = minus_3sd, line_width=3, line_color='red', line_dash="dash", annotation_text="-3SD")
    plot.add_hline(y = plus_2sd, line_width=2, line_color='green')
    plot.add_hline(y = minus_2sd, line_width=2, line_color='green') 

    st.plotly_chart(plot, use_container_width=True)
    
    # Markdown gap
    st.markdown("---")
    
    # Summary Stats
    st.subheader(f"Summary of {selected_std} Data ({start_date} \u2B0c {end_date})")
    
    total_standards=df_selected_standard["SampleID"].count()
    assay_result = dataframe[element] # not sure what this gets me but doesn't seem right
    passed_2sd = ((minus_2sd < assay_result) & (assay_result < plus_2sd))
    passed_2sd_pct = ((passed_2sd.sum()/total_standards)*100).round()
    passed_3sd = ((minus_3sd < assay_result) & (assay_result < plus_3sd))
    passed_3sd_pct = ((passed_3sd.sum()/total_standards)*100).round()
    failed_3sd = ((minus_3sd > assay_result) | (assay_result > plus_3sd))
    failed_3sd_pct = -((failed_3sd.sum()/total_standards)*100).round()

    col1, col2, col3, col4 = st.columns (4)
    col1.metric(label = 'Total No. Used', value = total_standards)
    col2.metric(label = "Passed (<2 Std. Dev.)", value = passed_2sd.sum(), delta = f'{passed_2sd_pct}%')
    col3.metric(label = "Passed (<3 Std. Dev.)", value = passed_3sd.sum(), delta = f'{passed_3sd_pct}%')
    col4.metric(label = "Failed (+/- 3 Std. Dev.)", value = failed_3sd.sum(), delta = f'{failed_3sd_pct}%')
    style_metric_cards(border_left_color='#DA390D')


    # Markdown gap
    st.markdown("---")
    # Create a section for the dataframe statistics
    st.subheader('Certified Reference Values')
    if st.checkbox("Check box to view certified referrence values"):
        st.dataframe(filt_df)


# Plot
#Error Message - displays error message if user has selected an element without certified reference values or std. dev.
try:
    surface_standard_plot(df_selected_standard,selected_std,selected_element)
except ValueError:
    st.error(":rotating_light: The selected Element has no certified value or standard deviation for this Standard. Please select another Element or Standard.")
