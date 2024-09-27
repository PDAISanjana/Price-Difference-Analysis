import pandas as pd # type: ignore
import plotly.graph_objects as go # type: ignore
from plotly.subplots import make_subplots # type: ignore
import streamlit as st # type: ignore

def percent_diff(df_ti, reco, fair, market, best, reco_option, other_option):
    # Creating an empty DataFrame to store differences
    st.write(f'Disrubution of %Difference[PDAI Reco{reco_option} - IBB]')

    hist_ti = pd.DataFrame()

    # Defining columns to calculate differences
    ti_cols = [fair, market, best]
    ti_prefix = 'ti_FINAL - '

    # Calculating differences between reco price and each price type
    for colu in ti_cols:
        hist_ti[ti_prefix + colu] = ((df_ti[reco] - df_ti[colu])/df_ti[colu])*100


    # Binning and counting occurrences for each difference column
    ti_dict = {}
    for col_name in hist_ti.columns:
        ti_mar_hist = pd.cut(
            hist_ti[col_name], 
            right=False,
            bins = [-100,-90, -80, -70, -60, -50, -40, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, 30,
                     40, 50, 60, 70, 80, 90, 100.01, 150, 200, 400, 700],
            labels = ['-100% to -90%', '-90% to -80%', '-80% to -70%', '-70% to -60%', '-60% to -50%',
                        '-50% to -40%', '-40% to -30%', '-30% to -20%', '-20% to -15%', '-15% to -10%',
                        '-10% to -5%', '-5% to 0%', '0% to 5%', '5% to 10%', '10% to 15%', '15% to 20%',
                        '20% to 30%', '30% to 40%', '40% to 50%', '50% to 60%', '60% to 70%', '70% to 80%',
                        '80% to 90%', '90% to 100.01%', '100.01% to 150%', '150% to 200%', '200% to 400%',
                        '400% to 700%'])

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
    ti.update_xaxes(title_text=f"<b> %DIFF [PDAI Reco{reco_option} - {other_option}] </b>", showgrid=False,tickangle=90)
    ti.update_yaxes(title_text="<b> nCars </b>", secondary_y=False, showgrid=False)
    ti.update_yaxes(title_text="<b> cum_% </b>", secondary_y=True, showgrid=False)

    # Display the figure
    return ti
