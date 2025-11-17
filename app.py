import streamlit as st
import streamlit.components.v1 as components 
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
            color: #003366 !important;
            font-size: 36px !important;
            text-align: center !important;
            font-weight: bold !important;
        }

        h3 {
            color: #003366;
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
        
        /* Remove paddings around main container */
        .block-container {
            padding-top: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
            margin: 0 !important;
        }

        /* Make banner image full width */
        .banner-image {
            width: 100% !important;
            height: auto !important;
            display: block;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Make all other images smaller as before */
        .stApp img:not(.banner-image) {
            max-width: 70% !important;
            height: auto !important;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        .title-container {
            display: flex;
            align-items: center;      /* vertically center */
            width: 100%;
        }

        .logo-left {
            flex: 0 0 10%;            /* logo takes 20% of horizontal space */
            max-width: 100px;         /* optional maximum size */
            height: auto;
            margin-right: 0px;       /* space between logo and text */
        }

        .title-text {
            flex: 1;                  /* takes remaining space */
        }

        /* ---- Center Tabs + Increase Font Size ---- */
        .stTabs [role="tablist"] {
            justify-content: center !important;   /* center the whole row */
        }

        .stTabs [role="tab"] {
            font-size: 22px !important;           /* bigger tab text */
            padding: 12px 24px !important;        /* larger click area */
            font-weight: 600 !important;          /* make them bold */
        }

        .stTabs [aria-selected="true"] {
            border-bottom: 3px solid #2196F3 !important;  /* highlight selected tab */
            color: #2196F3 !important;
        }





    </style>
    """,
    unsafe_allow_html=True,
)





# --- Ropewise software banner ---
Banner_URL = "assets/Logo for a Software called RopeWise, in ropeway calculation (1).jpg"

if os.path.exists(Banner_URL):
    with open(Banner_URL, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode("utf-8")
    st.markdown(
    f"""
    <img class='banner-image' src='data:image/png;base64,{encoded}'>
    """,
    unsafe_allow_html=True,
)
else:
    st.warning("Logo not found at 'assets/Logo for a Software called RopeWise, in ropeway calculation (1).jpg'")

# Load the logo
LOGO_URL = "assets/Logo3.png"
if os.path.exists(LOGO_URL):
    with open(LOGO_URL, "rb") as f:
        data = f.read()
    encoded_logo = base64.b64encode(data).decode("utf-8")

    html_code = f"""
    <div style="display: flex; align-items: center; width: 100%;">

        <div style="flex: 0 0 20%; text-align:center;">
            <img src='data:image/png;base64,{encoded_logo}' style="max-width:120px; height:auto;">
            <a href="https://nexgen-cableway.com/" target="_blank">
                <button style="
                    background-color:#2196F3;
                    color:white;
                    padding:10px 20px;
                    border:none;
                    border-radius:8px;
                    font-size:18px;
                    cursor:pointer;
                    margin-top: 12px;">
                    Visit Website 🌐
                </button>
            </a>
        </div>

        <div style="flex: 1; padding-left: 25px;">
            <h3 style='color:#003366; font-size:40px; font-weight:bold; margin:0;'>
                Acceleration Effects on Passengers Medical Tolerances
            </h3>
            <h3 style='color:#003366; font-size:40px; font-weight:bold; margin:0;'>
                When Using Amusement Devices
            </h3>
        </div>

    </div>
    """

    # Render HTML properly
    components.html(html_code, height=200)

else:
    st.warning("Logo not found at 'assets/Logo3.png'")

tab1, tab2 = st.tabs(["Body Coordinate System", "Mode Selection"])

with tab1:
    # --- Standards ---
    st.subheader("Standards:")
    st.markdown(
            f"""
            <div>
                <ul>
                    <li>
                        BS ISO 17842-1:2023, Safety of amusement rides and amusement devices
                    </li>
                    <li>
                        AS 3533, Amusement rides and devices
                    </li> 
                    <li>
                        INSO 8987
                    </li>              
                </ul>
                <a href="https://nexgen-cableway.com/standard-files/" target="_blank">
                    <button style="
                        background-color:#2196F3;
                        color:white;
                        padding:12px 12px;
                        border:none;
                        border-radius:8px;
                        font-size:14px;
                        cursor:pointer;
                    ">
                        Open Standards 🌐
                    </button>
                </a>
            </div>
            """,
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


# # --- Standards ---
# st.subheader("Standards:")
# st.markdown(
#         f"""
#         <div>
#             <ul>
#                 <li>
#                     BS ISO 17842-1:2023, Safety of amusement rides and amusement devices
#                 </li>
#                 <li>
#                     AS 3533, Amusement rides and devices
#                 </li> 
#                 <li>
#                     INSO 8987
#                 </li>              
#             </ul>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )



# # --- Image and Guide ---
# st.subheader("Body Coordinate System:")
# AXIS_GUIDE_URL = "assets/Axis_Guide_new.png"
# st.image(AXIS_GUIDE_URL, caption="3-axis X-Y-Z", use_column_width=True)

# st.write(
#     """
# This diagram shows how the X, Y, and Z axes are oriented 
# relative to the human body while seated in the amusement vehicle.  
# It is used as a guide when interpreting acceleration data 
# from the mounted sensors.  
# """
# )

# st.subheader(
#     "Acceleration is defined in accordance with the following coordinate system:"
# )
# st.markdown(
#     "+a<sub>z</sub> presses the body into the seat downwards, described as “eyes down”.<br>"
#     "−a<sub>z</sub> lifts the body out of the seat, described as “eyes up”.<br>"
#     "+a<sub>y</sub> presses the body sideward to the right, described as “eyes right”.<br>"
#     "−a<sub>y</sub> presses the body sideward to the left, described as “eyes left”.<br>"
#     "+a<sub>x</sub> presses the body into the seat backward, described as “eyes back”.<br>"
#     "−a<sub>x</sub> pushes the body out of the seat forward, described as “eyes front”.",
#     unsafe_allow_html=True,
# )

with tab2:
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
