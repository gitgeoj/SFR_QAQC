import pandas as pd
import streamlit as st
import plotly_express as px

# Subheading
st.header('Lithogeochem Standards')
st.subheader('Select a standard and analytical element from the dropdown lists below')

st.error(":rotating_light::rotating_light: THIS PAGE IS STILL UNDER DEVELOPMENT :rotating_light::rotating_light:")
# Web app stuff

# Standard Details & Dataframes
CRM = [['OREAS 920', 'Cu_ppm', 265, 226, 304, 13],
['OREAS 920', 'Pb_ppm', 5.16, 2.61, 7.71, 0.85],
['OREAS 920', 'Zn_ppm', 66.4, 48.4, 84.4, 6],
['OREAS 920', 'S_pct', 0.0841, 0.0607, 0.1075, 0.0078],
['OREAS 920', 'Bi_ppm', 1.01, 0.62, 1.4, 0.13],
['OREAS 920', 'Co_ppm', 14.2, 11.8, 16.6, 0.18],
['OREAS 920', 'Sb_ppm', 0.85, 0.55, 1.15, 0.1],
['OREAS 920', 'Se_ppm', 1.28, 0, 2.99, 0.57],
['OREAS 920', 'Sn_ppm', 7.47, 5.49, 9.45, 0.66],

['OREAS 921', 'Ag_ppm', 1.1, 0.77, 1.43, 0.11],
['OREAS 921', 'Cu_ppm', 4090, 3730, 4450, 120],
['OREAS 921', 'Pb_ppm', 135, 105, 165, 10],
['OREAS 921', 'Zn_ppm', 22, 4, 40, 6],
['OREAS 921', 'S_pct', 3.06, 2.55, 3.57, 0.17],
['OREAS 921', 'Co_ppm', 119, 110, 128, 3],
['OREAS 921', 'Fe_pct', 4.26, 3.9, 4.62, 0.12],
]

crm_df = pd.DataFrame(CRM, columns=['Standard','Element','Expected Value', 'Min 3sd', 'Max 3sd', 'Standard Deviation'])


# Web app stuff


#Error Message - displays error message if user hasn't loaded in required data for viewing
try:
    df =df_lithogeochem =st.session_state['df_lithogeochem']
except KeyError:
    st.error("Please load some Lithogeochem Standard data for viewing (vwDHLithogeochemStandards)")

# Sidebar text displaying selected date range
# with st.sidebar:
#     st.write("### :calendar: Selected Date Range:")
#     st.write(f"{start_date} \u2B0c {end_date}")

def standard_plot(dataframe, standard, element):
    x_axis_val = df_std['SampleID']
    y_axis_val = df_std['column_name']=element
    
    filt_df= crm_df.loc[crm_df['Standard']==standard]
    expected_val = filt_df.loc[filt_df['Element'] == element, 'Expected Value'].item()
    plus_3sd = filt_df.loc[filt_df['Element']== element, 'Max 3sd'].item()
    minus_3sd = filt_df.loc[filt_df['Element']== element, 'Min 3sd'].item()
    sd = filt_df.loc[filt_df['Element']== element, 'Standard Deviation'].item()
    plus_2sd = expected_val + (2*sd)
    minus_2sd = expected_val - (2*sd)
  
    plot = px.line(dataframe, x= x_axis_val, y = y_axis_val, markers=True, title=f"<b>{standard}</b> - {element}(expected value = {expected_val})", template="simple_white", hover_name=x_axis_val, hover_data=['Batch_No'])
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
    
    # Create a section for the dataframe statistics
    st.subheader('Summary of Blank Data')
    if st.checkbox("Check box to view certified referrence values"):
        st.dataframe(filt_df)



#Dataframe filters
standards = ['OREAS 920','OREAS 921']
standard_df = df_lithogeochem[df_lithogeochem['StandardID'].isin(standards)]
standard_list = standard_df['StandardID'].drop_duplicates().sort_values()
elements_list=standard_df.loc[:,['Cu_ppm', 'Ag_ppm', 'Zn_ppm', 'S_pct', 'Bi_ppm', 'Co_ppm', 'Fe_pct', 'Sb_ppm']]

##, 'Pb_ppm' remove. need to reinclude

# Standard and Element Selection
l_col, r_col = st.columns(2)
selected_std = l_col.selectbox('Select Standard', options=standard_list)
selected_element = r_col.selectbox('Select Element', options=elements_list.columns)
    
#Filtered Dataframe
df_std = df_lithogeochem.loc[df_lithogeochem['StandardID']==selected_std]

# Markdown gap
st.markdown("---")



# Plot
standard_plot(df_std,selected_std,selected_element)
