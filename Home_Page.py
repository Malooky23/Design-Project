import streamlit as st

from sidebar import create_sidebar


st.set_page_config(
    page_title="Global Name Explorer - Home",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# st.sidebar.success("Select a feature from the list to begin.")

st.title("Welcome to the Global Name Explorer!")
st.markdown(
    """
<div style='margin-bottom:0.05rem;'>
This application lets you explore the fascinating world of names.<br>
</div>
""",
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .marketing-img {
            width: 100%;
            object-fit: cover;
            margin-bottom: 0.02rem;
            border-radius: 0.2rem;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
            .marketing-img {
                width: 100% !important;
                height: auto !important;
                object-fit: contain;
                margin-bottom: 0.01rem;
                border-radius: 0.2rem;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
        html, body, [class*="css"]  {
            font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif !important;
        }
        .block-container {
            padding-top: 3.5rem !important;
            padding-bottom: 0 !important;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .stContainer, .st-cq, .st-cx, .st-cy, .st-cz, .st-da, .st-db {
            background: transparent !important;
        }
        /* Light theme */
        @media (prefers-color-scheme: light) {
            html, body, [class*="css"]  {
                background: #f8fafc !important;
                color: #181818 !important;
            }
            .stContainer[border="true"], .st-cq[border="true"] {
                background: #fff !important;
                box-shadow: 0 4px 24px 0 rgba(0,0,0,0.09);
            }
            h1, h2, h3, .stHeader, .stSubheader {
                color: #181818 !important;  # This line remains unchanged
                text-shadow: 0 1px 2px rgba(255,255,255,0.15);  # This line remains unchanged
                font-size: 0.6rem !important;
                margin-bottom: 0 !important;
            }
            .stTitle {
                font-size: 0.7rem !important;
                margin-bottom: 0 !important;
            }
            .stMarkdown, .stText, .stWrite, p {
                color: #22223b !important;  # This line remains unchanged
                font-size: 0.6rem !important;
                margin-bottom: 0 !important;
            }
            .stMarkdown, .stText, .stWrite, p {
                color: #22223b !important;
            }
            .stContainer[border="true"] .stSubheader, .st-cq[border="true"] .stSubheader {
                color: #ff6f61 !important;
            }
            .stButton > button {
                background: linear-gradient(90deg, #ff6f61 0%, #ffb347 100%) !important;
                color: #fff !important;
                text-shadow: 0 1px 2px rgba(0,0,0,0.15);
            }
            .stButton > button:hover {
                background: linear-gradient(90deg, #ffb347 0%, #ff6f61 100%) !important;
            }
        }
        /* Dark theme */
        @media (prefers-color-scheme: dark) {
            html, body, [class*="css"]  {
                background: #181a20 !important;
                color: #f8fafc !important;
            }
            .stContainer[border="true"], .st-cq[border="true"] {
                background: #23263a !important;
                box-shadow: 0 4px 24px 0 rgba(0,0,0,0.25);
            }
            h1, h2, h3, .stHeader, .stSubheader {
                color: #fff !important;
                text-shadow: 0 1px 2px rgba(0,0,0,0.25);
            }
            .stMarkdown, .stText, .stWrite, p {
                color: #e0e0e0 !important;
            }
            .stContainer[border="true"] .stSubheader, .st-cq[border="true"] .stSubheader {
                color: #ffb347 !important;
            }
            .stButton > button {
                background: linear-gradient(90deg, #ffb347 0%, #ff6f61 100%) !important;
                color: #181818 !important;
                text-shadow: 0 1px 2px rgba(255,255,255,0.15);
            }
            .stButton > button:hover {
                background: linear-gradient(90deg, #ff6f61 0%, #ffb347 100%) !important;
            }
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("<h2 style='font-size:1.1rem; margin-top:0.1rem; margin-bottom:0.5rem;'>Explore Our Features</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2,)


with col1:
    st.markdown(
        """
        <div style='width:320px; margin: 0 auto; text-align: center; margin-top: 0.3rem; border-radius: 1rem; padding: 0.5rem 1rem; box-sizing: border-box;'>
            <a href="http://localhost:8501/geo" target="_self" style="display:block;">
                <img src='https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80' style='width: 110%; max-width: 110%; display: block; border-radius: 0.2rem; margin-bottom: 0.01rem; margin-left: -5%;' alt='Geographical Explorer image'>
            </a>
    """,
        unsafe_allow_html=True,
    )
    st.subheader("Geographical Explorer")
    st.write("Our dashboard provides insights into names among people living in Sweden. Search one or multiple names to explore their geographic origins, gender distribution, and country-specific statistics through interactive maps, charts, and tables.")
    st.markdown("""
<div style='margin-top: 0.7rem;'></div>
""", unsafe_allow_html=True)
    if st.button("Go to Geographical Explorer", key="geo", use_container_width=True):
        # st.switch_page("pages/geo.py")
        st.switch_page("pages/Geographical_Explorer.py")
    st.markdown("""</div>""", unsafe_allow_html=True)


with col2:
    st.markdown(
        """
        <div style='width:320px; margin: 0 auto; text-align: center; margin-top: 0.3rem; border-radius: 1rem; padding: 0.5rem 1rem; box-sizing: border-box;'>
            <a href="http://localhost:8501/generators" target="_self" style="display:block;">
                <img src='https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80' style='width: 110%; max-width: 110%; display: block; border-radius: 0.2rem; margin-bottom: 0.01rem; margin-left: -5%;' alt='Generator image'>
            </a>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("Name Generator")
    st.write("This name generator dashboard helps you explore and discover names with ease. Search for any name to access similar alternatives, meanings, origins, nicknames, and unique facts.")
    # Use a wrapper div with a larger margin-top to align the right button with the left button, without affecting other elements
    st.markdown("""
<div style='width:100%; display:flex; justify-content:center;'>
    <div style='margin-top: calc(2.65rem); width:100%;'>
""", unsafe_allow_html=True)
    if st.button("Go to Name Meaning", key="meaning", use_container_width=True):
        st.switch_page("pages/Generators.py")
    st.markdown("""
  </div>
</div>
""", unsafe_allow_html=True)
    st.markdown("""</div>""", unsafe_allow_html=True)
