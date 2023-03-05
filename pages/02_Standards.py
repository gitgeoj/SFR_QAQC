import pandas as pd
import streamlit as st
import plotly_express as px
import datetime
from datetime import date
from streamlit_extras.metric_cards import style_metric_cards


# Page Title and Subtext
st.header('Standard Performance')
st.subheader('Select a Standard and analytical element from the dropdown lists below')

# Standard Details (CRM, Element, Expected Value, -3SD, +3SD, Std. Dev)
CRM = [['OREAS 91', 'Cu_ppm', 265, 226, 304, 13],
['OREAS 91', 'Pb_ppm', 5.16, 2.61, 7.71, 0.85],
['OREAS 91', 'Zn_ppm', 66.4, 48.4, 84.4, 6],
['OREAS 91', 'S_pct', 0.0841, 0.0607, 0.1075, 0.0078],
['OREAS 91', 'Bi_ppm', 1.01, 0.62, 1.4, 0.13],
['OREAS 91', 'Co_ppm', 14.2, 11.8, 16.6, 0.18],
['OREAS 91', 'Sb_ppm', 0.85, 0.55, 1.15, 0.1],
['OREAS 91', 'Se_ppm', 1.28, 0, 2.99, 0.57],
['OREAS 91', 'Sn_ppm', 7.47, 5.49, 9.45, 0.66],

['OREAS 161', 'Ag_ppm', 1.1, 0.77, 1.43, 0.11],
['OREAS 161', 'Cu_ppm', 4090, 3730, 4450, 120],
['OREAS 161', 'Pb_ppm', 135, 105, 165, 10],
['OREAS 161', 'Zn_ppm', 22, 4, 40, 6],
['OREAS 161', 'S_pct', 3.06, 2.55, 3.57, 0.17],
['OREAS 161', 'Co_ppm', 119, 110, 128, 3],
['OREAS 161', 'Fe_pct', 4.26, 3.9, 4.62, 0.12],

['OREAS 163', 'Ag_ppm', 4.3, 2.5, 6.1, 0.6],
['OREAS 163', 'Cu_ppm', 17600, 15500, 19700, 700],
['OREAS 163', 'Pb_ppm', 492, 450, 534, 14],
['OREAS 163', 'Zn_ppm', 108, 81, 135, 9],
['OREAS 163', 'S_pct', 10.4, 8.9, 11.4, 0.5],

['OREAS 164', 'Ag_ppm', 2.94, 2.46, 3.42, 0.16],
['OREAS 164', 'Cu_ppm', 22500, 20100, 24900, 800],
['OREAS 164', 'Pb_ppm', 214, 172, 256, 14],
['OREAS 164', 'Zn_ppm', 45, 24, 66, 7],
['OREAS 164', 'S_pct', 6.2, 5, 7.4, 0.4]
]

# Creating Dataframe from CRM Dictionary
crm_df = pd.DataFrame(CRM, columns=['Standard','Element','Expected Value', 'Min 3sd', 'Max 3sd', 'Standard Deviation'])


### Web app stuff###

#Error Message - displays error message if user hasn't loaded in required data for viewing, otherwise it recalls dataframe from Session State
try:
    df_standardassay =st.session_state['df_standardassay']
except KeyError:
    st.error(":rotating_light: Please load some Standard & Blank data for viewing (vwDHStandardAssays)")

# Create Start and End date variables from user selected date range
start_date= st.session_state['start']
end_date= st.session_state['end']

# Sidebar text displaying selected date range
with st.sidebar:
    st.write("### :calendar: Selected Date Range:")
    st.write(f"{start_date} \u2B0c {end_date}")
    
# Dataframe filters
standards = ['OREAS 91','OREAS 161','OREAS 163','OREAS 164']
standard_df = df_standardassay[df_standardassay['StandardID'].isin(standards)]
standard_list = standard_df['StandardID'].drop_duplicates().sort_values()
elements_list=standard_df.loc[:,['Ag_ppm', 'Bi_ppm', 'Co_ppm', 'Cu_ppm', 'Fe_pct', 'S_pct',  'Sb_ppm', 'Pb_ppm', 'Zn_ppm']]

# Standard and Element Selection
l_col, r_col = st.columns(2)
selected_std = l_col.selectbox('Select Standard', options=standard_list)
selected_element = r_col.selectbox('Select Element', options=elements_list.columns)
    
# Filter dataframe by selected standard
df_selected_standard = df_standardassay.loc[df_standardassay['StandardID']==selected_std].sort_values(['Assay_Date', 'SampleID'])

# Filter dataframe by Date Range
df_selected_standard=df_selected_standard.loc[(df_selected_standard['Assay_Date'].dt.date >=start_date)
                                              & (df_selected_standard['Assay_Date'].dt.date <=end_date)]
# Markdown gap
st.markdown("---")


# Defining the Standard Plot Function
def standard_plot(dataframe, standard, element):
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
    
    # Adding Expected Value and control lines
    plot.add_hline(y = expected_val, line_width=0.5, line_color='black', line_dash="dot")
    plot.add_hline(y = plus_3sd, line_width=3, line_color='red', line_dash="dash", annotation_text="+3SD")
    plot.add_hline(y = minus_3sd, line_width=3, line_color='red', line_dash="dash", annotation_text="-3SD")
    plot.add_hline(y = plus_2sd, line_width=2, line_color='green')
    plot.add_hline(y = minus_2sd, line_width=2, line_color='green') 

    st.plotly_chart(plot, use_container_width=True)
    
    # Markdown gap
    st.markdown("---")
    
    # Creation of dynamic Summary Stats
    st.subheader(f"Summary of {selected_std} Data [{start_date} \u2B0c {end_date}]")
    
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

# # Plot
# standard_plot(df_selected_standard,selected_std,selected_element)

# Plot
#Error Message - displays error message if user has selected an element without certified reference values or std. dev.
try:
    standard_plot(df_selected_standard,selected_std,selected_element)
except ValueError:
    st.error(":rotating_light: The selected Element has no certified value or standard deviation for this Standard. Please select another Element or Standard.")

