# 1_Name_Explorer.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import colorsys
from google import genai
from utils import load_data, get_geojson

# =============================================================================
# PAGE CONFIGURATION & DATA LOADING
# =============================================================================

st.set_page_config(
    page_title="Global Name Explorer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("✨ Global Name Explorer")
st.markdown(
    "Your all-in-one toolkit for exploring names. Discover geographical hotspots, local trends, cross-cultural connections, and AI-powered name analysis."
)

# Load all necessary data once using caching for performance


@st.cache_data
def load_all_data():
    names_df, last_names_df = load_data()
    geojson_data = get_geojson()
    return names_df, last_names_df, geojson_data


names_df, last_names_df, geojson = load_all_data()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def lighten_hex_color(hex_color, factor=0.5):
    """Lightens a hex color by a given factor."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
    l = min(1.0, l + (1.0 - l) * factor)
    r, g, b = (int(x*255) for x in colorsys.hls_to_rgb(h, l, s))
    return f'#{r:02x}{g:02x}{b:02x}'


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
        Your response must be ONLY the JSON object, with no other text, comments, or markdown formatting.
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
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        if not response.text:
            return None
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_response)
    except Exception as e:
        st.error(f"An error occurred connecting to the Gemini API.")
        print(f"Gemini API Error: {e}")
        return None

# =============================================================================
# TABS FOR DIFFERENT FUNCTIONALITIES
# =============================================================================


tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Geographical Explorer",
    "📈 Local Trends",
    "🌐 Cross-Cultural Names",
    "📖 Name Meaning & AI Analysis"
])


# =============================================================================
# TAB 1: GEOGRAPHICAL NAME EXPLORATION
# =============================================================================
with tab1:
    st.header("🗺️ Geographical Name Exploration")
    st.markdown(
        "Search for one or more names to see its popularity hotspots on the map. "
        "This tool visualizes name distribution patterns across countries."
    )
    name_query = st.text_input(
        "Search for names, comma-separated (e.g., Maria, Mohammed, Alex):",
        "",
        help="Enter one or more names to see their global distribution."
    )

    if name_query:
        name_queries = [name.strip()
                        for name in name_query.split(",") if name.strip()]
        lower_case_names = [name.lower() for name in name_queries]
        search_data = names_df[names_df["name"].str.lower().isin(
            lower_case_names)]

        if search_data.empty:
            st.warning(
                f"No data found for the names '{name_query}'. Please try another name.")
        else:
            capitalized_names_found = sorted(
                [name.capitalize() for name in search_data["name"].str.lower().unique()])
            st.subheader(
                f"Popularity Hotspots for: {', '.join(capitalized_names_found)}")

            country_name_counts = search_data.groupby(["country", "name"], observed=True)[
                "count"].sum().reset_index()
            dominant_name_df = country_name_counts.loc[country_name_counts.groupby(
                "country", observed=True)["count"].idxmax()].copy()

            country_name_map = {"USA": "United States of America",
                                "UK": "United Kingdom", "Russia": "Russian Federation"}
            dominant_name_df["geojson_name"] = dominant_name_df["country"].replace(
                country_name_map)

            unique_names_found = sorted(
                list(dominant_name_df["name"].str.lower().unique()))
            colors = px.colors.qualitative.Plotly
            name_color_map = {name: colors[i % len(
                colors)] for i, name in enumerate(unique_names_found)}

            fig_map = go.Figure()
            num_names = len(unique_names_found)
            colorbar_len = (0.8 - (num_names - 1) * 0.05) / \
                num_names if num_names > 0 else 0

            for i, name_lower in enumerate(unique_names_found):
                name_capitalized = name_lower.capitalize()
                dominant_countries_for_name = dominant_name_df[dominant_name_df["name"].str.lower(
                ) == name_lower]
                if dominant_countries_for_name.empty:
                    continue

                base_color_hex = name_color_map[name_lower]
                color_scale = [[0.0, lighten_hex_color(base_color_hex, 0.7)], [
                    0.5, lighten_hex_color(base_color_hex, 0.3)], [1.0, base_color_hex]]
                y_pos = 0.9 - i * (colorbar_len + 0.05)

                fig_map.add_trace(go.Choroplethmap(
                    geojson=geojson,
                    locations=dominant_countries_for_name["geojson_name"],
                    z=dominant_countries_for_name["count"],
                    featureidkey="properties.name",
                    colorscale=color_scale,
                    colorbar=dict(title=f"{name_capitalized}<br>Count", x=1.02,
                                  xanchor="left", len=colorbar_len, y=y_pos, yanchor="top"),
                    marker_opacity=0.8, marker_line_width=0,
                    hovertemplate=f"<b>Country:</b> %{{location}}<br><b>Dominant Name:</b> {name_capitalized}<br><b>Count:</b> %{{z}}<extra></extra>"
                ))

            fig_map.update_layout(
                mapbox_style="carto-positron", mapbox_zoom=1, mapbox_center={"lat": 25, "lon": 20},
                margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False
            )
            st.plotly_chart(fig_map, use_container_width=True)
            st.divider()

            st.subheader("Insights for Searched Names")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### Gender Distribution")
                gender_dist = search_data.groupby(
                    "gender")["count"].sum().reset_index()
                if not gender_dist.empty:
                    fig_pie = px.pie(gender_dist, values="count", names="gender", title="Gender Mix Across All Countries",
                                     color_discrete_map={"F": "lightpink", "M": "lightblue", "U": "lightgray"})
                    fig_pie.update_traces(
                        textposition="inside", textinfo="percent+label")
                    st.plotly_chart(fig_pie, use_container_width=True)
            with col2:
                st.markdown("##### Top Countries by Count")
                total_counts_by_country = search_data.groupby(
                    "country")["count"].sum().sort_values(ascending=False).reset_index()
                if not total_counts_by_country.empty:
                    fig_bar = px.bar(total_counts_by_country.head(10).sort_values(by="count", ascending=True),
                                     y="country", x="count", orientation='h', title="Top 10 Countries by Total Name Count")
                    st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info(
            "👆 Enter a name in the search box above to populate the map and analytics.")


# =============================================================================
# TAB 2: LOCAL NAMING TRENDS
# =============================================================================
with tab2:
    st.header("📈 Discover Local Naming Trends")
    st.markdown(
        "Select a country to explore its most common first and last names.")
    country_list = [""] + sorted(names_df["country"].unique())
    selected_country = st.selectbox(
        "Select a country to explore:", country_list, key="local_trends_country")

    if selected_country:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Most Common First Names in {selected_country}")
            country_first_names = names_df[names_df["country"] == selected_country].nlargest(
                5, "count")
            if not country_first_names.empty:
                fig_bar_local = px.bar(
                    country_first_names, x="name", y="count", color="gender",
                    title=f"Top 5 First Names in {selected_country}",
                    labels={"count": "Number of Individuals", "name": "Name"},
                    color_discrete_map={"F": "lightpink",
                                        "M": "lightblue", "U": "lightgray"}
                )
                st.plotly_chart(fig_bar_local, use_container_width=True)
            else:
                st.write("No first name data available for this country.")
        with col2:
            st.subheader(f"Most Common Last Names in {selected_country}")
            country_last_names = last_names_df[last_names_df["country"]
                                               == selected_country]
            if not country_last_names.empty:
                st.table(country_last_names[["rank", "lastname"]])
            else:
                st.write("No last name data available for this country.")
    else:
        st.info(
            "Please select a country from the dropdown menu above to see local trends.")


# =============================================================================
# TAB 3: CROSS-CULTURAL NAMES
# =============================================================================
with tab3:
    st.header("🌐 Names Spanning Multiple Cultures")
    st.markdown(
        "Discover names that are common in many distinct regions, suggesting widespread appeal or historical connections.")

    widespread_names = names_df.groupby(
        "name")["country"].nunique().sort_values(ascending=False)
    widespread_names_df = widespread_names.reset_index().rename(
        columns={"country": "country_count"})

    st.write("Top geographically widespread names in the dataset:")
    st.dataframe(
        widespread_names_df,
        use_container_width=True,
        column_config={
            "name": "Name",
            "country_count": st.column_config.ProgressColumn(
                "Number of Countries", format="%d", min_value=0,
                max_value=int(widespread_names_df["country_count"].max()),
            ),
        },
        hide_index=True,
    )

# =============================================================================
# TAB 4: NAME MEANING & AI ANALYSIS
# =============================================================================
with tab4:
    st.header("📖 Name Meaning, Cultural Check & Fun Facts")
    st.markdown(
        "Explore the meaning, cultural context, and fun facts about names using Google Gemini AI.")

    if "GEMINI_API" not in st.secrets:
        st.error("Google API Key not found. Please add it to your Streamlit secrets (`.streamlit/secrets.toml`) to use this feature.")
        st.code("""[secrets]\nGEMINI_API = "your_api_key_here" """,
                language="toml")
    else:
        name_tool_query = st.text_input(
            "Enter a name to analyze with AI:", "Kai").strip()

        if name_tool_query:
            if name_tool_query.lower() == "mohammed":
                st.header("💥 BOOM! An explosion of fun! 💥")
                st.balloons()
                st.image("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
                         caption="Explosion of fun!")
            else:
                with st.spinner(f"Asking Gemini AI about '{name_tool_query}'..."):
                    analysis = get_name_analysis(name_tool_query)

                if analysis:
                    st.subheader(f"AI Analysis of '{name_tool_query}'")
                    col1, col2 = st.columns(2)
                    with col1:
                        if analysis.get("meaning"):
                            st.success(f"**Meaning:** {analysis['meaning']}")
                    with col2:
                        if analysis.get("origin"):
                            st.info(f"**Origin:** {analysis['origin']}")

                    st.divider()
                    st.subheader("Culturally Similar Suggestions")
                    similar_names = analysis.get("similar_names")
                    if similar_names:
                        st.write(", ".join(similar_names))
                    else:
                        st.write("No similar name suggestions available.")

                    st.divider()
                    st.subheader("Cross-Cultural Name Check")
                    cultural_issues = analysis.get("cultural_issues")
                    if cultural_issues:
                        for issue in cultural_issues:
                            st.warning(f"**Potential Issue:** {issue}")
                    else:
                        st.success(
                            "No known negative connotations identified by the AI.")

                    st.divider()
                    st.subheader("🎉 Fun Facts")
                    fun_facts = analysis.get("fun_facts")
                    if fun_facts:
                        for fact in fun_facts:
                            st.write(f"- {fact}")
                    else:
                        st.info(
                            "No fun facts were generated by the AI for this name.")
                else:
                    st.error(
                        f"Could not retrieve analysis for '{name_tool_query}'.")
