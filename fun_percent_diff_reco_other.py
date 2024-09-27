import pandas as pd # type: ignore
import plotly.graph_objects as go# type: ignore
from plotly.subplots import make_subplots# type: ignore
import streamlit as st # type: ignore


def percent_diff_other(df_ti, q1, q2, q3, other,other_price_diff_options):

    st.write(f'Disrubution of %Difference[PDAI Reco - {other_price_diff_options}]')
    hist_ti = pd.DataFrame()
    ti_cols = ['PDAI Price MIN', 'PDAI Price AVG', 'PDAI Price Max']
    ti_prefix = 'ti_FINAL - '

    # Calculate the difference between the PDAI prices and the other price
    for colu in ti_cols:
        hist_ti[ti_prefix + colu] = ((df_ti[colu] - df_ti[other])/df_ti[other])*100

    ti_dict = {}

    # Create bins and group data for each price type
    for col_name in hist_ti.columns:
        ti_mar_hist = pd.cut(hist_ti[col_name], right=False,
        bins = [-100,-90, -80, -70, -60, -50, -40, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, 30,
                     40, 50, 60, 70, 80, 90, 100.01, 150, 200, 400, 700],
        labels = ['-100% to -90%', '-90% to -80%', '-80% to -70%', '-70% to -60%', '-60% to -50%',
                        '-50% to -40%', '-40% to -30%', '-30% to -20%', '-20% to -15%', '-15% to -10%',
                        '-10% to -5%', '-5% to 0%', '0% to 5%', '5% to 10%', '10% to 15%', '15% to 20%',
                        '20% to 30%', '30% to 40%', '40% to 50%', '50% to 60%', '60% to 70%', '70% to 80%',
                        '80% to 90%', '90% to 100.01%', '100.01% to 150%', '150% to 200%', '200% to 400%',
                        '400% to 700%'])
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
    ti.update_xaxes(title_text=f"<b> %DIFF [PDAI Reco - {other_price_diff_options}] </b>", showgrid=False,tickangle=90)
    ti.update_yaxes(title_text="<b> nCars </b>", secondary_y=False, showgrid=False)
    ti.update_yaxes(title_text="<b> cum_% </b>", secondary_y=True, showgrid=False)

    return ti
