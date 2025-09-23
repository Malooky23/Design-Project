import streamlit as st


st.set_page_config(page_title="Name Merger", page_icon="✨", layout="wide")

st.title("✨ Creative Name Merger")
st.markdown("Combine two names to create a unique new one.")
col1, col2 = st.columns(2)
with col1:
    name1 = st.text_input("First Name", "Maria")
with col2:
    name2 = st.text_input("Second Name", "Lynn")

if st.button("Merge Names"):
    if name1 and name2:
        midpoint1 = len(name1) // 2
        midpoint2 = len(name2) // 2
        merged_name1 = name1[:midpoint1] + name2[midpoint2:]
        merged_name2 = name1 + name2
        st.success(
            f"Merged suggestions: **{merged_name1.capitalize()}**, **{merged_name2.capitalize()}**"
        )
    else:
        st.warning("Please enter two names to merge.")
