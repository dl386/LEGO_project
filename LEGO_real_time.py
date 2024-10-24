#import streamlit as st
#import time
## Streamlit GUI setup
#st.title("Raspberry Pi Signal Monitor")
#
#digital_placeholder = st.empty()
#analog_placeholder = st.empty()
#toggle_switch = st.checkbox("Toggle Output")
#a= 1
#while True:
#    a = a+1
#    # Update GUI
#    digital_placeholder.text(f"Digital Signal: {a}")
#    analog_placeholder.text(f"Analog Signal: {a}")
#    time.sleep(.3)

import RPi.GPIO as GPIO
import spidev
import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
#test

# GPIO setup
GPIO.setmode(GPIO.BCM)
digital_input_pin = 17
toggle_output_pin = 27
GPIO.setup(digital_input_pin, GPIO.IN)
GPIO.setup(toggle_output_pin, GPIO.OUT)

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000


def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


# Streamlit GUI setup
st.title('LEGO minimal example')
st.set_page_config(layout="wide")


# Function to refresh the data and UI
def refresh_data():
    col1, col2, col3 = st.columns([1, 2, 3], gap='small')

    with col1:
        KHMI = st.checkbox("Kontrola preko HMI", value=False)
        if KHMI:
            S_1 = st.checkbox('Stikalo S1', value=True, disabled=False)
            S_2 = st.checkbox('Stikalo S2', value=True, disabled=False)
        else:
            S_1 = st.checkbox('Stikalo S1', value=True, disabled=True)
            S_2 = st.checkbox('Stikalo S2', value=True, disabled=True)

    data = pd.DataFrame({
        'Frekvenca / Hz': ['50,01'],
        'Napetost / kV': ['110,23'],
        'Moč SG / MW': ['69,11'],
    })

    with col2:
        st.data_editor(data)

        plot_bgcolor = "#def"
        quadrant_colors = [plot_bgcolor, "#2bad4e", "#eff229", "#f25829", "#eff229", "#2bad4e"]
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

    x2 = np.linspace(0, 10, 100)
    y2 = 110 * np.ones(len(x))

    with col3:
        st.line_chart(pd.DataFrame(y), x_label="Čas", y_label="Frekvenca / Hz", color="#ff0000")
        st.line_chart(pd.DataFrame(y2), x_label="Čas", y_label="Napetost / kV", color="#00FFFF")


# Main loop
while True:
    refresh_data()
    time.sleep(1)
    st.experimental_rerun()
