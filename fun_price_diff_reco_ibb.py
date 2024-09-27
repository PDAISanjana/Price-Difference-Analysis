import pandas as pd # type: ignore
import plotly.graph_objects as go # type: ignore
from plotly.subplots import make_subplots # type: ignore
import streamlit as st # type: ignore

def price_diff(df_ti, reco, fair, market, best, reco_option, other_option):

    st.write(f'Disrubution of Difference[PDAI Reco{reco_option} - IBB]')
    # Creating an empty DataFrame to store differences
    hist_ti = pd.DataFrame()

    # Defining columns to calculate differences
    ti_cols = [fair, market, best]
    ti_prefix = 'ti_FINAL - '

    # Calculating differences between reco price and each price type
    for colu in ti_cols:
        hist_ti[ti_prefix + colu] = df_ti[reco] - df_ti[colu]

    # Binning and counting occurrences for each difference column
    ti_dict = {}
    for col_name in hist_ti.columns:
        ti_mar_hist = pd.cut(
            hist_ti[col_name], 
            right=False,
            bins=[-1200000, -1000000, -900000, -800000, -700000, -600000, -500000, -400000,
                  -300000, -250000, -200000, -150000, -100000, -50000, 0, 50000, 100000, 150000, 200000,
                  250000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1200000, 1400000,
                  1600000, 1800000, 3500000],
            labels=['-12L to -10L', '-10L to -9L', '-9L to -8L', '-8L to -7L', '-7L to -6L',
                    '-6L to -5L', '-5L to -4L', '-4L to -3L', '-3L to -2.5L', '-2.5L to -2L', '-2L to -1.5L',
                    '-1.5L to -1L', '-1L to -0.5L', '-0.5L to 0', '0 to 0.5L', '0.5L`1 to 1L', '1L to 1.5L',
                    '1.5L to 2L', '2L to 2.5L', '2.5L to 3L', '3L to 4L', '4L to 5L', '5L to 6L', '6L to 7L',
                    '7L to 8L', '8L to 9L', '9L to 10L', '10L to 12L', '12L to 14L', '14L to 16L',
                    '16L to 18L', '18L to 35L']
        )

        # Counting occurrences for each bin
        ti_mar = hist_ti.groupby(ti_mar_hist)[col_name].count().reset_index(name='Count').to_dict(orient='records')

        # Store the result DataFrame in the dictionary
        ti_dict[col_name + '_RESULT'] = pd.DataFrame(ti_mar)

    # Calculating cumulative percentage for each difference column
    cumu_per_ti_dict = {}
    for key, valu in ti_dict.items():
        cum_sum = valu['Count'].cumsum()
        cum_per = (cum_sum / cum_sum.max()) * 100
        valu['cumu%'] = cum_per
        cumu_per_ti_dict[key] = valu

    # Creating the plot with secondary y-axis
    ti = make_subplots(specs=[[{"secondary_y": True}]])

    # Adding bar and scatter traces for each price type
    for price_type in ['IBB Fair Price', 'IBB Market Price', 'IBB Best Price']:
        # Adding bar traces (nCars) with larger text size
        ti.add_trace(
            go.Bar(x=cumu_per_ti_dict[f'ti_FINAL - {price_type}_RESULT'][f'ti_FINAL - {price_type}'],
                   y=cumu_per_ti_dict[f'ti_FINAL - {price_type}_RESULT']['Count'],
                #    text=cumu_per_ti_dict[f'ti_FINAL - {price_type}_RESULT']['Count'],
                #    textfont=dict(size=35),  # Increased font size for bar text
                   name=price_type.split()[1]), secondary_y=False
        )
        # Adding scatter traces (cumulative %) with markers
        ti.add_trace(
            go.Scatter(x=cumu_per_ti_dict[f'ti_FINAL - {price_type}_RESULT'][f'ti_FINAL - {price_type}'],
                       y=cumu_per_ti_dict[f'ti_FINAL - {price_type}_RESULT']['cumu%'],
                       mode='lines+markers',  # Adding markers to the line
                       marker=dict(size=6),  # Size of the markers
                       name=f"cum%_{price_type.split()[1]}"), secondary_y=True
        )

    # Updating layout for better presentation
    ti.update_layout(
        autosize=False,
        width=1200,
        height=500,
        legend=dict(x=0.8, y=1.5, traceorder="normal", font=dict(size=12), borderwidth=1)
    )

    # Updating x-axis and y-axes
    ti.update_xaxes(title_text=f"<b> DIFF [PDAI Reco{reco_option} - {other_option}] </b>", showgrid=False,tickangle=90)
    ti.update_yaxes(title_text="<b> nCars </b>", secondary_y=False, showgrid=False)
    ti.update_yaxes(title_text="<b> cum_% </b>", secondary_y=True, showgrid=False)


    # Display the figure
    return ti
