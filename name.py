import streamlit as st

st.set_page_config(
    page_title="Global Name Explorer - Home",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.success("Select a feature from the list to begin.")

st.title("🌍 Welcome to the Global Name Explorer!")
st.markdown(
    """
This demo application lets you explore the fascinating world of names.
Discover popularity hotspots, uncover meanings, and find unique names using the tools available.

**Select a feature from the sidebar on the left to get started!**
"""
)

st.header("Explore Our Features")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("🌍 Geographical Explorer")
        st.write("Search for names to see their popularity hotspots on a world map.")
        if st.button("Go to Geographical Explorer", key="geo", width='stretch'):
            st.switch_page("pages/1_geo_exp.py")

    with st.container(border=True):
        st.subheader("📖 Name Meaning")
        st.write("Find the meaning, origin, and cultural notes for any name.")
        if st.button("Go to Name Meaning", key="meaning", width='stretch'):
            st.switch_page("pages/4_name_meaning.py")

    with st.container(border=True):
        st.subheader("🔠 Unique Letter Finder")
        st.write("Find names with the most unique letters.")
        if st.button("Go to Unique Letter Finder", key="unique", width='stretch'):
            st.switch_page("pages/6_unique_letter.py")


with col2:
    with st.container(border=True):
        st.subheader("📈 Local Trends")
        st.write("Select a country to explore its top first and last names.")
        if st.button("Go to Local Trends", key="local", width='stretch'):
            st.switch_page("pages/2_local_trends.py")

    with st.container(border=True):
        st.subheader("✨ Name Merger")
        st.write("Creatively combine two names to generate a new, unique one.")
        if st.button("Go to Name Merger", key="merger", width='stretch'):
            st.switch_page("pages/5_name_merger.py")

    with st.container(border=True):
        st.subheader("🚻 Gender-Neutral Finder")
        st.write("Identify names used across different genders.")
        if st.button("Go to Gender-Neutral Finder", key="gender", width='stretch'):
            st.switch_page("pages/7_gender_neutral.py")


with col3:
    with st.container(border=True):
        st.subheader("🌐 Cross-Cultural Names")
        st.write("Discover names that are popular across multiple distinct cultures.")
        if st.button("Go to Cross-Cultural Names", key="cross", width='stretch'):
            st.switch_page("pages/3_cross_cult_names.py")
