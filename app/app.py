"""
Serving as single page web app
powered by streamlit
"""

import os
from pathlib import Path
import sys
sys.path.append("..")

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

from rustoked import get_prediction

# make sure addresses are relatively set up
curr_location = Path(os.path.dirname(__file__))
icon_location = Path("photos/BreakTime.png")
foot_location = Path("photos/foot.png")

icon = Image.open(curr_location / icon_location)
st.image(icon)

st.title("R.U.Stoked?")
st.markdown("Write or paste some text (opinion) here an I tell you the content sentiment.")

comment = st.text_area("What do you reckon? ...")

# this part does the job. take input text and return the sentiment prediction
if st.button("Do Tell"):
    if comment:
        st.markdown("**`{}`**".format(get_prediction(comment)))
    else:
        st.markdown(" **-> IMPORTANT** : You need to provide some text input!")

st.write("----------")

st.markdown("""This is an experimental **NLP** (_Sentiment Detection_) project. The 
            model has been trained on a series of text data collected 
            from [SEEK](https://www.seek.com.au/) by which employees expressed their 
            opinion about employers and companies they have worked for. I focused on detecting a 
            middle class of employees that are neither `happy` nor `dissatisfied` which 
            I call them `Disengaged`""")
st.markdown("""I think it could be a good business case to detect those neutral contents 
            and create value in problem cases such as prospect customers or churn.""")
st.markdown("""**NOTE** : _This is an under development project and the currently deployed model 
            is not performing well on detecting the middle class discussed above._""")

st.write("----------")

st.markdown("Made by [Mohsen Saki](https://www.linkedin.com/in/mohsen-saki)")
st.markdown("More about the project [here]()")
st.markdown("Source code on [GitHub](https://github.com/mohsen-saki/RUStoked)")

st.write("----------")
st.write("Thanks to open source and free world ...")
foot = Image.open(curr_location / foot_location)
st.image(foot)