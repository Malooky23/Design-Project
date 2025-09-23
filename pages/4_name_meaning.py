# from pages.utils import load_data
# import streamlit as st


# # Load Data
# _, meanings_df, _ = load_data()

# st.set_page_config(page_title="Name Meaning", page_icon="📖", layout="wide")

# st.title("📝 Name Meaning & Cultural Check")
# st.markdown(
#     "Explore the meaning of names and check for potential cross-cultural issues.")

# name_tool_query = st.text_input("Enter a name to get started:", "Maria")

# if name_tool_query:
#     st.subheader(f"Meaning of '{name_tool_query}'")
#     meaning_info = meanings_df[
#         meanings_df["name"].str.lower() == name_tool_query.lower()
#     ]
#     if not meaning_info.empty:
#         st.success(f"**Meaning:** {meaning_info['meaning'].iloc[0]}")
#         st.info(f"**Origin:** {meaning_info['origin'].iloc[0]}")
#         origin = meaning_info["origin"].iloc[0]
#     else:
#         st.warning("Meaning not found in our database.")
#         origin = None

#     st.divider()

#     st.subheader("Culturally Similar Suggestions")
#     if origin:
#         similar_origin_names = meanings_df[meanings_df["origin"] == origin]
#         similar_origin_names = similar_origin_names[
#             similar_origin_names["name"].str.lower() != name_tool_query.lower()
#         ]
#         if not similar_origin_names.empty:
#             st.write(f"Other names with a **{origin}** origin:")
#             st.write(", ".join(similar_origin_names["name"].tolist()))
#         else:
#             st.write(f"No other names with a {origin} origin in the dataset.")
#     else:
#         st.write("Enter a name with a known origin to get suggestions.")

#     st.divider()

#     st.subheader("Cross-Cultural Name Check")
#     appropriateness_db = {
#         "nova": {
#             "Spanish": 'Means "doesn\'t go", which could be seen as negative for a car or product.'
#         },
#         "gary": {
#             "Japanese": 'Sounds similar to "geri" (下痢), which means "diarrhea".'
#         },
#     }

#     check_name = name_tool_query.lower()
#     if check_name in appropriateness_db:
#         for lang, note in appropriateness_db[check_name].items():
#             st.warning(f"**Potential Issue in {lang}:** {note}")
#     else:
#         st.success(
#             "No known negative connotations for this name in our (limited) database."
#         )

import streamlit as st
import json
import os

# Import the new Google Gen AI SDK
from google import genai

# Use a robust, modern model
MODEL_ID = "gemini-2.5-flash-lite"


@st.cache_data(show_spinner=False)
def get_name_analysis(name: str):
    """
    Calls the Gemini API (via google-genai SDK) to get the meaning, origin, 
    and cultural analysis of a name.
    """
    # Retrieve the API key from Streamlit secrets
    api_key = st.secrets.get("GEMINI_API")
    if not api_key:
        st.error("GEMINI_API not found in Streamlit secrets.")
        return None

    try:
        # Create the new client instance
        client = genai.Client(api_key=api_key)

        # The prompt explicitly requests a JSON object for reliable parsing.
        prompt = f"""
        Analyze the name "{name}". Provide the following information in a single, valid JSON object.

        Your response must be ONLY the JSON object, with no other text, comments, or markdown formatting.

        The JSON object must have these exact keys:
        - "meaning": A concise definition of the name's meaning.
        - "origin": The primary cultural and/or linguistic origin(s) (e.g., "Hebrew", "Latin", "Japanese").
        - "similar_names": An array of 4-6 names with a similar cultural origin or vibe.
        - "cultural_issues": An array of strings describing potential cross-cultural issues, negative connotations, or unfortunate meanings in other languages. If none are known, provide an empty array [].

        Example for "Lucy":
        {{
            "meaning": "Light.",
            "origin": "Latin",
            "similar_names": ["Clara", "Stella", "Nora", "Ruby", "Hazel"],
            "cultural_issues": []
        }}

        Now, provide the analysis for the name "{name}":
        """

        # Make the API call using the new client structure
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
        )

        # Check if the response was blocked (safety settings)
        if not response.text:
            print(
                f"Gemini API returned an empty response for '{name}'. Check safety filters.")
            return None

        # Clean the response in case of markdown wrapping (e.g., ```json ... ```)
        clean_response = response.text.strip().replace("```json", "").replace("```", "")

        return json.loads(clean_response)

    except json.JSONDecodeError:
        st.error(
            "Failed to parse the response from the AI. The format was unexpected.")
        print(f"JSON Parse Error for '{name}': {response.text}")
        return None
    except Exception as e:
        st.error(f"An error occurred connecting to the Gemini API.")
        print(f"Gemini API Error: {e}")
        return None


# =============================================================================
# Streamlit Page Logic
# =============================================================================

st.set_page_config(page_title="Name Meaning", page_icon="📖", layout="wide")

st.title("📝 Name Meaning & Cultural Check")
st.markdown(
    "Explore the meaning of names and check for potential cross-cultural issues using the latest Google Gemini AI."
)

# Check for API key availability
if "GEMINI_API" not in st.secrets:
    st.error("Google API Key not found. Please add it to your Streamlit secrets (`.streamlit/secrets.toml`) to use this feature.")
    st.code("""
    [secrets]
    GOOGLE_API_KEY = "your_api_key_here"
    """, language="toml")
    st.stop()

# User Input
name_tool_query = st.text_input("Enter a name to get started:", "Kai").strip()

if name_tool_query:
    with st.spinner(f"Asking Gemini AI about '{name_tool_query}'..."):
        analysis = get_name_analysis(name_tool_query)

    if analysis:
        # Display Meaning and Origin
        st.subheader(f"Analysis of '{name_tool_query}'")
        col1, col2 = st.columns(2)

        with col1:
            if analysis.get("meaning"):
                st.success(f"**Meaning:** {analysis['meaning']}")
            else:
                st.warning("Meaning not found.")

        with col2:
            if analysis.get("origin"):
                st.info(f"**Origin:** {analysis['origin']}")
            else:
                st.warning("Origin not found.")

        st.divider()

        # Display Similar Names
        st.subheader("Culturally Similar Suggestions")
        similar_names = analysis.get("similar_names")
        if similar_names and isinstance(similar_names, list):
            st.write(f"Other names with a similar feel or origin:")
            st.write(", ".join(similar_names))
        else:
            st.write("No similar name suggestions available.")

        st.divider()

        # Display Cross-Cultural Check
        st.subheader("Cross-Cultural Name Check")
        cultural_issues = analysis.get("cultural_issues")

        # We check if the list exists and is not empty.
        if cultural_issues:
            for issue in cultural_issues:
                st.warning(f"**Potential Issue:** {issue}")
        else:
            st.success(
                "No known negative connotations or cross-cultural issues identified by the AI.")
    else:
        st.error(
            f"Could not retrieve analysis for '{name_tool_query}'. It might be an uncommon name, or the AI might have filtered the request."
        )
