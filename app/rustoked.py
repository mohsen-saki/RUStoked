import os
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

current_path = Path(os.path.dirname(__file__))

model_path = Path("../models/model_v1.pkl")
vectorizer_path = Path("../models/vectorizer_v1.pkl")

VECTORIZER = joblib.load(current_path / vectorizer_path)
MODEL = joblib.load(current_path / model_path)

@st.cache(suppress_st_warning=True)
def get_prediction(text):
    sentiment = ["Dissatisfied", "Disengaged", "Stoked"]
    df = pd.DataFrame([text], columns=["comment"])
    vectors = VECTORIZER.transform(df["comment"])

    return sentiment[MODEL.predict(vectors)[0]]