import streamlit as st

from sidebar import create_sidebar


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
create_sidebar()
st.header("Explore Our Features")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("🌍 Geographical Explorer")
        st.write("Search for names to see their popularity hotspots on a world map.")
        if st.button("Go to Geographical Explorer", key="geo", width='stretch'):
            st.switch_page("pages/geo.py")

with col2:

    with st.container(border=True):
        st.subheader("📖 Generatorrrrrr")
        st.write("Find the meaning, origin, and cultural notes for any name.")
        if st.button("Go to Name Meaning", key="meaning", width='stretch'):
            st.switch_page("pages/generators.py")
