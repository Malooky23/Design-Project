# pages/Generators.py
# 2_Creative_Name_Tools.py
import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import difflib
from typing import Dict, List, TypedDict

# Import the Google Gen AI SDK
from google import genai
# Assuming utils.py with load_data is in the project root
from utils import load_data


# =============================================================================
# PAGE CONFIGURATION & DATA LOADING
# =============================================================================
st.set_page_config(
    page_title="Creative Name Tools",
    page_icon="🎨",
    layout="wide"
)

st.title("Creative Name Tools")
st.markdown("A collection of tools to help you find, create, and analyze names.")


@st.cache_data
def load_name_data():
    """Loads the primary names dataframe for tools that need it."""
    df, _ = load_data()
    return df


# Load data needed for specific tabs
names_df = load_name_data()


# =============================================================================
# HELPER FUNCTIONS & CONSTANTS (from all merged files)
# =============================================================================

# --- From 4_name_meaning.py (AI Analysis) ---
@st.cache_data(show_spinner=False)
def get_name_analysis(name: str):
    """Calls the Gemini API to get a full analysis of a name."""
    api_key = st.secrets.get("GEMINI_API")
    if not api_key:
        st.error("GEMINI_API not found in Streamlit secrets.")
        return None
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        Analyze the name "{name}". Provide the following information in a single, valid JSON object.
        Your response must be ONLY the JSON object.
        The JSON object must have these exact keys:
        - "meaning": A concise definition of the name's meaning.
        - "origin": The primary cultural and/or linguistic origin(s).
        - "similar_names": An array of 4-6 names with a similar cultural origin or vibe.
        - "cultural_issues": An array of strings describing potential cross-cultural issues. If none, provide an empty array [].
        - "fun_facts": An array of 3-4 interesting trivia points or famous people. If none, provide an empty array [].

        Example for "Lucy":
        {{
            "meaning": "Light.",
            "origin": "Latin",
            "similar_names": ["Clara", "Stella", "Nora", "Ruby", "Hazel"],
            "cultural_issues": [],
            "fun_facts": ["Famous Lucy: Lucy from the Peanuts comic strip.", "Saint Lucy is the patron saint of the blind."]
        }}
        Now, provide the analysis for the name "{name}":
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=prompt)
        if not response.text:
            return None
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_response)
    except Exception as e:
        st.error(f"An error occurred connecting to the Gemini API: {e}")
        return None


# --- From 8_nickname_generator.py ---
NICKNAME_DATABASE = {"alexander": ["Alex", "Xander", "Lex"], "elizabeth": ["Liz", "Lizzy", "Beth", "Eliza"], "michael": ["Mike", "Mikey", "Mick"], "gabriella": ["Gabby", "Ella"], "christopher": ["Chris", "Topher"], "katherine": [
    "Kate", "Katie", "Kat"], "william": ["Will", "Liam", "Billy"], "benjamin": ["Ben", "Benny", "Benji"], "robert": ["Rob", "Bobby"], "margaret": ["Maggie", "Meg", "Margot"], "charlotte": ["Charlie", "Lottie"], "isabella": ["Bella", "Izzy"]}
STYLE_FILTERS = {"All styles": lambda n: True, "Classic": lambda n: len(n) >= 4 and not n.lower().endswith(
    ("y", "ie")), "Playful": lambda n: n.lower().endswith(("y", "ie", "o")), "Short & Sweet": lambda n: len(n) <= 4}


def _heuristic_variations(name: str) -> List[str]:
    base = name.strip()
    if not base:
        return []
    cands = set()
    if len(base) >= 3:
        cands.add((base[:3] + "y").capitalize())
        cands.add((base[:3] + "ie").capitalize())
    if len(base) >= 4:
        cands.add((base[:4]).capitalize())
    return sorted({nick for nick in cands if nick and nick.lower() != base.lower()})


def generate_nicknames(name: str, vibe: str) -> List[str]:
    if not name:
        return []
    norm = name.lower().strip()
    sugs = NICKNAME_DATABASE.get(norm, []) + _heuristic_variations(name)
    seen = set()
    unique_sugs = [s for s in sugs if s.lower(
    ) not in seen and not seen.add(s.lower())]
    filter_fn = STYLE_FILTERS.get(vibe, lambda n: True)
    return [nick for nick in unique_sugs if filter_fn(nick)]

# --- From 9_parent_name_blender.py ---


class Candidate(TypedDict):
    name: str
    gender: str
    tags: List[str]


CANDIDATE_NAMES: List[Candidate] = [{"name": "Aria", "gender": "F", "tags": ["Modern"]}, {"name": "Avery", "gender": "N", "tags": ["Modern"]}, {"name": "Amelia", "gender": "F", "tags": ["Classic"]}, {"name": "Bennett", "gender": "M", "tags": ["Classic"]}, {"name": "Caleb", "gender": "M", "tags": ["Biblical"]}, {"name": "Elara", "gender": "F", "tags": ["Celestial"]}, {"name": "Elias", "gender": "M", "tags": ["Biblical"]}, {"name": "Emilia", "gender": "F", "tags": ["Classic"]}, {"name": "Ezra", "gender": "M", "tags": ["Biblical"]}, {"name": "Julian", "gender": "M", "tags": [
    "Classic"]}, {"name": "Kai", "gender": "N", "tags": ["Nature"]}, {"name": "Levi", "gender": "M", "tags": ["Biblical"]}, {"name": "Luca", "gender": "N", "tags": ["Global"]}, {"name": "Milo", "gender": "M", "tags": ["Modern"]}, {"name": "Noah", "gender": "M", "tags": ["Biblical"]}, {"name": "Nova", "gender": "F", "tags": ["Celestial"]}, {"name": "Orion", "gender": "M", "tags": ["Celestial"]}, {"name": "Rowan", "gender": "N", "tags": ["Nature"]}, {"name": "Silas", "gender": "M", "tags": ["Biblical"]}, {"name": "Theo", "gender": "M", "tags": ["Classic"]}]
VIBE_OPTIONS = {"All vibes": lambda t: True, "Classic": lambda t: "Classic" in t,
                "Modern": lambda t: "Modern" in t, "Nature inspired": lambda t: "Nature" in t or "Celestial" in t}
GENDER_FILTERS = {"Any": lambda g: True, "Feminine": lambda g: g ==
                  "F", "Masculine": lambda g: g == "M", "Neutral": lambda g: g == "N"}


def _clean(name: str) -> str: return "".join(ch for ch in name.strip()
                                             if ch.isalpha()).lower()


def _blend_fragments(p1: str, p2: str) -> List[str]:
    c1, c2 = _clean(p1), _clean(p2)
    if not c1 or not c2:
        return []
    return sorted({(c1[:len(c1)//2] + c2[len(c2)//2:]).capitalize(), (c2[:len(c2)//2] + c1[len(c1)//2:]).capitalize()})


def _score_candidate(cand: str, parents: List[str]) -> float:
    c_cand, scores = _clean(cand), []
    for p in parents:
        c_p = _clean(p)
        if c_p:
            scores.append(difflib.SequenceMatcher(None, c_cand, c_p).ratio())
    return sum(scores) / len(scores) if scores else 0.0


def suggest_names(p1: str, p2: str, vibe: str, gender: str, limit: int) -> List[Dict]:
    vibe_fn, gender_fn = VIBE_OPTIONS.get(
        vibe, lambda t: True), GENDER_FILTERS.get(gender, lambda g: True)
    parents = [p1, p2]
    cands = [{"name": e["name"], "score": _score_candidate(e["name"], parents), "tags": ", ".join(
        e["tags"])} for e in CANDIDATE_NAMES if vibe_fn(e["tags"]) and gender_fn(e["gender"])]
    return sorted([c for c in cands if c["score"] > 0.4], key=lambda i: i["score"], reverse=True)[:limit]


# =============================================================================
# TABS FOR DIFFERENT TOOLS
# =============================================================================

tab_ai, tab_name_creation, tab_nick, tab_unique, tab_neutral = st.tabs([
    "AI Name Analysis",
    "Name Creation Tools",  # Renamed and combined tab
    "Nickname Generator",
    "Unique Letter Finder",
    "Gender-Neutral Finder",
])


# --- TAB 1: AI NAME ANALYSIS ---
with tab_ai:
    st.header("Name Meaning, Cultural Check & Fun Facts")
    st.markdown(
        "Explore the meaning, cultural context, and fun facts about names using Google Gemini AI.")
    if "GEMINI_API" not in st.secrets:
        st.error("Google API Key not found. Please add it to your Streamlit secrets (`.streamlit/secrets.toml`) to use this feature.")
    else:
        ai_name_query = st.text_input(
            "Enter a name to analyze with AI:", "Maria").strip()
        if ai_name_query:
            with st.spinner(f"Asking Gemini AI about '{ai_name_query}'..."):
                analysis = get_name_analysis(ai_name_query)
            if analysis:
                st.subheader(f"Analysis of '{ai_name_query}'")
                col1, col2 = st.columns(2)
                with col1:
                    if analysis.get("meaning"):
                        st.success(f"**Meaning:** {analysis['meaning']}")
                with col2:
                    if analysis.get("origin"):
                        st.info(f"**Origin:** {analysis['origin']}")
                st.divider()
                st.subheader("Culturally Similar Suggestions")
                if analysis.get("similar_names"):
                    st.write(", ".join(analysis["similar_names"]))
                st.divider()
                st.subheader("Cross-Cultural Name Check")
                if analysis.get("cultural_issues"):
                    for issue in analysis["cultural_issues"]:
                        st.warning(f"**Potential Issue:** {issue}")
                else:
                    st.success(
                        "No known negative connotations identified by the AI.")
                st.divider()
                st.subheader("Fun Facts")
                if analysis.get("fun_facts"):
                    for fact in analysis["fun_facts"]:
                        st.write(f"- {fact}")
                else:
                    st.info("No fun facts were generated for this name.")
            else:
                st.error(f"Could not retrieve analysis for '{ai_name_query}'.")

# --- TAB 2: NAME CREATION TOOLS (MERGED) ---
with tab_name_creation:
    st.header("Name Creation Tools")
    st.markdown("Combine names or blend parent names to inspire new ideas.")

    # Name Merger Section
    st.subheader("Creative Name Merger")
    st.markdown("Combine two names to create a unique new one.")
    col1, col2 = st.columns(2)
    with col1:
        name1 = st.text_input("First Name", "Maria", key="merger_name1")
    with col2:
        name2 = st.text_input("Second Name", "Lynn", key="merger_name2")
    if st.button("Merge Names", key="merge_button"):
        if name1 and name2:
            mid1, mid2 = len(name1) // 2, len(name2) // 2
            merged1 = (name1[:mid1] + name2[mid2:]).capitalize()
            merged2 = (name1 + name2).capitalize()
            st.success(f"Merged suggestions: **{merged1}**, **{merged2}**")
        else:
            st.warning("Please enter two names to merge.")

    st.divider()  # Separator between merger and blender

    # Parent Name Blender Section
    st.subheader("Parent Name Blender")
    st.markdown(
        "Blend two parent names and discover baby name ideas that feel like family.")
    with st.container(border=True):
        col_a, col_b = st.columns(2)
        with col_a:
            parent_one = st.text_input(
                "Parent one name", "Sophia", key="blender_parent1")
        with col_b:
            parent_two = st.text_input(
                "Parent two name", "Liam", key="blender_parent2")
        vibe_choice = st.selectbox("Preferred vibe", list(
            VIBE_OPTIONS.keys()), key="blender_vibe")
        gender_choice = st.selectbox(
            "Baby name style", list(GENDER_FILTERS.keys()), key="blender_gender")
    if st.button("Find family-fit names", use_container_width=True, key="blend_button"):
        blends = _blend_fragments(parent_one, parent_two)
        suggestions = suggest_names(
            parent_one, parent_two, vibe_choice, gender_choice, 6)
        if blends:
            st.subheader("Custom blends")
            st.write("• " + "  • ".join(f"**{b}**" for b in blends))
        if suggestions:
            st.subheader("Similar existing names")
            for item in suggestions:
                st.write(f"• **{item['name']}** — _{item['tags']}_")
        if not blends and not suggestions:
            st.warning(
                "Could not find any suggestions. Try different names or vibes.")

# --- TAB 3: NICKNAME GENERATOR ---
with tab_nick:
    st.header("Nickname Generator")
    st.markdown(
        "Create playful, classic, or short-and-sweet nicknames for any name.")
    with st.container(border=True):
        name_input = st.text_input("First name", "Alexander", key="nick_name")
        vibe_choice_nick = st.radio("Choose a nickname vibe", list(
            STYLE_FILTERS.keys()), horizontal=True)
        count = st.slider("Number of nicknames", 3, 10, 5)
    if st.button("Find nicknames", use_container_width=True):
        nicknames = generate_nicknames(name_input, vibe_choice_nick)
        if nicknames:
            st.subheader("Nickname ideas")
            st.write(" • ".join(f"**{n}**" for n in nicknames[:count]))
        else:
            st.warning("Try another name – we couldn't find any nicknames.")

# --- TAB 4: UNIQUE LETTER FINDER ---
with tab_unique:
    st.header("Unique Letter Finder")
    st.markdown(
        "Find names that are phonetically diverse by counting their unique letters.")
    unique_names = names_df["name"].unique()
    unique_letter_counts = {name: len(set(name.lower()))
                            for name in unique_names}
    sorted_names = sorted(unique_letter_counts.items(),
                          key=lambda item: item[1], reverse=True)
    unique_df = pd.DataFrame(sorted_names, columns=[
                             "Name", "Unique Letter Count"]).head(10)
    fig_unique = px.bar(
        unique_df, x="Name", y="Unique Letter Count", title="Top 10 Names by Unique Letter Count",
        color="Unique Letter Count", color_continuous_scale=px.colors.sequential.Viridis,
    )
    fig_unique.update_layout(xaxis={"categoryorder": "total descending"})
    st.plotly_chart(fig_unique, use_container_width=True)

# --- TAB 5: GENDER-NEUTRAL FINDER ---
with tab_neutral:
    st.header("Gender-Neutral Name Finder")
    st.markdown(
        "Discover names with a close to 50/50 gender split in our dataset. The list is sorted from most to least gender-neutral."
    )

    # Find names that appear for both Male and Female
    # considering only 'M' and 'F' for percentage calculation
    mf_names_df = names_df[names_df['gender'].isin(['M', 'F'])]
    name_gender_counts = mf_names_df.groupby('name')['gender'].nunique()
    neutral_name_list = name_gender_counts[name_gender_counts > 1].index

    if not neutral_name_list.empty:
        # Filter the df to only these names
        neutral_df = mf_names_df[mf_names_df['name'].isin(
            neutral_name_list)].copy()

        # Pivot to get M and F counts per name
        gender_pivot = neutral_df.pivot_table(
            index='name',
            columns='gender',
            values='count',
            aggfunc='sum',
            fill_value=0
        )

        # Calculate totals, percentages, and neutrality score
        gender_pivot['count'] = gender_pivot['M'] + gender_pivot['F']
        gender_pivot['female %'] = (
            gender_pivot['F'] / gender_pivot['count']) * 100
        gender_pivot['male %'] = (
            gender_pivot['M'] / gender_pivot['count']) * 100
        # The score is the distance from a perfect 50/50 split
        gender_pivot['neutrality_score'] = abs(gender_pivot['female %'] - 50)

        # Sort by the score (ascending)
        sorted_neutral_df = gender_pivot.sort_values(
            'neutrality_score', ascending=True)

        # Prepare final dataframe for display
        display_df = sorted_neutral_df[[
            'count', 'female %', 'male %'
        ]].reset_index()

        # Rename columns for clarity in the table
        display_df.rename(columns={
            'name': 'Name',
            'count': 'Total Count',
            'female %': 'Female %',
            'male %': 'Male %'
        }, inplace=True)

        # Reorder columns for display
        display_df = display_df[['Name', 'Total Count', 'Female %', 'Male %']]

        num_names_to_show = st.slider(
            "How many names to display?",
            min_value=10,
            max_value=len(display_df),
            value=50,
            step=10,
            key="neutral_names_slider"
        )

        st.dataframe(
            display_df.head(num_names_to_show),
            column_config={
                "Name": st.column_config.TextColumn("Name"),
                "Total Count": st.column_config.NumberColumn(
                    "Total Count",
                    format="%d"
                ),
                "Female %": st.column_config.ProgressColumn(
                    "Female %",
                    help="The percentage of times this name was recorded as female.",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
                "Male %": st.column_config.ProgressColumn(
                    "Male %",
                    help="The percentage of times this name was recorded as male.",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
            },
            use_container_width=True,
            hide_index=True
        )

    else:
        st.write(
            "No names with both Male and Female entries found in the dataset.")

