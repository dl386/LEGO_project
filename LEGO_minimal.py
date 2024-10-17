import streamlit as st
import pandapower as pp
import plotly.graph_objects as go
import pandapower.plotting.plotly as pplotly
import pandapower.plotting as plot
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import numpy as np


st.set_page_config(layout="wide")
def app():
    # Start the root App
    st.title('LEGO minimal example')
    col1, col2, col3 = st.columns([1, 2, 3], gap='small')
    with col1:
    # Load slider
        KHMI = st.toggle("Kontrola preko HMI", value=False)
        if KHMI == 1:
            S_1 = st.toggle('Stikalo S1', value=True,disabled=False)
            S_2 = st.toggle('Stikalo S2', value=True,disabled=False)
        else:
            S_1 = st.toggle('Stikalo S1', value=True, disabled=True)
            S_2 = st.toggle('Stikalo S2', value=True, disabled=True)

    data = pd.DataFrame(
        {
            'Frekvenca / Hz': ['50,01'],
            'Napetost / kV': ['110,23'],
            'Moč SG / MW': ['69,11'],
        }
    )
    with col2:
        # Use st.write() for a basic table
        st.data_editor(data)

        plot_bgcolor = "#def"
        quadrant_colors = [plot_bgcolor, "#2bad4e", "#eff229", "#f25829","#eff229", "#2bad4e"]
        quadrant_text = ["", "<b>Very high</b>", "<b>High</b>", "<b>Medium</b>", "<b>Low</b>", "<b>Very low</b>"]
        n_quadrants = len(quadrant_colors) - 1

        current_value = 50.01
        min_value = 40
        max_value = 60
        hand_length = np.sqrt(2) / 4
        hand_angle = np.pi * (1 - (max(min_value, min(max_value, current_value)) - min_value) / (max_value - min_value))

        fig = go.Figure(
            data=[
                go.Pie(
                    values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                    rotation=90,
                    hole=0.5,
                    marker_colors=quadrant_colors,
                    text=quadrant_text,
                    textinfo="text",
                    hoverinfo="skip",
                ),
            ],
            layout=go.Layout(
                showlegend=False,
                margin=dict(b=0, t=10, l=10, r=10),
                width=450,
                height=450,
                paper_bgcolor=plot_bgcolor,
                annotations=[
                    go.layout.Annotation(
                        text=f"<b>Frekvenca / Hz:</b><br>{current_value} units",
                        x=0.5, xanchor="center", xref="paper",
                        y=0.25, yanchor="bottom", yref="paper",
                        showarrow=False,
                    )
                ],
                shapes=[
                    go.layout.Shape(
                        type="circle",
                        x0=0.48, x1=0.52,
                        y0=0.48, y1=0.52,
                        fillcolor="#333",
                        line_color="#333",
                    ),
                    go.layout.Shape(
                        type="line",
                        x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                        y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                        line=dict(color="#333", width=4)
                    )
                ]
            )
        )
        st.plotly_chart(fig)

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Create a figure

    x2 = np.linspace(0, 10, 100)
    y2 = 110 * np.ones(len(x))


    # Plot the figure in streamlit
    with col3:
        st.line_chart(pd.DataFrame(y), x_label="Čas", y_label="Frekvenca / Hz", color="#ff0000")
        st.line_chart(pd.DataFrame(y2), x_label="Čas", y_label="Napetost / kv", color="#00FFFF")

    return KHMI
        #st.pyplot(fig2)
    ## Create or load your pandapower network here
    #net = pp.create_empty_network()
#
    #b1 = pp.create_bus(net, vn_kv=110.)
    #b2 = pp.create_bus(net, vn_kv=20.)
    #b3 = pp.create_bus(net, vn_kv=20.)
    #b4 = pp.create_bus(net, vn_kv=20.)
    #pp.create_ext_grid(net, bus=b1)
    ## Create transformers
    #pp.create_transformer(net, b1, b2, std_type="25 MVA 110/20 kV")
#
    ## Create 110 kV line
    #pp.create_line(net, b2, b3, length_km=10., std_type='149-AL1/24-ST1A 110.0')
    #pp.create_line(net, b3, b4, length_km=10., std_type='149-AL1/24-ST1A 110.0')
#
    ## Add loads as per the slider value
    #for i in range(num_loads):
    #    pp.create_load(net, bus=b4, p_mw=3)
    #net.bus_geodata.drop(net.bus_geodata.index, inplace=True)
    #net.line_geodata.drop(net.line_geodata.index, inplace=True)
    #plot.create_generic_coordinates(net, respect_switches=True)
    #plot.fuse_geodata(net)
    #net.bus_geodata.loc[:, 'x'] = net.bus_geodata.loc[:, 'x'] * 1.5
    #net.bus_geodata.loc[0, 'x'] = net.bus_geodata.loc[0, 'x'] - 1
    #net.bus_geodata.loc[0, 'y'] = net.bus_geodata.loc[0, 'y'] + 0.01
    #pp.runpp(net)
    #transformer_loading = net.res_trafo['loading_percent']
    #voltages = net.res_bus['vm_pu']
#
#
    #bt = pplotly.create_bus_trace(net, cmap_vals=voltages, cmap=True, cbar_title='Voltage / p.u.', trace_name='Node', size=10)
    #lt = pplotly.create_line_trace(net, cmap=True)
    #tc = pplotly.create_trafo_trace(net, net.trafo.index, trafotype='2W', color='blue', infofunc=net.trafo.name, cmap='Accent', cmin=0, cmax=1, cmap_vals=transformer_loading, use_line_geodata=None, trace_name='SN/NN transformator', width=2.5)
    #x_coords = []
    #y_coords = []
#
    #for trace in bt:
    #    x_coords.extend(trace['x'])
    #    y_coords.extend([y + 0.3 for y in trace['y']])
#
    #node_names = [str(bus + 1) for bus in net.bus.index]
#
    #background_trace = go.Scatter(x=[0, 1, 1, 0, 0], y=[0, 0, 1, 1, 0], fill='toself',
    #                              fillcolor='rgba(240, 240, 240, 0.7)', line=dict(color='rgba(255, 255, 255, 0)'),
    #                              showlegend=False)
    ## Create a new trace containing the node numbers as annotations
    #node_numbers_trace = go.Scatter(x=x_coords, y=y_coords, text=node_names,
    #                                mode='text', textposition='middle center', hoverinfo='skip', showlegend=False)
    #fig = go.Figure(data=[background_trace] + lt + bt + tc + [node_numbers_trace])
    ## fig = pplotly.draw_traces(lt + bt + tc+[node_numbers_trace], showlegend=True)
    #fig.update_layout(
    #    width=800,  # Set the width of the figure in pixels
    #    height=900,  # Set the height of the figure in pixels
    #    xaxis=dict(showline=False, showgrid=False, zeroline=False, showticklabels=False),
    #    yaxis=dict(showline=False, showgrid=False, zeroline=False, showticklabels=False),
    #    legend=dict(
    #        orientation="h",
    #        yanchor="bottom",
    #        y=1.02,
    #        xanchor="right",
    #        x=1
    #    ))
    ##fig.show()
#
    #fig.write_html("network_plot.html")
    #with open("network_plot.html", 'r', encoding='utf-8') as f:
    #    html_data = f.read()
    ##st.write('<iframe src="network_plot.html" width=700 height=450></iframe>', unsafe_allow_html=True)
    #st.components.v1.html(html_data, scrolling=True, height=1000, width = 1000)
    #st.subheader('Line Results')
    #st.write(net.res_line)
#
    #st.subheader('Transformer Results')
    #st.write(net.res_trafo)
#
    #st.subheader('Power Flow Result')
#
    #st.write(net.res_bus)


app()