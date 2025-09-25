# pages/Generators.py
# 2_Creative_Name_Tools.py
import streamlit as st
import os
import pandas as pd
import plotly.express as px
import difflib
from typing import Dict, List, TypedDict

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

tab_name_creation, tab_nick = st.tabs([
    "Name Creation Tools",
    "Nickname Generator",
])


# --- TAB 1: NAME CREATION TOOLS (MERGED) ---
with tab_name_creation:
    st.header("Name Creation Tools")
    st.markdown("Combine names or blend parent names to inspire new ideas.")

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

# --- TAB 2: NICKNAME GENERATOR ---
with tab_nick:
    st.header("Nickname Generator")
    st.markdown(
        "Create playful, classic, or short-and-sweet nicknames for any name.")
    with st.container(border=True):
        name_input = st.text_input("First name", "Alexander", key="nick_name")
        vibe_choice_nick = st.radio("Choose a nickname vibe", list(
            STYLE_FILTERS.keys()), horizontal=True)
    if st.button("Find nicknames", use_container_width=True):
        nicknames = generate_nicknames(name_input, vibe_choice_nick)
        if nicknames:
            st.subheader("Nickname ideas")
            st.write(" • ".join(f"**{n}**" for n in nicknames[:3]))
        else:
            st.warning("Try another name – we couldn't find any nicknames.")
