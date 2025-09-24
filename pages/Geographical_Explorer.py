# pages/geo.py
from utils import load_data, get_geojson
from typing import Optional, List
from google import genai
import colorsys
import json
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pycountry
from streamlit_plotly_events import plotly_events

# 1_Name_Explorer.py

# =============================================================================
# PAGE CONFIGURATION & DATA LOADING
# =============================================================================

st.set_page_config(
    page_title="Global Name Explorer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# CUSTOM CSS FOR UI/UX ENHANCEMENT
# =============================================================================
st.markdown("""
<style>
    /* Main App background and theme */
    .stApp {
        background-color: #F0F2F6; /* Softer background */
    }
    /* Large flag emoji for Tab 2 */
    .large-flag-emoji {
        font-size: 3em;
        line-height: 1.2;
        display: block;
        margin: 0.2em 0;
    }

    /* Define theme colors */
    :root {
        --primary-color: #4F8BF9; /* A nice, modern blue */
        --secondary-color: #6D788D; /* A muted gray for text */
        --text-color: #262730;
        --light-text-color: #ffffff;
        --card-bg-color: #ffffff;
        --border-color: #EAEBF0;
    }

    /* Hide the Streamlit header, footer, and menu */
    #MainMenu, .stDeployButton, footer {
        visibility: hidden;
    }
    header[data-testid="stHeader"] {
        background: none;
    }

    /* Main container padding */
    .main .block-container {
        padding: 2rem 2rem;
    }

    /* Title and markdown styling */
    h1 {
        color: var(--text-color);
        font-weight: 700;
    }
    h2, h3 {
        color: var(--text-color);
    }
    
    /* Custom Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid var(--border-color);
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        border: none;
        border-bottom: 2px solid transparent;
        transition: all 0.2s ease-in-out;
        color: var(--secondary-color);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E9F2FF;
        color: var(--primary-color);
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--card-bg-color);
        color: var(--primary-color);
        border-bottom: 2px solid var(--primary-color);
        font-weight: 600;
    }

    /* Styling the search input */
    [data-testid="stTextInput"] > div > div > input {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        background-color: #ffffff;
        padding: 10px 20px;
        height: 3rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    [data-testid="stTextInput"] > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(79, 139, 249, 0.2);
    }
    [data-testid="stTextInput"] label {
        display: none; /* Hide label as we have a placeholder */
    }

    /* Big GEOGRAPHICAL title (making it more subtle) */
    .geographical-title {
        font-size: 1.5em; /* Reduced size */
        font-weight: 600;
        color: var(--text-color);
        text-align: left;
        margin-bottom: 1rem;
    }
    
    /* Card component for analytics */
    .card {
        background-color: var(--card-bg-color);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        border: 1px solid var(--border-color);
        height: 300px; /* Fixed height for alignment */
        display: flex;
        flex-direction: column;
    }
    .card-title {
        font-size: 1.1em;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 15px;
    }

    /* INFO box specific styling (redesigned) */
    .info-box {
        background-color: #E9F2FF; /* Light blue background */
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        color: var(--text-color);
        border-left: 5px solid var(--primary-color);
    }
    .info-box h3 {
        color: var(--primary-color);
        font-size: 1em;
        font-weight: 700;
        text-align: left;
        margin: 0 0 5px 0;
        text-transform: uppercase;
    }
    
    /* Placeholder for analytics (redesigned) */
    .placeholder-text {
        text-align: center;
        color: var(--secondary-color);
        font-size: 0.9em;
        padding: 20px;
        flex-grow: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Center map placeholder */
    .map-placeholder {
        height: 620px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #F8F9FA;
        border-radius: 12px;
        color: var(--secondary-color);
        border: 1px dashed var(--border-color);
    }

</style>
""", unsafe_allow_html=True)


st.title("✨ Global Name Explorer")
st.markdown(
    "Your all-in-one toolkit for exploring names. Discover geographical hotspots, local trends, cross-cultural connections, and AI-powered name analysis."
)


@st.cache_data
def load_all_data():
    names_df, last_names_df = load_data()
    geojson_data = get_geojson()
    return names_df, last_names_df, geojson_data


names_df, last_names_df, geojson = load_all_data()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


COUNTRY_NAME_MAP = {
    "USA": "United States of America",
    "UK": "United Kingdom",
    "Russia": "Russian Federation",
}

REVERSE_COUNTRY_NAME_MAP = {v: k for k, v in COUNTRY_NAME_MAP.items()}


def map_country_to_geojson_name(country: str) -> str:
    """Normalize country labels to align with the GeoJSON dataset."""
    return COUNTRY_NAME_MAP.get(country, country)


def map_geojson_name_to_country(geojson_name: str) -> str:
    """Convert GeoJSON country naming back to the dataset conventions."""
    return REVERSE_COUNTRY_NAME_MAP.get(geojson_name, geojson_name)


FLAG_OVERRIDES = {
    "Kosovo": "🇽🇰",
    "Taiwan": "🇹🇼",
    "Hong Kong": "🇭🇰",
    "Czech Republic": "🇨🇿",
    "United Kingdom": "🇬🇧",
    "United States": "🇺🇸",
    "United States of America": "🇺🇸",
    "Russia": "🇷🇺",
    "Vietnam": "🇻🇳",
}


def alpha2_to_flag(alpha2: Optional[str]) -> str:
    """Convert an ISO alpha-2 code into a regional indicator flag."""
    if not alpha2 or len(alpha2) != 2:
        return ""
    base = 0x1F1E6
    try:
        return ''.join(chr(base + ord(char.upper()) - ord('A')) for char in alpha2)
    except ValueError:
        return ""


def country_to_flag(country_name: Optional[str]) -> str:
    """Return a flag emoji for the provided country name, if possible."""
    if not country_name:
        return ""

    if country_name in FLAG_OVERRIDES:
        return FLAG_OVERRIDES[country_name]

    if pycountry is None:
        return ""

    try:
        country = pycountry.countries.lookup(country_name)
        return alpha2_to_flag(country.alpha_2)
    except LookupError:
        pass

    try:
        matches = pycountry.countries.search_fuzzy(country_name)
        if matches:
            return alpha2_to_flag(matches[0].alpha_2)
    except LookupError:
        pass
    return ""


def lighten_hex_color(hex_color, factor=0.5):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
    l = min(1.0, l + (1.0 - l) * factor)
    r, g, b = (int(x*255) for x in colorsys.hls_to_rgb(h, l, s))
    return f'#{r:02x}{g:02x}{b:02x}'


def build_country_selection_map(all_names_df, geojson_obj, selected_countries: Optional[List[str]]):
    """Create an interactive mapbox choropleth for selecting countries."""
    if all_names_df.empty:
        return go.Figure()

    aggregated = (
        all_names_df.groupby("country", observed=True)["count"]
        .sum().reset_index()
    )
    aggregated["geojson_name"] = aggregated["country"].apply(
        map_country_to_geojson_name)

    top_names = (
        all_names_df.groupby(["country", "name"], observed=True)["count"]
        .sum().reset_index()
        .sort_values(["country", "count"], ascending=[True, False])
    )

    top_name_lookup = {
        country: "<br>".join([
            f"{row['name']}: {int(row['count']):,}"
            for _, row in subset.head(5).iterrows()
        ]) or "No data"
        for country, subset in top_names.groupby("country", observed=True)
    }

    hover_text = [
        "<b>{}</b><br>Total names counted: {:,}<br><br><b>Top names:</b><br>{}".format(
            row["country"],
            int(row["count"]),
            top_name_lookup.get(row["country"], "No data available"),
        )
        for _, row in aggregated.iterrows()
    ]

    base_trace = go.Choroplethmapbox(
        geojson=geojson_obj,
        locations=aggregated["geojson_name"],
        z=aggregated["count"],
        featureidkey="properties.name",
        colorscale="Blues",
        colorbar=dict(title="Total Count"),
        hovertemplate="%{customdata[0]}<extra></extra>",
        customdata=[[text] for text in hover_text],
        marker_opacity=0.7,
        marker_line_width=0.5,
    )

    fig_map = go.Figure(base_trace)

    if selected_countries:
        selected_geo_names = [map_country_to_geojson_name(
            c) for c in selected_countries]
        highlight_data = aggregated[aggregated["geojson_name"].isin(
            selected_geo_names)]

        if not highlight_data.empty:
            fig_map.add_trace(
                go.Choroplethmapbox(
                    geojson=geojson_obj,
                    locations=highlight_data["geojson_name"].tolist(),
                    z=highlight_data["count"].tolist(),
                    featureidkey="properties.name",
                    colorscale=[[0, "rgba(255,107,107,0.85)"], [
                        1, "rgba(255,107,107,0.85)"]],
                    showscale=False,
                    hoverinfo="skip",
                    marker_opacity=1.0,
                    marker_line_width=2,
                    marker_line_color="#ff6b6b",
                )
            )

    fig_map.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=1,
        mapbox_center={"lat": 40, "lon": 10},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=False,
        height=520,
        paper_bgcolor='#F0F2F6',  # Match app background
        plot_bgcolor='#F0F2F6',  # Match app background
    )
    return fig_map


def get_top_names_for_country(dataframe, country: str | None, limit: int = 5):
    """Return aggregated top names for a given country."""
    if not country:
        return None

    subset = dataframe[dataframe["country"] == country]
    if subset.empty:
        return None

    aggregated = (
        subset.groupby("name", observed=True)["count"].sum()
        .sort_values(ascending=False)
        .head(limit)
        .reset_index()
    )
    return aggregated


@st.cache_data(show_spinner=False)
def get_name_analysis(name: str):
    api_key = st.secrets.get("GEMINI_API")
    if not api_key:
        return None
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""Analyze the name "{name}". Provide a single, valid JSON object with keys: "meaning", "origin", "similar_names" (array), "cultural_issues" (array), "fun_facts" (array). Respond with ONLY the JSON."""
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=prompt)
        if not response.text:
            return None
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_response)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None


# =============================================================================
# TABS FOR DIFFERENT FUNCTIONALITIES
# =============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Geographical Explorer", "📈 Local Trends", "🌐 Cross-Cultural Names", "📖 Name Meaning & AI Analysis"
])

# =============================================================================
# TAB 1: GEOGRAPHICAL NAME EXPLORATION (REDESIGNED)
# =============================================================================
with tab1:
    left_col, mid_col, right_col = st.columns([1.3, 3, 1.3])

    with left_col:
        st.markdown('<h2 class="geographical-title">Search Names</h2>',
                    unsafe_allow_html=True)
        name_query = st.text_input(value='Aria',
                                   label="SEARCH", placeholder="Search names (e.g., Maria, Alex)", label_visibility="collapsed")

        st.markdown(
            '<div class="info-box"><h3>HOW TO USE</h3>Search for one or more names (comma-separated) to see popularity hotspots on the map.</div>', unsafe_allow_html=True)

    search_data = None
    if name_query:
        name_queries = [name.strip().lower()
                        for name in name_query.split(",") if name.strip()]
        if name_queries:
            search_data = names_df[names_df["name"].str.lower().isin(
                name_queries)]

    with mid_col:
        if search_data is not None and not search_data.empty:
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
            colorbar_len = max(
                0.1, (0.8 - (num_names - 1) * 0.05) / num_names if num_names > 0 else 0)

            for i, name_lower in enumerate(unique_names_found):
                name_capitalized = name_lower.capitalize()
                dominant_countries_for_name = dominant_name_df[dominant_name_df["name"].str.lower(
                ) == name_lower]
                if dominant_countries_for_name.empty:
                    continue
                base_color_hex = name_color_map[name_lower]
                color_scale = [[0.0, lighten_hex_color(base_color_hex, 0.7)], [
                    1.0, base_color_hex]]
                y_pos = 0.95 - i * (colorbar_len + 0.05)
                fig_map.add_trace(go.Choroplethmapbox(
                    geojson=geojson, locations=dominant_countries_for_name[
                        "geojson_name"], z=dominant_countries_for_name["count"],
                    featureidkey="properties.name", colorscale=color_scale,
                    colorbar=dict(title=f"{name_capitalized}", x=1.02, xanchor="left",
                                  len=colorbar_len, y=y_pos, yanchor="top", tickfont=dict(color='black')),
                    marker_opacity=0.8, marker_line_width=0,
                    hovertemplate=f"<b>Country:</b> %{{location}}<br><b>Dominant:</b> {name_capitalized}<br><b>Count:</b> %{{z}}<extra></extra>"
                ))
            fig_map.update_layout(
                mapbox_style="carto-positron", mapbox_zoom=1, mapbox_center={"lat": 40, "lon": 10},
                margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False, height=620,
                paper_bgcolor='#F0F2F6',  # Match app background
                plot_bgcolor='#F0F2F6'   # Match app background
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            if name_query:
                st.warning(
                    f"No data found for '{name_query}'. Please try another name.")
            st.markdown(
                f"<div class='map-placeholder'>Search for a name to view the global distribution map.</div>", unsafe_allow_html=True)

    with right_col:
        # This whole section has been adjusted for better vertical compactness.

        # GENDER DISTRIBUTION PIE CHART
        # The title is now integrated directly into the Plotly chart,
        # removing the extra space from the st.markdown title element.
        if search_data is not None and not search_data.empty:
            gender_dist = search_data.groupby(
                "gender")["count"].sum().reset_index()
            fig_pie = px.pie(gender_dist, values="count", names="gender",
                             title="Gender Distribution",
                             color_discrete_map={"F": "#FFB6C1", "M": "#87CEFA", "U": "#D3D3D3"})
            fig_pie.update_layout(
                margin=dict(l=10, r=10, t=35, b=10),  # Reduced margins
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font_size=18,
                title_x=0.05,  # Left-aligned to match other titles
            )
            fig_pie.update_traces(
                textposition="inside", textinfo="percent+label", textfont_color='black')
            st.plotly_chart(fig_pie, use_container_width=True,
                            config={'displayModeBar': False})
        else:
            # Fallback for when no data is available
            st.markdown(
                '<div class="card-title">Gender Distribution</div>', unsafe_allow_html=True)
            st.markdown(
                "<div class='placeholder-text'>Search for a name to see gender data.</div>", unsafe_allow_html=True)

        # TOP COUNTRIES TABLE
        # The fixed height of the dataframe has been removed to allow it to
        # dynamically size to its content, saving space.
        st.markdown(
            '<div class="card-title">Top Countries by Count</div>', unsafe_allow_html=True)
        if search_data is not None and not search_data.empty:
            total_counts_by_country = search_data.groupby(
                "country")["count"].sum().sort_values(ascending=False).reset_index()
            st.dataframe(total_counts_by_country.head(10),
                         use_container_width=True,
                         hide_index=True)  # Removed fixed height
        else:
            st.markdown(
                "<div class='placeholder-text'>Search for a name to see country data.</div>", unsafe_allow_html=True)


# =============================================================================
# TAB 2: LOCAL NAMING TRENDS [REVISED & FIXED]
# =============================================================================
with tab2:
    st.header("📈 Discover Local Naming Trends")
    st.markdown(
        "Use the interactive map or the dropdown below to select one or more countries. Selecting multiple countries will show names that are common to all of them."
    )

    # Use a list for multiple country selection
    if "local_trends_countries" not in st.session_state:
        st.session_state["local_trends_countries"] = []

    available_countries = sorted(names_df["country"].unique())

    map_col, info_col = st.columns([2, 1])
    with map_col:
        selection_map = build_country_selection_map(
            names_df, geojson, st.session_state["local_trends_countries"]
        )
        map_events = plotly_events(
            selection_map,
            click_event=True,
            select_event=False,
            hover_event=False,
            override_height=520,
            key="local_trends_map",
        )

    if map_events:
        event = map_events[0]
        clicked_geo_name = event.get("location")
        if not clicked_geo_name:
            curve_idx = event.get("curveNumber", 0)
            point_idx = event.get("pointIndex")
            if point_idx is None:
                point_idx = event.get("pointNumber")
            if point_idx is not None and selection_map.data:
                curve_idx = min(curve_idx, len(selection_map.data) - 1)
                locations = selection_map.data[curve_idx].locations
                if locations and point_idx < len(locations):
                    clicked_geo_name = locations[point_idx]

        if clicked_geo_name:
            derived_country = map_geojson_name_to_country(clicked_geo_name)
            if derived_country in available_countries:
                current_selection = st.session_state["local_trends_countries"]
                if derived_country in current_selection:
                    current_selection.remove(derived_country)  # Toggle off
                else:
                    current_selection.append(derived_country)  # Toggle on
                st.session_state["local_trends_countries"] = current_selection
                st.rerun()

    with info_col:
        selected_countries = st.multiselect(
            "Select countries to explore:",
            available_countries,
            key="local_trends_countries",
        )

        if selected_countries:
            st.write("#### Selected Countries:")
            flags = " ".join(
                [f for f in [country_to_flag(c) for c in selected_countries] if f])
            if flags:
                st.markdown(
                    f"<div class='large-flag-emoji'>{flags}</div>", unsafe_allow_html=True)
            for country in selected_countries:
                st.markdown(f"• {country}")

    st.divider()

    # Data Display Logic
    selected_countries = st.session_state.get("local_trends_countries", [])

    if not selected_countries:
        st.info(
            "Please select one or more countries from the map or dropdown to see local trends.")

    elif len(selected_countries) == 1:
        selected_country = selected_countries[0]
        st.markdown(f"### Showing Stats for **{selected_country}**")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Most Common First Names")
            country_first_names = names_df[names_df["country"] == selected_country].nlargest(
                10, "count")
            if not country_first_names.empty:
                fig_bar = px.bar(
                    country_first_names.sort_values("count", ascending=True),
                    y="name", x="count", color="gender",
                    title=f"Top 10 First Names",
                    labels={"count": "Count", "name": "Name"},
                    color_discrete_map={"F": "#FFB6C1",
                                        "M": "#87CEFA", "U": "#D3D3D3"},
                    orientation='h'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No first name data available for this country.")
        with col2:
            st.subheader(f"Most Common Last Names")
            country_last_names = last_names_df[last_names_df["country"]
                                               == selected_country]
            if not country_last_names.empty:
                st.dataframe(country_last_names[["rank", "lastname"]].head(
                    20), use_container_width=True, hide_index=True)
            else:
                st.info("No last name data available for this country.")

    else:  # Multiple countries selected
        num_countries = len(selected_countries)
        st.markdown(
            f"### Cross-examining Names Across **{num_countries}** Countries")
        st.write(
            f"Showing names that exist in all selected countries: {', '.join(selected_countries)}")

        # --- First Names Logic ---
        first_names_filtered = names_df[names_df['country'].isin(
            selected_countries)]
        name_counts_per_country = first_names_filtered.groupby('name')[
            'country'].nunique()
        common_first_names_list = name_counts_per_country[name_counts_per_country ==
                                                          num_countries].index
        common_first_names_df = first_names_filtered[first_names_filtered['name'].isin(
            common_first_names_list)]

        # --- Last Names Logic ---
        last_names_filtered = last_names_df[last_names_df['country'].isin(
            selected_countries)]
        lastname_counts_per_country = last_names_filtered.groupby('lastname')[
            'country'].nunique()
        common_last_names_list = lastname_counts_per_country[
            lastname_counts_per_country == num_countries].index
        common_last_names_df = last_names_filtered[last_names_filtered['lastname'].isin(
            common_last_names_list)]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Common First Names")
            if not common_first_names_df.empty:
                aggregated_first_names = common_first_names_df.groupby(
                    'name')['count'].sum().nlargest(10).reset_index()
                fig_bar_common = px.bar(
                    aggregated_first_names.sort_values(
                        "count", ascending=True),
                    y="name", x="count",
                    title=f"Top 10 Common First Names (Total Count)",
                    labels={"count": "Total Count", "name": "Name"},
                    orientation='h'
                )
                st.plotly_chart(fig_bar_common, use_container_width=True)
            else:
                st.info(
                    "No first names were found to be common across all selected countries.")

        with col2:
            st.subheader("Common Last Names")
            if not common_last_names_df.empty:
                st.write(
                    "Common last names and their rank in each country (Top 20 shown):")
                pivot_df = common_last_names_df.pivot(
                    index='lastname', columns='country', values='rank').reset_index()
                st.dataframe(pivot_df.head(
                    20), use_container_width=True, hide_index=True)
            else:
                st.info(
                    "No last names were found to be common across all selected countries.")


# =============================================================================
# TAB 3: CROSS-CULTURAL NAMES
# =============================================================================
with tab3:
    st.header("🌐 Names Spanning Multiple Cultures")
    st.markdown("Discover names that are common in many distinct regions.")
    widespread_names = names_df.groupby(
        "name")["country"].nunique().sort_values(ascending=False)
    widespread_names_df = widespread_names.reset_index().rename(
        columns={"country": "country_count"})
    st.write("Top geographically widespread names:")
    st.dataframe(widespread_names_df, use_container_width=True, hide_index=True,
                 column_config={"name": "Name", "country_count": st.column_config.ProgressColumn("Number of Countries", format="%d", min_value=0, max_value=int(widespread_names_df["country_count"].max()))})

# =============================================================================
# TAB 4: NAME MEANING & AI ANALYSIS
# =============================================================================
with tab4:
    st.header("📖 Name Meaning, Cultural Check & Fun Facts")
    st.markdown("Explore names using Google Gemini AI.")
    if "GEMINI_API" not in st.secrets:
        st.error(
            "Google API Key not found. Please add it to your Streamlit secrets to use this feature.")
    else:
        name_tool_query = st.text_input(
            "Enter a name to analyze with AI:", "Kai").strip()
        if name_tool_query:
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
                st.write(", ".join(analysis.get("similar_names", ["N/A"])))
                st.divider()
                st.subheader("Cross-Cultural Name Check")
                cultural_issues = analysis.get("cultural_issues")
                if cultural_issues:
                    for issue in cultural_issues:
                        st.warning(f"**Potential Issue:** {issue}")
                else:
                    st.success("No known negative connotations identified.")
                st.divider()
                st.subheader("🎉 Fun Facts")
                fun_facts = analysis.get("fun_facts")
                if fun_facts:
                    for fact in fun_facts:
                        st.write(f"- {fact}")
                else:
                    st.info("No fun facts generated.")
            else:
                st.error(
                    f"Could not retrieve analysis for '{name_tool_query}'.")
