# import streamlit as st
# import pandas as pd
# from urllib.request import urlopen
# import json

# # Mappings to process the data from CSV files
# from pages.country_mappings import SWEDISH_TO_ENGLISH_COUNTRIES, COUNTRY_COORDS


# @st.cache_data
# def load_data():
#     """
#     Loads and processes men, women, and surname data from CSV files.
    
#     This function handles the complete data loading pipeline:
#     1. Processes men's names (from men.csv) with gender='M'
#     2. Processes women's names (from women.csv) with gender='F' 
#     3. Combines first names data and adds geographical coordinates
#     4. Processes surname data separately with ranking by country
#     5. Creates mock data for name meanings (placeholder for future enhancement)
    
#     Returns:
#         tuple: (names_df, meanings_df, last_names_df)
#         - names_df: DataFrame with columns [name, gender, country, count, lat, lon]
#         - meanings_df: DataFrame with name meanings and origins
#         - last_names_df: DataFrame with surname rankings by country
    
#     Data Processing Notes:
#     - Swedish country names are translated to English using SWEDISH_TO_ENGLISH_COUNTRIES
#     - Geographic coordinates are added using COUNTRY_COORDS mapping
#     - Invalid/unmappable countries are filtered out
#     - The 'Total' column from CSV files is excluded to prevent double counting
#     """

#     def process_file(file_path, name_col, gender=None):
#         """
#         Helper function to read and process a single CSV file.
        
#         Args:
#             file_path (str): Path to the CSV file to process
#             name_col (str): Name for the column containing names (first column)
#             gender (str, optional): Gender identifier ('M' or 'F') to add to the data
            
#         Returns:
#             pd.DataFrame: Processed dataframe in long format with columns:
#                           [name/lastname, country, count, gender (if specified)]
        
#         The function:
#         1. Reads the CSV file with UTF-8 encoding
#         2. Standardizes column names (first col = name, second col = Total)
#         3. Melts from wide to long format, excluding the Total column
#         4. Cleans count data (removes commas, converts to numeric)
#         5. Aggregates data to prevent double-counting from duplicate source columns
#         6. Filters out zero/invalid counts
#         7. Adds gender information if specified
#         """
#         try:
#             df = pd.read_csv(file_path, encoding='utf-8-sig' ,low_memory=False)
#         except FileNotFoundError:
#             st.error(
#                 f"File not found: {file_path}. Please make sure the file exists in the correct directory.")
#             return pd.DataFrame()

#         # Standardize column names
#         df = df.rename(columns={
#             df.columns[0]: name_col,
#             df.columns[1]: 'Total'
#         })

#         df.columns = df.columns.str.replace('\n', ' ')

#         id_vars = [name_col, 'Total']
#         country_cols = [col for col in df.columns if col not in id_vars]

#         df_long = df.melt(id_vars=id_vars, value_vars=country_cols,
#                           var_name='country', value_name='count')

#         df_long = df_long.drop(columns=['Total'], errors='ignore')

#         df_long['count'] = df_long['count'].astype(
#             str).str.replace(',', '', regex=False)
#         df_long['count'] = pd.to_numeric(df_long['count'], errors='coerce')
#         df_long = df_long.dropna(subset=['count'])
#         df_long['count'] = df_long['count'].astype(int)

#         df_long = df_long[df_long['count'] > 0]

#         # Add gender and aggregate to fix potential double-counting from source data
#         if gender:
#             df_long['gender'] = gender
#             # This groupby sums counts if the source CSV had duplicate country columns,
#             # which is the likely cause of the "double totals" issue.
#             group_cols = [name_col, 'gender', 'country']
#             df_long = df_long.groupby(
#                 group_cols, as_index=False)['count'].sum()
#         else:  # For surnames
#             group_cols = [name_col, 'country']
#             df_long = df_long.groupby(
#                 group_cols, as_index=False)['count'].sum()

#         return df_long

#     # =============================================================================
#     # PROCESS FIRST NAMES DATA
#     # =============================================================================
#     men_df = process_file('data/men1.csv', 'name', gender='M')
#     women_df = process_file('data/women1.csv', 'name', gender='F')
#     names_df = pd.concat([men_df, women_df], ignore_index=True)

#     # =============================================================================
#     # ADD GEOGRAPHICAL INFORMATION
#     # =============================================================================
#     names_df['country'] = names_df['country'].map(SWEDISH_TO_ENGLISH_COUNTRIES)
#     names_df = names_df.dropna(subset=['country'])

#     coords = names_df['country'].map(COUNTRY_COORDS)
#     names_df['lat'] = coords.apply(
#         lambda x: x[0] if isinstance(x, tuple) else None)
#     names_df['lon'] = coords.apply(
#         lambda x: x[1] if isinstance(x, tuple) else None)
#     names_df = names_df.dropna(subset=['lat', 'lon'])

#     names_df = names_df[['name', 'gender', 'country', 'count', 'lat', 'lon']]

#     # =============================================================================
#     # PROCESS SURNAMES DATA
#     # =============================================================================
#     surnames_df = process_file('data/surname1.csv', 'lastname')
#     if not surnames_df.empty:
#         surnames_df['country'] = surnames_df['country'].map(
#             SWEDISH_TO_ENGLISH_COUNTRIES)
#         surnames_df = surnames_df.dropna(subset=['country'])

#         surnames_df['rank'] = surnames_df.groupby('country')['count'].rank(
#             method='dense', ascending=False).astype(int)
#         last_names_df = surnames_df[['country', 'rank', 'lastname']].sort_values(by=[
#                                                                                  'country', 'rank'])
#     else:
#         last_names_df = pd.DataFrame(columns=['country', 'rank', 'lastname'])

#     # =============================================================================
#     # NAME MEANINGS DATA (PLACEHOLDER)
#     # =============================================================================
#     meanings_data = {
#         "name": ["Sophia", "Liam", "Maria", "Mohammed", "John", "Yuki", "Chen", "Alex", "Arvid"],
#         "meaning": [
#             "Wisdom", "Strong-willed warrior", "Of the sea, bitter, or beloved",
#             "Praiseworthy", "God is gracious", "Snow, happiness", "Morning",
#             "Defender of the people", "Ancient tree"
#         ],
#         "origin": ["Greek", "Irish", "Hebrew", "Arabic", "Hebrew", "Japanese", "Chinese", "Greek", "Swedish"],
#     }
#     meanings_df = pd.DataFrame(meanings_data)

#     return names_df, meanings_df, last_names_df


# @st.cache_data
# def get_geojson():
#     """
#     Retrieves GeoJSON data for world country boundaries.
#     """
#     url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
#     with urlopen(url) as response:
#         return json.load(response)


# pages/utils.py
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
        tuple: (names_df, meanings_df, last_names_df)
    """
    # Check if the pre-processed files exist.
    if not os.path.exists(PROCESSED_NAMES_PATH) or not os.path.exists(PROCESSED_SURNAMES_PATH):
        st.error(
            "Error: Pre-processed data files not found. "
            "Please run the `preprocess_data.py` script first from your terminal: "
            "`python preprocess_data.py`"
        )
        # Return empty dataframes to prevent the app from crashing.
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Load the pre-processed data from Parquet files. This is extremely fast.
    names_df = pd.read_parquet(PROCESSED_NAMES_PATH)
    last_names_df = pd.read_parquet(PROCESSED_SURNAMES_PATH)

    # Placeholder for meanings data remains the same
    meanings_data = {
        "name": ["Sophia", "Liam", "Maria", "Mohammed", "John", "Yuki", "Chen", "Alex", "Arvid"],
        "meaning": [
            "Wisdom", "Strong-willed warrior", "Of the sea, bitter, or beloved",
            "Praiseworthy", "God is gracious", "Snow, happiness", "Morning",
            "Defender of the people", "Ancient tree"
        ],
        "origin": ["Greek", "Irish", "Hebrew", "Arabic", "Hebrew", "Japanese", "Chinese", "Greek", "Swedish"],
    }
    meanings_df = pd.DataFrame(meanings_data)

    return names_df, meanings_df, last_names_df


@st.cache_data
def get_geojson():
    """
    Retrieves GeoJSON data for world country boundaries.
    """
    url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
    with urlopen(url) as response:
        return json.load(response)
