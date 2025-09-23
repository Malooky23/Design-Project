from pages.utils import load_data
import plotly.express as px
import pandas as pd
import streamlit as st


# Load Data
names_df, _, _ = load_data()

st.set_page_config(page_title="Unique Letter Finder",
                   page_icon="🔠", layout="wide")

st.title("🔠 Unique Letter Finder")
st.markdown(
    "Find names that are phonetically diverse by counting their unique letters.")

unique_names = names_df["name"].unique()
unique_letter_counts = {name: len(set(name.lower())) for name in unique_names}
sorted_names = sorted(
    unique_letter_counts.items(), key=lambda item: item[1], reverse=True
)

unique_df = pd.DataFrame(
    sorted_names, columns=["Name", "Unique Letter Count"]
).head(10)
fig_unique = px.bar(
    unique_df,
    x="Name",
    y="Unique Letter Count",
    title="Top 10 Names by Unique Letter Count",
    color="Unique Letter Count",
    color_continuous_scale=px.colors.sequential.Viridis,
)
fig_unique.update_layout(xaxis={"categoryorder": "total descending"})
st.plotly_chart(fig_unique, width='stretch')
