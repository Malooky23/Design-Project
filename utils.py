import streamlit as st
import pandas as pd
from urllib.request import urlopen
import json
import os

PROCESSED_NAMES_PATH = 'data/processed_names.parquet'
PROCESSED_SURNAMES_PATH = 'data/processed_surnames.parquet'


@st.cache_data
def load_data():
    """
    Loads pre-processed data from efficient Parquet files.

    This function reads data that has been cleaned and transformed by the
    `preprocess_data.py` script. This is significantly faster than
    processing raw CSV files on app startup.

    If files are not found, it displays an error guiding the user to run
    the preprocessing script.

    Returns:
        tuple: (names_df, last_names_df)
    """
    # Check if the pre-processed files exist.
    if not os.path.exists(PROCESSED_NAMES_PATH) or not os.path.exists(PROCESSED_SURNAMES_PATH):
        st.error(
            "Error: Pre-processed data files not found. "
            "Please run the `preprocess_data.py` script first from your terminal: "
            "`python preprocess_data.py`"
        )
        # Return empty dataframes to prevent the app from crashing.
        return pd.DataFrame(), pd.DataFrame()

    # Load the pre-processed data from Parquet files. This is extremely fast.
    names_df = pd.read_parquet(PROCESSED_NAMES_PATH)
    last_names_df = pd.read_parquet(PROCESSED_SURNAMES_PATH)

    # The static meanings_df has been removed. This functionality is now handled
    # by a Gemini API call in the 'Name Meaning' page.

    return names_df, last_names_df


@st.cache_data
def get_geojson():
    """
    Retrieves GeoJSON data for world country boundaries.
    """
    url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
    with urlopen(url) as response:
        return json.load(response)