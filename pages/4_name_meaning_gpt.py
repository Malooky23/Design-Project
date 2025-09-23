import streamlit as st
import json
from openai import OpenAI
import os


@st.cache_data(show_spinner=False)
def get_name_analysis(name: str):
    """
    Calls the OpenAI Responses API (GPT-5-nano) to get the meaning, origin,
    and cultural analysis of a name. Returns a dict with the expected keys
    or None on error.
    """
    # Retrieve the API key from Streamlit secrets
    api_key = st.secrets.get("OPENAI_API")
    if not api_key:
        st.error("OPENAI_API not found in Streamlit secrets.")
        return None

    try:
        # Create the OpenAI client
        client = OpenAI(api_key=api_key)

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

        # Call OpenAI Responses API (GPT-5-nano)
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt,
        )

        # Try to extract text from the response. New SDKs may provide output_text.
        text = None
        # Preferred: output_text if available
        if hasattr(response, "output_text") and response.output_text:
            text = response.output_text
        else:
            # Fallback to structured output extraction
            try:
                # response.output is typically a list of items with 'content'
                parts = []
                for item in getattr(response, "output", []) or []:
                    for c in item.get("content", []) if isinstance(item, dict) else []:
                        # content pieces may be dicts with 'text' or strings
                        if isinstance(c, dict) and c.get("type") == "output_text":
                            parts.append(c.get("text", ""))
                        elif isinstance(c, dict) and "text" in c:
                            parts.append(c.get("text", ""))
                        elif isinstance(c, str):
                            parts.append(c)
                text = "\n".join(parts).strip() if parts else None
            except Exception:
                text = None

        if not text:
            st.error("OpenAI returned an empty response. Check your API key and model availability.")
            return None

        # Clean the response in case of markdown wrapping (e.g., ```json ... ```)
        clean_response = text.strip().replace("```json", "").replace("```", "")

        return json.loads(clean_response)

    except json.JSONDecodeError:
        st.error("Failed to parse the response from the AI. The format was unexpected.")
        try:
            # Attempt to show any available raw text/response for debugging
            raw = locals().get("text") or locals().get("clean_response") or locals().get("response")
            st.text_area("Raw AI response", value=str(raw), height=200)
        except Exception:
            pass
        return None
    except Exception as e:
        st.error(f"An error occurred connecting to the OpenAI API: {e}")
        print(f"OpenAI API Error: {e}")
        return None
# =============================================================================
# Streamlit Page Logic
# =============================================================================

st.set_page_config(page_title="Name Meaning", page_icon="📖", layout="wide")

st.title("📝 Name Meaning & Cultural Check")
st.markdown(
    "Explore the meaning of names and check for potential cross-cultural issues using OpenAI (GPT-5-nano)."
)

# Check for API key availability
if "OPENAI_API" not in st.secrets:
    st.error("OpenAI API key not found. Please add it to your Streamlit secrets (`.streamlit/secrets.toml`) as OPENAI_API to use this feature.")
    st.code("""
    [secrets]
    OPENAI_API = "your_api_key_here"
    """, language="toml")
    st.stop()

# User Input
name_tool_query = st.text_input("Enter a name to get started:", "Kai").strip()

if name_tool_query:
    with st.spinner(f"Asking GPT-5-nano about '{name_tool_query}'..."):
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

