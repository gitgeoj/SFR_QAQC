import pandas as pd
import streamlit as st
import plotly_express as px
from streamlit_extras.metric_cards import style_metric_cards


# Page Title and Subtext
st.header('Blank Performance')
st.subheader('Select a blank and analytical element from the dropdown lists below')

# Web app stuff

#Error Message - displays error message if user hasn't loaded in required data for viewing, otherwise it recalls dataframe from Session State
try:
    df =st.session_state['df_standardassay']
except KeyError:
    st.error(":rotating_light: Please load some Standard & Blank data for viewing (vwDHStandardAssays)")

# Create Start and End date variables from user selected date range
start_date= st.session_state['start']
end_date= st.session_state['end']

# Sidebar text displaying selected date range
with st.sidebar:
    st.write("### :calendar: Selected Date Range:")
    st.write(f"{start_date} \u2B0c {end_date}")
    
# Defining the Blank Plot Function
def blank_plot(dataframe):
    x_axis_val = df_selected_blk['SampleID'].sort_values()
    y_axis_val = df_selected_blk['column_name']=element
    
    plot = px.line(dataframe, x= x_axis_val, y = y_axis_val,template="none", markers=True, hover_name=x_axis_val, hover_data=['Batch_No', 'Assay_Date'])
    plot.update_traces(marker=dict(color='black'))
    plot.add_hline(y = 30, line_width=3, line_color='red')
    plot.add_hline(y = 10, line_width=2, line_color='orange')
    st.plotly_chart(plot, use_container_width=True)

    # Markdown gap
    st.markdown("---")
    
    # Creation of the dynamic Summary Stats
    st.header(f"Summary of {blk} Data ({start_date} \u2B0c {end_date})")
    
    total_standards=df_selected_blk["SampleID"].count()
    passed_standards=len(df_selected_blk[df_selected_blk['Cu_ppm']<30])
    failed_standards=len(df_selected_blk[df_selected_blk['Cu_ppm']>30])
    pass_rate = int(((total_standards-failed_standards)/total_standards)*100)

    col1, col2, col3, col4 = st.columns (4)
    col1.metric(label = f'Total No. Used', value = total_standards)
    col2.metric(label = "Total No. Passed", value = passed_standards)
    col3.metric(label = "Total No. Failed", value = failed_standards)
    col4.metric(label = "Pass Rate", value = f'{pass_rate}%')
    style_metric_cards(border_left_color='#DA390D')

#Dataframe filters
blanks = ['AMIS0793','Amis0793','AMIS0681','Amis0681', 'LABBLANK']
blank_df = df[df['StandardID'].isin(blanks)]
blank_list = blank_df['StandardID'].drop_duplicates().sort_values()
elements_list=blank_df.loc[:,['Cu_ppm', 'Ag_ppm', 'Pb_ppm', 'Zn_ppm']]

# Standard and Element Selection
l_col, r_col = st.columns(2)
blk = l_col.selectbox('Select Standard', options=blank_list)
element = r_col.selectbox('Select Element', options=elements_list.columns)
    
#Filter Dataframe by user selected Blank
df_selected_blk = df.loc[df['StandardID']==blk].sort_values(['Assay_Date', 'SampleID'])

# Filter Dataframe by user defined Date Range
df_selected_blk=df_selected_blk.loc[(df_selected_blk['Assay_Date'].dt.date >=start_date)
                                              & (df_selected_blk['Assay_Date'].dt.date <=end_date)]
# Markdown gap
st.markdown("---")

# Plot
blank_plot(df_selected_blk)

