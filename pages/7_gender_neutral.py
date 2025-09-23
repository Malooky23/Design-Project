from pages.utils import load_data
import plotly.express as px
import pandas as pd
import streamlit as st


# Load Data
names_df, _= load_data()

st.set_page_config(page_title="Gender-Neutral Finder",
                   page_icon="🚻", layout="wide")

st.title("🚻 Gender-Neutral Name Finder")
st.markdown("Discover names that are used for multiple genders in our dataset.")

gender_counts = names_df.groupby("name")["gender"].nunique()
unisex_names = names_df[names_df["gender"] == "U"]["name"].unique()
neutral_names_list = gender_counts[gender_counts > 1].index.tolist()

combined_neutral_names = sorted(
    list(set(neutral_names_list + list(unisex_names))))

if combined_neutral_names:
    neutral_df = names_df[names_df["name"].isin(combined_neutral_names)]

    gender_distribution = (
        neutral_df.groupby(["name", "gender"], observed=True)["count"].sum().reset_index()
    )

    fig_gender_neutral = px.bar(
        gender_distribution,
        x="name",
        y="count",
        color="gender",
        title="Gender Distribution of Neutral Names",
        labels={"count": "Total Count", "name": "Name", "gender": "Gender"},
        barmode="stack",
        color_discrete_map={"F": "lightpink",
                            "M": "lightblue", "U": "lightgray"},
    )
    st.plotly_chart(fig_gender_neutral, width='stretch')

    with st.expander("View Raw Data for Gender-Neutral Names"):
        st.dataframe(
            neutral_df[["name", "gender", "country", "count"]
                       ].sort_values(by="name"),
            width='stretch',
        )

else:
    st.write("No gender-neutral names found in the dataset.")
