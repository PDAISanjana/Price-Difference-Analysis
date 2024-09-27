import streamlit as st  # type: ignore
import plotly.graph_objects as go  # type: ignore
import pandas as pd  # type: ignore
import numpy as np # type: ignore
from plotly.subplots import make_subplots # type: ignore
import os
from fun_price_diff_reco_ibb import price_diff
from fun_price_diff_reco_other import price_diff_other
from fun_percent_diff_reco_ibb import percent_diff
from fun_percent_diff_reco_other import percent_diff_other
# Load Datasets
script_dir = os.path.dirname(__file__)

file_path1 = os.path.join(script_dir, "Dataset", "Dataset for Price Difference analysis.xlsx")
df = pd.read_excel(file_path1)


st.set_page_config(
    layout='wide'
)

st.sidebar.header('Price Difference Analysis')
type = st.sidebar.radio("Type",('TradeIn','Retail'))
diff = st.sidebar.radio("Difference",('Price','%'))

col1, col2 = st.columns(2)

# Store the default state for reco_price_diff_options
disable_reco = False

# Logic to disable reco_price_diff_options when CTDMS or PO Selected is selected
with col2:
    other_price_diff_options = st.radio("Others", ('IBB', 'CTDMS', 'PO Selected'), horizontal=True)

# Disable reco_price_diff_options if CTDMS or PO Selected is selected
if other_price_diff_options in ['CTDMS', 'PO Selected']:
    disable_reco = True

with col1:
    reco_price_diff_options = st.radio("PDAI Reco", ('Q1', 'Q2', 'Q3'), horizontal=True, disabled=disable_reco)


df_ti = df.loc[df['newCarTradeIn'] == 'Yes']                                                                             
df_re = df.loc[df['newCarTradeIn'] == 'No'] 

if type == 'TradeIn':

    if diff == 'Price':
        
        if reco_price_diff_options == 'Q1' and other_price_diff_options == 'IBB':
            st.plotly_chart(price_diff(df_ti,reco = 'PDAI Price MIN',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q1',other_option='IBB'))
        elif reco_price_diff_options == 'Q2' and other_price_diff_options == 'IBB':
            st.plotly_chart(price_diff(df_ti,reco = 'PDAI Price AVG',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q2',other_option='IBB'))
        elif reco_price_diff_options == 'Q3' and other_price_diff_options == 'IBB':
            st.plotly_chart(price_diff(df_ti,reco = 'PDAI Price Max',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q3',other_option='IBB'))
        elif other_price_diff_options == 'CTDMS':
            st.plotly_chart(price_diff_other(df_ti,q1='Q1',q2='Q2',q3='Q3',other='CTDMS Price',other_price_diff_options='CTDMS'))
        elif other_price_diff_options == 'PO Selected':
            st.plotly_chart(price_diff_other(df_ti,q1='Q1',q2='Q2',q3='Q3',other='PO Selected Price',other_price_diff_options='PO Selected'))
    elif diff == '%':
        if reco_price_diff_options == 'Q1' and other_price_diff_options == 'IBB':
            st.plotly_chart(percent_diff(df_ti,reco = 'PDAI Price MIN',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q1',other_option='IBB'))
        elif reco_price_diff_options == 'Q2' and other_price_diff_options == 'IBB':
            st.plotly_chart(percent_diff(df_ti,reco = 'PDAI Price AVG',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q2',other_option='IBB'))
        elif reco_price_diff_options == 'Q3' and other_price_diff_options == 'IBB':
            st.plotly_chart(percent_diff(df_ti,reco = 'PDAI Price Max',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q3',other_option='IBB'))
        elif other_price_diff_options == 'CTDMS':
            st.plotly_chart(percent_diff_other(df_ti,q1='Q1',q2='Q2',q3='Q3',other='CTDMS Price',other_price_diff_options='CTDMS'))
        elif other_price_diff_options == 'PO Selected':
            st.plotly_chart(percent_diff_other(df_ti,q1='Q1',q2='Q2',q3='Q3',other='PO Selected Price',other_price_diff_options='PO Selected'))

elif type== 'Retail':

    if diff == 'Price':
        
        if reco_price_diff_options == 'Q1' and other_price_diff_options == 'IBB':
            st.plotly_chart(price_diff(df_re,reco = 'PDAI Price MIN',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q1',other_option='IBB'))
        elif reco_price_diff_options == 'Q2' and other_price_diff_options == 'IBB':
            st.plotly_chart(price_diff(df_re,reco = 'PDAI Price AVG',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q2',other_option='IBB'))
        elif reco_price_diff_options == 'Q3' and other_price_diff_options == 'IBB':
            st.plotly_chart(price_diff(df_re,reco = 'PDAI Price Max',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q3',other_option='IBB'))
        elif other_price_diff_options == 'CTDMS':
            st.plotly_chart(price_diff_other(df_re,q1='Q1',q2='Q2',q3='Q3',other='CTDMS Price',other_price_diff_options='CTDMS'))
        elif other_price_diff_options == 'PO Selected':
            st.plotly_chart(price_diff_other(df_re,q1='Q1',q2='Q2',q3='Q3',other='PO Selected Price',other_price_diff_options='PO Selected'))
    elif diff == '%':
        if reco_price_diff_options == 'Q1' and other_price_diff_options == 'IBB':
            st.plotly_chart(percent_diff(df_re,reco = 'PDAI Price MIN',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q1',other_option='IBB'))
        elif reco_price_diff_options == 'Q2' and other_price_diff_options == 'IBB':
            st.plotly_chart(percent_diff(df_re,reco = 'PDAI Price AVG',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q2',other_option='IBB'))
        elif reco_price_diff_options == 'Q3' and other_price_diff_options == 'IBB':
            st.plotly_chart(percent_diff(df_re,reco = 'PDAI Price Max',fair = 'IBB Fair Price',market = 'IBB Market Price',best='IBB Best Price',reco_option='Q3',other_option='IBB'))
        elif other_price_diff_options == 'CTDMS':
            st.plotly_chart(percent_diff_other(df_re,q1='Q1',q2='Q2',q3='Q3',other='CTDMS Price',other_price_diff_options='CTDMS'))
        elif other_price_diff_options == 'PO Selected':
            st.plotly_chart(percent_diff_other(df_re,q1='Q1',q2='Q2',q3='Q3',other='PO Selected Price',other_price_diff_options='PO Selected'))
