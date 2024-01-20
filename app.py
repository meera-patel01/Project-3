import numpy as np
import pandas as pd
import datetime as dt
import streamlit as st
from PIL import Image

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, text
from sqlalchemy import create_engine, text, inspect, func


im = Image.open("travel-image.png")
st.set_page_config(page_title="Travel Check-Ins App", page_icon=im, layout="wide")

#UNCOMMENT BEFORE SUBMITTING
#hide_default_format = """
#       <style>
       #MainMenu {visibility: hidden; }
#       footer {visibility: hidden;}
#       </style>
#       """
#st.markdown(hide_default_format, unsafe_allow_html=True)

option = st.selectbox("State You're Visiting", ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
                                        'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
                                        'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                                        'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
                                        'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                                        'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                                        'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                                        'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
                                        'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
                                        'Virginia',  'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
                                        'Washington D.C.'])


left, right = st.columns([1, 5])
with left:
    st.radio('Visual', options=['Temperature', 'Crime', 'Map'])
with right:
    data = {"letter": ['A', 'B'], "number": [1, 2]}
    data = pd.DataFrame(data)
    data = data.set_index('letter')
    st.title("Travel Check-Ins")
    st.bar_chart(data)