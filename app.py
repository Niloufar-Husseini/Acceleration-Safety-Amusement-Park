import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import base64
from scipy.signal import butter, lfilter
from functions import *

# --- Set Page Layout to Wide ---
st.set_page_config(layout="wide")


# --- CSS Styling ---
st.markdown(
    """
    <style>
        /* Default background and text color */
        .stApp {
            background-color: #FFFFFF !important;  /* White background */
            color: #333333 !important;  /* Dark text for contrast */
        }

        /* Restore default container behavior */
        .stContainer {
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Default button styling */
        div.stButton > button:first-child {
            background-color: #2196F3 !important;  /* Blue button */
            color: white !important;
            border-radius: 8px !important;
            height: 3em !important;
            font-size: 16px !important;
            border: none !important;
        }

        div.stButton > button:first-child:hover {
            background-color: #1976D2 !important;  /* Darker blue for hover effect */
        }

        /* Default headers styling */
        h1 {
            color: #2196F3 !important;
            font-size: 36px !important;
            text-align: center !important;
            font-weight: bold !important;
        }

        /* Default text for labels and inputs */
        .stSelectbox label, .stNumberInput label {
            color: #333333 !important;
            font-weight: bold !important;
        }

        /* Default success/error messages styling */
        .stSuccess {
            background-color: #388E3C !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-weight: bold !important;
        }

        .stError {
            background-color: #D32F2F !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-weight: bold !important;
        }

        /* Default markdown styling */
        .stMarkdown p {
            color: #333333 !important;
        }

        /* Success/Error Button */
        .stSuccess, .stError {
            font-size: 16px !important;
            text-align: center !important;
            border-radius: 8px !important;
        }
        
        /* Table styling */
        .stDataFrame {
            width: 100% !important;  /* Ensure the table takes up full width */
            table-layout: auto !important;  /* Allow columns to adjust based on content */
        }

        table {
            width: 100% !important;  /* Make sure the table is full width */
            table-layout: auto !important;  /* Allow table columns to adjust dynamically */
            color: #333333 !important;  /* Set text color for table content */
        }

        th, td {
            padding: 8px !important;
            text-align: left !important;
            border: 1px solid #ddd !important;  /* Border styling */
        }

        .stDataFrame > div > div {
            background-color: #FFFFFF !important;  /* Ensure background color for tables */
        }

        .stDataFrame table {
            width: 100% !important;  /* Full width for tables */
            font-size: 14px !important;  /* Set font size */
            word-wrap: break-word !important;  /* Prevent word overflow */
        }
        
        /* ---- shrink every st.image ---- */
        .stApp img {
            max-width: 70% !important;   /* try 30 %, 50 %, 200 px, whatever */
            height: auto !important;     /* keep aspect ratio */
            display: block;              /* centre it (optional) */
            margin-left: auto;
            margin-right: auto;
        }


    </style>
    """,
    unsafe_allow_html=True,
)


# --- Nexgen Logo ---
LOGO_URL = "assets/Logo3.png"

if os.path.exists(LOGO_URL):
    with open(LOGO_URL, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode("utf-8")
    st.markdown(
        f"""
        <div style='display: flex; justify-content: center;'>
            <img src='data:image/png;base64,{encoded}' width='200'>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.warning("Logo not found at 'assets/Logo3.png'")

# --- Title ---
st.markdown(
    """<h1 style='color: #2196F3; font-size: 40px; text-align: center;
            font-weight: bold;'>Acceleration Effects on Passengers</h1>""",
    unsafe_allow_html=True,
)
st.markdown(
    """<h2 style='color: #2196F3;font-size: 35px; text-align: center;
            font-weight: bold;'>Medical Tolerances</h2>""",
    unsafe_allow_html=True,
)
st.markdown(
    """<h3 style='color: #2196F3; font-size: 30px; text-align: center;
            font-weight: bold;'>when USING AMUSEMENT DEVICES ⚙️</h3>""",
    unsafe_allow_html=True,
)
st.markdown(
    """<h3 style='color: #000000; font-size: 20px; text-align: center;
            font-weight: bold;'>Standard: BS ISO 17842-1:2023, Safety of amusement rides and amusement devices, Part 1: Design and manufacture</h3>""",
    unsafe_allow_html=True,
)

# --- Image and Guide ---
st.subheader("Body Coordinate System:")
AXIS_GUIDE_URL = "assets/Axis_Guide_new.png"
st.image(AXIS_GUIDE_URL, caption="3-axis X-Y-Z", use_column_width=True)

st.write(
    """
This diagram shows how the X, Y, and Z axes are oriented 
relative to the human body while seated in the amusement vehicle.  
It is used as a guide when interpreting acceleration data 
from the mounted sensors.  
"""
)

st.subheader(
    "Acceleration is defined in accordance with the following coordinate system:"
)
st.markdown(
    "+a<sub>z</sub> presses the body into the seat downwards, described as “eyes down”.<br>"
    "−a<sub>z</sub> lifts the body out of the seat, described as “eyes up”.<br>"
    "+a<sub>y</sub> presses the body sideward to the right, described as “eyes right”.<br>"
    "−a<sub>y</sub> presses the body sideward to the left, described as “eyes left”.<br>"
    "+a<sub>x</sub> presses the body into the seat backward, described as “eyes back”.<br>"
    "−a<sub>x</sub> pushes the body out of the seat forward, described as “eyes front”.",
    unsafe_allow_html=True,
)


# --- Mode Selection ---
mode = st.radio("Select Mode", ["Manual Input", "Upload Dataset"])

# --- Manual Mode ---
if mode == "Manual Input":
    ride_type = st.selectbox(
        "Ride Vehicle", ["Over the shoulder restraint", "Base case (typical restraint)"]
    )
    axis = st.selectbox("Axis", ["X", "Y", "Z"])
    g_force = st.number_input("Acceleration (g)", value=1.0)
    duration = st.number_input("Duration (seconds)", value=1.0)

    if st.button("Check Safety"):
        result = check_safety(axis, g_force, duration, ride_type)

        if "Safe" in result:
            st.success(f"Result: {result}")
        else:
            st.error(f"Result: {result}")

# --- Dataset Mode ---
else:
    ride_type = st.selectbox(
        "Ride Vehicle", ["Over the shoulder restraint", "Base case (typical restraint)"]
    )

    data_mode = st.radio("Select Data", ["Upload File", "Sample File"])
    if data_mode == 'Upload File':
        uploaded_file = st.file_uploader("Upload IMU CSV/TXT file", type=["csv", "txt"])
        if uploaded_file is not None:
            final_file = uploaded_file
            call_calculations(final_file, ride_type)
    elif data_mode == 'Sample File':
        default_file_url = 'assets/simulated_unsafe_imu.txt'
        st.header("Sample data")
        final_file = default_file_url
        call_calculations(final_file, ride_type)
