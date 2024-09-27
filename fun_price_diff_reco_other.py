import pandas as pd # type: ignore
import plotly.graph_objects as go# type: ignore
from plotly.subplots import make_subplots# type: ignore
import streamlit as st # type: ignore

def price_diff_other(df_ti, q1, q2, q3, other,other_price_diff_options):

    st.write(f'Disrubution of Difference[PDAI Reco - {other_price_diff_options}]')

    hist_ti = pd.DataFrame()
    ti_cols = ['PDAI Price MIN', 'PDAI Price AVG', 'PDAI Price Max']
    ti_prefix = 'ti_FINAL - '

    # Calculate the difference between the PDAI prices and the other price
    for colu in ti_cols:
        hist_ti[ti_prefix + colu] = df_ti[colu] - df_ti[other]

    ti_dict = {}

    # Create bins and group data for each price type
    for col_name in hist_ti.columns:
        ti_mar_hist = pd.cut(hist_ti[col_name], right=False,
                             bins=[-8500000, -1400000, -1200000, -1000000, -900000, -800000, -700000, -600000, -500000, 
                                   -400000, -300000, -250000, -200000, -150000, -100000, -50000, 0, 50000, 100000, 
                                   150000, 200000, 250000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 
                                   1000000, 1200000, 1400000, 1600000, 1800000, 3500000],
                             labels=['-85L to -14L', '-14L to -12L', '-12L to -10L', '-10L to -9L', '-9L to -8L', '-8L to -7L', 
                                     '-7L to -6L', '-6L to -5L', '-5L to -4L', '-4L to -3L', '-3L to -2.5L', '-2.5L to -2L', 
                                     '-2L to -1.5L', '-1.5L to -1L', '-1L to -0.5L', '-0.5L to 0', '0 to 0.5L', '0.5L to 1L', 
                                     '1L to 1.5L', '1.5L to 2L', '2L to 2.5L', '2.5L to 3L', '3L to 4L', '4L to 5L', 
                                     '5L to 6L', '6L to 7L', '7L to 8L', '8L to 9L', '9L to 10L', '10L to 12L', 
                                     '12L to 14L', '14L to 16L', '16L to 18L', '18L to 35L'])

        ti_mar = hist_ti.groupby(ti_mar_hist)[col_name].count().reset_index(name='Count').to_dict(orient='records')
        ti_mar_df = pd.DataFrame(ti_mar)

        # Store the result DataFrame in the dictionary with unique names
        ti_dict[col_name + '_RESULT'] = ti_mar_df

    cumu_per_ti_dict = {}

    # Calculate cumulative percentage for each result
    for key, valu in ti_dict.items():
        cum_sum = valu['Count'].cumsum()
        cum_per = (cum_sum / cum_sum.max()) * 100
        valu['cumu%'] = cum_per
        cumu_per_ti_dict[key] = valu

    # Create a subplot with secondary y-axis
    ti = make_subplots(specs=[[{"secondary_y": True}]])

    # Plot Q1
    ti.add_trace(go.Bar(x=cumu_per_ti_dict[ti_prefix + 'PDAI Price MIN_RESULT'][ti_prefix + 'PDAI Price MIN'],
                        y=cumu_per_ti_dict[ti_prefix + 'PDAI Price MIN_RESULT']['Count'],
                        # text=cumu_per_ti_dict[ti_prefix + 'PDAI Price MIN_RESULT']['Count'], 
                        name=f'{q1}-{other_price_diff_options}'), secondary_y=False)

    ti.add_trace(go.Scatter(x=cumu_per_ti_dict[ti_prefix + 'PDAI Price MIN_RESULT'][ti_prefix + 'PDAI Price MIN'],
                            y=cumu_per_ti_dict[ti_prefix + 'PDAI Price MIN_RESULT']['cumu%'], 
                            name=f'cum%_{q1}-CTDMS', mode='lines+markers'), secondary_y=True)

    # Plot Q2
    ti.add_trace(go.Bar(x=cumu_per_ti_dict[ti_prefix + 'PDAI Price AVG_RESULT'][ti_prefix + 'PDAI Price AVG'],
                        y=cumu_per_ti_dict[ti_prefix + 'PDAI Price AVG_RESULT']['Count'],
                        # text=cumu_per_ti_dict[ti_prefix + 'PDAI Price AVG_RESULT']['Count'], 
                        name=f'{q2}-{other_price_diff_options}'), secondary_y=False)

    ti.add_trace(go.Scatter(x=cumu_per_ti_dict[ti_prefix + 'PDAI Price AVG_RESULT'][ti_prefix + 'PDAI Price AVG'],
                            y=cumu_per_ti_dict[ti_prefix + 'PDAI Price AVG_RESULT']['cumu%'], 
                            name=f'cum%_{q2}-CTDMS', mode='lines+markers'), secondary_y=True)

    # Plot Q3
    ti.add_trace(go.Bar(x=cumu_per_ti_dict[ti_prefix + 'PDAI Price Max_RESULT'][ti_prefix + 'PDAI Price Max'],
                        y=cumu_per_ti_dict[ti_prefix + 'PDAI Price Max_RESULT']['Count'],
                        # text=cumu_per_ti_dict[ti_prefix + 'PDAI Price Max_RESULT']['Count'], 
                        name=f'{q3}-{other_price_diff_options}'), secondary_y=False)

    ti.add_trace(go.Scatter(x=cumu_per_ti_dict[ti_prefix + 'PDAI Price Max_RESULT'][ti_prefix + 'PDAI Price Max'],
                            y=cumu_per_ti_dict[ti_prefix + 'PDAI Price Max_RESULT']['cumu%'], 
                            name=f'cum%_{q3}-CTDMS', mode='lines+markers'), secondary_y=True)

    # Update layout with the legend above the plot
    ti.update_layout(
        autosize=False,
        width=1200,
        height=500,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=1.5,
            xanchor="right",
            x=0.8
        )
    )

    # Update axes
    ti.update_xaxes(title_text=f"<b> DIFF [PDAI Reco - {other_price_diff_options}] </b>", showgrid=False,tickangle=90)
    ti.update_yaxes(title_text="<b> nCars </b>", secondary_y=False, showgrid=False)
    ti.update_yaxes(title_text="<b> cum_% </b>", secondary_y=True, showgrid=False)

    return ti
