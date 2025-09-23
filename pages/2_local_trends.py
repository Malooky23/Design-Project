from pages.utils import load_data
import plotly.express as px
import streamlit as st


# Load Data
names_df, _, last_names_df = load_data()

st.set_page_config(page_title="Local Naming Trends",
                   page_icon="📈", layout="wide")

st.title("📈 Discover Local Naming Trends")
country_list = [""] + sorted(names_df["country"].unique())
selected_country = st.selectbox("Select a country to explore:", country_list)

if selected_country:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Most Common First Names in {selected_country}")
        country_first_names = names_df[
            names_df["country"] == selected_country
        ].nlargest(5, "count")
        if not country_first_names.empty:
            fig_bar = px.bar(
                country_first_names,
                x="name",
                y="count",
                color="gender",
                title=f"Top 5 First Names in {selected_country}",
                labels={"count": "Number of Individuals", "name": "Name"},
                color_discrete_map={"F": "lightpink",
                                    "M": "lightblue", "U": "lightgray"},
            )
            st.plotly_chart(fig_bar, width='stretch')
        else:
            st.write("No first name data available for this country.")

    with col2:
        st.subheader(f"Most Common Last Names in {selected_country}")
        country_last_names = last_names_df[
            last_names_df["country"] == selected_country
        ]
        if not country_last_names.empty:
            st.table(country_last_names[["rank", "lastname"]])
        else:
            st.write("No last name data available for this country.")
else:
    st.info("Please select a country from the dropdown menu above to see local trends.")
