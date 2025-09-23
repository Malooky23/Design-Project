# sidebar.py
import streamlit as st


def create_sidebar():
    """
    Creates and populates the sidebar for the Global Name Explorer application.
    
    This function can be called from any page to ensure a consistent sidebar
    across the entire application.
    """
    with st.sidebar:
        st.title("🌍 Global Name Explorer")
        st.info(
            "Welcome! This app helps you explore names around the world. "
            "Select a feature from the list below to begin."
        )

        # Streamlit automatically creates page navigation from the 'pages' directory.
        # We can add other elements here for a consistent look and feel.

        st.success("Select a feature to get started.")

        st.markdown("---")
        st.caption("Created with ❤️ by [Your Name]")
        st.caption("Data source: Names for days")
