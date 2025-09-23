from pages.utils import load_data
import streamlit as st


# Load Data
names_df, _, _ = load_data()

st.set_page_config(page_title="Cross-Cultural Names",
                   page_icon="🌐", layout="wide")

st.title("🌐 Names Spanning Multiple Cultures")
st.markdown(
    "Discover names that are common in distinct regions, suggesting historical connections."
)

widespread_names = (
    names_df.groupby("name")["country"].nunique().sort_values(ascending=False)
)
widespread_names_df = widespread_names.reset_index().rename(
    columns={"country": "country_count"}
)

st.write("Top geographically widespread names in the dataset:")
st.dataframe(
    widespread_names_df,
    width='stretch',
    column_config={
        "name": "Name",
        "country_count": st.column_config.ProgressColumn(
            "Number of Countries",
            format="%f",
            min_value=0,
            max_value=int(widespread_names_df["country_count"].max()),
        ),
    },
    hide_index=True,
)
