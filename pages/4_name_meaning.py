from pages.utils import load_data
import streamlit as st


# Load Data
_, meanings_df, _ = load_data()

st.set_page_config(page_title="Name Meaning", page_icon="📖", layout="wide")

st.title("📝 Name Meaning & Cultural Check")
st.markdown(
    "Explore the meaning of names and check for potential cross-cultural issues.")

name_tool_query = st.text_input("Enter a name to get started:", "Maria")

if name_tool_query:
    st.subheader(f"Meaning of '{name_tool_query}'")
    meaning_info = meanings_df[
        meanings_df["name"].str.lower() == name_tool_query.lower()
    ]
    if not meaning_info.empty:
        st.success(f"**Meaning:** {meaning_info['meaning'].iloc[0]}")
        st.info(f"**Origin:** {meaning_info['origin'].iloc[0]}")
        origin = meaning_info["origin"].iloc[0]
    else:
        st.warning("Meaning not found in our database.")
        origin = None

    st.divider()

    st.subheader("Culturally Similar Suggestions")
    if origin:
        similar_origin_names = meanings_df[meanings_df["origin"] == origin]
        similar_origin_names = similar_origin_names[
            similar_origin_names["name"].str.lower() != name_tool_query.lower()
        ]
        if not similar_origin_names.empty:
            st.write(f"Other names with a **{origin}** origin:")
            st.write(", ".join(similar_origin_names["name"].tolist()))
        else:
            st.write(f"No other names with a {origin} origin in the dataset.")
    else:
        st.write("Enter a name with a known origin to get suggestions.")

    st.divider()

    st.subheader("Cross-Cultural Name Check")
    appropriateness_db = {
        "nova": {
            "Spanish": 'Means "doesn\'t go", which could be seen as negative for a car or product.'
        },
        "gary": {
            "Japanese": 'Sounds similar to "geri" (下痢), which means "diarrhea".'
        },
    }

    check_name = name_tool_query.lower()
    if check_name in appropriateness_db:
        for lang, note in appropriateness_db[check_name].items():
            st.warning(f"**Potential Issue in {lang}:** {note}")
    else:
        st.success(
            "No known negative connotations for this name in our (limited) database."
        )
