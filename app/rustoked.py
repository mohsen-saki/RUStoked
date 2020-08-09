import os
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st


# make sure objects addresses are "relatively" set up
current_path = Path(os.path.dirname(__file__))
model_path = Path("../models/model_v1.pkl")
vectorizer_path = Path("../models/vectorizer_v1.pkl")

# Loading pre-trained instance of TfidfVectorizer
VECTORIZER = joblib.load(current_path / vectorizer_path)
# Loading pre-trained instance of RandomForestClassifier
MODEL = joblib.load(current_path / model_path)

# cache main function for faster performance
# see https://docs.streamlit.io/en/stable/caching.html
@st.cache(suppress_st_warning=True)
def get_prediction(text):
    """
    get an array of text as input (review / comment)
    and make a prediction of its sentment
    :param text: an array of string/text
    :return: returns the sentiment mapped to predicted label
    """

    # sentimnts to be mapped to predicted label
    sentiment = ["Dissatisfied", "Disengaged", "Stoked"]

    df = pd.DataFrame([text], columns=["comment"])
    vectors = VECTORIZER.transform(df["comment"])

    return sentiment[MODEL.predict(vectors)[0]]