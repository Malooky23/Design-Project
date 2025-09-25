# # pages/Geographical_Explorer.py
# from utils import load_data, get_geojson
# from typing import Optional, List
# from google import genai
# import colorsys
# import json
# import plotly.graph_objects as go
# import plotly.express as px
# import streamlit as st
# import pycountry
# from streamlit_plotly_events import plotly_events

# # 1_Name_Explorer.py

# # =============================================================================
# # PAGE CONFIGURATION & DATA LOADING
# # =============================================================================

# st.set_page_config(
#     page_title="Name Explorer",
#     page_icon=None,
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # =============================================================================
# # CUSTOM CSS FOR UI/UX ENHANCEMENT
# # =============================================================================
# st.markdown("""
# <style>
#     /* Main App background and theme */
#     .stApp {
#         background-color: #F0F2F6; /* Softer background */
#     }
#     /* Large flag emoji for Tab 2 */
#     .large-flag-emoji {
#         font-size: 3em;
#         line-height: 1.2;
#         display: block;
#         margin: 0.2em 0;
#     }

#     /* Define theme colors */
#     :root {
#         --primary-color: #4F8BF9; /* A nice, modern blue */
#         --secondary-color: #6D788D; /* A muted gray for text */
#         --text-color: #262730;
#         --light-text-color: #ffffff;
#         --card-bg-color: #ffffff;
#         --border-color: #EAEBF0;
#     }

#     /* Hide the Streamlit header, footer, and menu */
#     #MainMenu, .stDeployButton, footer {
#         visibility: hidden;
#     }
#     header[data-testid="stHeader"] {
#         background: none;
#     }

#     /* Main container padding */
#     .main .block-container {
#         padding: 2rem 2rem;
#     }

#     /* Title and markdown styling */
#     h1 {
#         color: var(--text-color);
#         font-weight: 700;
#     }
#     h2, h3 {
#         color: var(--text-color);
#     }
    
#     /* Custom Tab styling */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#         border-bottom: 1px solid var(--border-color);
#     }
#     .stTabs [data-baseweb="tab"] {
#         height: 48px;
#         background-color: transparent;
#         border-radius: 8px 8px 0 0;
#         border: none;
#         border-bottom: 2px solid transparent;
#         transition: all 0.2s ease-in-out;
#         color: var(--secondary-color);
#     }
#     .stTabs [data-baseweb="tab"]:hover {
#         background-color: #E9F2FF;
#         color: var(--primary-color);
#     }
#     .stTabs [aria-selected="true"] {
#         background-color: var(--card-bg-color);
#         color: var(--primary-color);
#         border-bottom: 2px solid var(--primary-color);
#         font-weight: 600;
#     }

#     /* Styling the search input */
#     [data-testid="stTextInput"] > div > div > input {
#         border-radius: 8px;
#         border: 1px solid var(--border-color);
#         background-color: #ffffff;
#         padding: 10px 20px;
#         height: 3rem;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.05);
#         transition: border-color 0.2s, box-shadow 0.2s;
#     }
#     [data-testid="stTextInput"] > div > div > input:focus {
#         border-color: var(--primary-color);
#         box-shadow: 0 0 0 3px rgba(79, 139, 249, 0.2);
#     }
#     [data-testid="stTextInput"] label {
#         display: none; /* Hide label as we have a placeholder */
#     }

#     /* Custom styling for the multiselect in Tab 2 */
#     [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
#         background-color: #ffffff !important;
#         border: 2px solid #800000 !important; /* Maroon border */
#         border-radius: 8px;
#     }

#     /* Big GEOGRAPHICAL title (making it more subtle) */
#     .geographical-title {
#         font-size: 1.5em; /* Reduced size */
#         font-weight: 600;
#         color: var(--text-color);
#         text-align: left;
#         margin-bottom: 1rem;
#     }
    
#     /* Card component for analytics */
#     .card {
#         background-color: var(--card-bg-color);
#         border-radius: 12px;
#         padding: 24px;
#         margin-bottom: 20px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.04);
#         border: 1px solid var(--border-color);
#         height: 300px; /* Fixed height for alignment */
#         display: flex;
#         flex-direction: column;
#     }
#     .card-title {
#         font-size: 1.1em;
#         font-weight: 600;
#         color: var(--text-color);
#         margin-bottom: 15px;
#     }

#     /* INFO box specific styling (redesigned) */
#     .info-box {
#         background-color: #E9F2FF; /* Light blue background */
#         border-radius: 10px;
#         padding: 15px;
#         margin-top: 20px;
#         color: var(--text-color);
#         border-left: 5px solid var(--primary-color);
#     }
#     .info-box h3 {
#         color: var(--primary-color);
#         font-size: 1em;
#         font-weight: 700;
#         text-align: left;
#         margin: 0 0 5px 0;
#         text-transform: uppercase;
#     }
    
#     /* Placeholder for analytics (redesigned) */
#     .placeholder-text {
#         text-align: center;
#         color: var(--secondary-color);
#         font-size: 0.9em;
#         padding: 20px;
#         flex-grow: 1;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
    
#     /* Center map placeholder */
#     .map-placeholder {
#         height: 620px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         background: #F8F9FA;
#         border-radius: 12px;
#         color: var(--secondary-color);
#         border: 1px dashed var(--border-color);
#     }

# </style>
# """, unsafe_allow_html=True)


# st.title("Name Explorer")
# st.markdown(
#     "Your all-in-one toolkit for exploring names. Discover geographical hotspots, local trends, cross-cultural connections, and AI-powered name analysis."
# )


# @st.cache_data
# def load_all_data():
#     names_df, last_names_df = load_data()
#     geojson_data = get_geojson()
#     return names_df, last_names_df, geojson_data


# names_df, last_names_df, geojson = load_all_data()

# # =============================================================================
# # HELPER FUNCTIONS
# # =============================================================================


# COUNTRY_NAME_MAP = {
#     "USA": "United States of America",
#     "UK": "United Kingdom",
#     "Russia": "Russian Federation",
# }

# REVERSE_COUNTRY_NAME_MAP = {v: k for k, v in COUNTRY_NAME_MAP.items()}


# def map_country_to_geojson_name(country: str) -> str:
#     """Normalize country labels to align with the GeoJSON dataset."""
#     return COUNTRY_NAME_MAP.get(country, country)


# def map_geojson_name_to_country(geojson_name: str) -> str:
#     """Convert GeoJSON country naming back to the dataset conventions."""
#     return REVERSE_COUNTRY_NAME_MAP.get(geojson_name, geojson_name)


# FLAG_OVERRIDES = {
#     "Kosovo": "🇽🇰",
#     "Taiwan": "🇹🇼",
#     "Hong Kong": "🇭🇰",
#     "Czech Republic": "🇨🇿",
#     "United Kingdom": "🇬🇧",
#     "United States": "🇺🇸",
#     "United States of America": "🇺🇸",
#     "Russia": "🇷🇺",
#     "Vietnam": "🇻🇳",
# }


# def alpha2_to_flag(alpha2: Optional[str]) -> str:
#     """Convert an ISO alpha-2 code into a regional indicator flag."""
#     if not alpha2 or len(alpha2) != 2:
#         return ""
#     base = 0x1F1E6
#     try:
#         return ''.join(chr(base + ord(char.upper()) - ord('A')) for char in alpha2)
#     except ValueError:
#         return ""


# def country_to_flag(country_name: Optional[str]) -> str:
#     """Return a flag emoji for the provided country name, if possible."""
#     if not country_name:
#         return ""

#     if country_name in FLAG_OVERRIDES:
#         return FLAG_OVERRIDES[country_name]

#     if pycountry is None:
#         return ""

#     try:
#         country = pycountry.countries.lookup(country_name)
#         return alpha2_to_flag(country.alpha_2)
#     except LookupError:
#         pass

#     try:
#         matches = pycountry.countries.search_fuzzy(country_name)
#         if matches:
#             return alpha2_to_flag(matches[0].alpha_2)
#     except LookupError:
#         pass
#     return ""


# def lighten_hex_color(hex_color, factor=0.5):
#     hex_color = hex_color.lstrip('#')
#     rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
#     h, l, s = colorsys.rgb_to_hls(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
#     l = min(1.0, l + (1.0 - l) * factor)
#     r, g, b = (int(x*255) for x in colorsys.hls_to_rgb(h, l, s))
#     return f'#{r:02x}{g:02x}{b:02x}'


# def build_static_country_map(geojson_obj: dict, selected_countries: List[str]):
#     """
#     Creates a non-interactive map to display selected countries.
#     It highlights selected countries and shows the rest in a neutral color.
#     """
#     # Get all country names from the GeoJSON to draw the base map
#     all_geojson_countries = [
#         feature['properties']['name'] for feature in geojson_obj['features']
#         if 'name' in feature.get('properties', {})
#     ]

#     # Convert selected country names to the format used in GeoJSON
#     selected_geo_names = [map_country_to_geojson_name(
#         c) for c in selected_countries]

#     fig = go.Figure()

#     # Base layer: all countries in a neutral gray
#     fig.add_trace(go.Choroplethmapbox(
#         geojson=geojson_obj,
#         locations=all_geojson_countries,
#         z=[0] * len(all_geojson_countries),  # Dummy data for a single color
#         featureidkey="properties.name",
#         colorscale=[[0, '#EAEBF0'], [1, '#EAEBF0']],  # Neutral light gray
#         showscale=False,
#         hoverinfo='skip',  # No hover info for the base layer
#         marker_opacity=1,
#         marker_line_width=0.5,
#     ))

#     # Highlight layer: selected countries in the primary app color
#     if selected_geo_names:
#         fig.add_trace(go.Choroplethmapbox(
#             geojson=geojson_obj,
#             locations=selected_geo_names,
#             z=[1] * len(selected_geo_names),  # Dummy data for a single color
#             featureidkey="properties.name",
#             colorscale=[[0, '#4F8BF9'], [1, '#4F8BF9']],  # Primary blue
#             showscale=False,
#             hoverinfo='location',  # Show country name on hover
#             hovertemplate="<b>%{location}</b><extra></extra>",
#             marker_opacity=1,
#             marker_line_width=1,
#             marker_line_color='#262730',
#         ))

#     fig.update_layout(
#         mapbox_style="carto-positron",
#         mapbox_zoom=0.8,
#         mapbox_center={"lat": 40, "lon": 10},
#         margin={"r": 0, "t": 0, "l": 0, "b": 0},
#         showlegend=False,
#         height=450,
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#     )
#     return fig


# @st.cache_data(show_spinner=False)
# def get_name_analysis(name: str):
#     api_key = st.secrets.get("GEMINI_API")
#     if not api_key:
#         return None
#     try:
#         client = genai.Client(api_key=api_key)
#         prompt = f"""Analyze the name "{name}". Provide a single, valid JSON object with keys: "meaning", "origin", "similar_names" (array), "cultural_issues" (array), "fun_facts" (array). Respond with ONLY the JSON."""
#         response = client.models.generate_content(
#             model="gemini-2.5-flash-lite", contents=prompt)
#         if not response.text:
#             return None
#         clean_response = response.text.strip().replace("```json", "").replace("```", "")
#         return json.loads(clean_response)
#     except Exception as e:
#         print(f"Gemini API Error: {e}")
#         return None


# # =============================================================================
# # TABS FOR DIFFERENT FUNCTIONALITIES
# # =============================================================================
# tab1, tab2, tab3, tab4 = st.tabs([
#     "Geographical Explorer", "Local Trends", "Cross-Cultural Names", "Gender Neutral Names"
# ])

# # =============================================================================
# # TAB 1: GEOGRAPHICAL NAME EXPLORATION (REDESIGNED)
# # =============================================================================
# with tab1:
#     left_col, mid_col, right_col = st.columns([1.3, 3, 1.3])

#     with left_col:
#         st.markdown('<h2 class="geographical-title">Search Names</h2>',
#                     unsafe_allow_html=True)
#         # Use a form to prevent rerunning on every keystroke, which caused crashes.
#         with st.form(key="name_search_form"):
#             name_query = st.text_input(
#                 value='Aria',
#                 label="SEARCH",
#                 placeholder="Search names (e.g., Maria, Alex)",
#                 label_visibility="collapsed"
#             )
#             search_button = st.form_submit_button("Search")

#         st.markdown(
#             '<div class="info-box"><h3>HOW TO USE</h3>Search for one or more names (comma-separated) to see popularity hotspots on the map.</div>', unsafe_allow_html=True)

#     search_data = None
#     # Only perform the search when the form is submitted
#     if search_button and name_query:
#         name_queries = [name.strip().lower()
#                         for name in name_query.split(",") if name.strip()]
#         if name_queries:
#             search_data = names_df[names_df["name"].str.lower().isin(
#                 name_queries)]

#     with mid_col:
#         if search_data is not None and not search_data.empty:
#             country_name_counts = search_data.groupby(["country", "name"], observed=True)[
#                 "count"].sum().reset_index()
#             dominant_name_df = country_name_counts.loc[country_name_counts.groupby(
#                 "country", observed=True)["count"].idxmax()].copy()
#             country_name_map = {"USA": "United States of America",
#                                 "UK": "United Kingdom", "Russia": "Russian Federation"}
#             dominant_name_df["geojson_name"] = dominant_name_df["country"].replace(
#                 country_name_map)
#             unique_names_found = sorted(
#                 list(dominant_name_df["name"].str.lower().unique()))
#             colors = px.colors.qualitative.Plotly
#             name_color_map = {name: colors[i % len(
#                 colors)] for i, name in enumerate(unique_names_found)}

#             # --- MEMORY OPTIMIZATION START ---
#             all_plot_countries = dominant_name_df["geojson_name"].unique()
#             filtered_geojson = {
#                 "type": "FeatureCollection",
#                 "features": [
#                     feature for feature in geojson["features"]
#                     if feature.get("properties", {}).get("name") in all_plot_countries
#                 ]
#             }
#             # --- MEMORY OPTIMIZATION END ---

#             fig_map = go.Figure()
#             num_names = len(unique_names_found)
#             colorbar_len = max(
#                 0.1, (0.8 - (num_names - 1) * 0.05) / num_names if num_names > 0 else 0)

#             for i, name_lower in enumerate(unique_names_found):
#                 name_capitalized = name_lower.capitalize()
#                 dominant_countries_for_name = dominant_name_df[dominant_name_df["name"].str.lower(
#                 ) == name_lower]
#                 if dominant_countries_for_name.empty:
#                     continue
#                 base_color_hex = name_color_map[name_lower]
#                 color_scale = [[0.0, lighten_hex_color(base_color_hex, 0.7)], [
#                     1.0, base_color_hex]]
#                 y_pos = 0.95 - i * (colorbar_len + 0.05)
#                 fig_map.add_trace(go.Choroplethmapbox(
#                     geojson=filtered_geojson,
#                     locations=dominant_countries_for_name["geojson_name"],
#                     z=dominant_countries_for_name["count"],
#                     featureidkey="properties.name", colorscale=color_scale,
#                     colorbar=dict(title=f"{name_capitalized}", x=1.02, xanchor="left",
#                                   len=colorbar_len, y=y_pos, yanchor="top", tickfont=dict(color='black')),
#                     marker_opacity=0.8, marker_line_width=0,
#                     hovertemplate=f"<b>Country:</b> %{{location}}<br><b>Dominant:</b> {name_capitalized}<br><b>Count:</b> %{{z}}<extra></extra>"
#                 ))
#             fig_map.update_layout(
#                 mapbox_style="carto-positron", mapbox_zoom=1, mapbox_center={"lat": 40, "lon": 10},
#                 margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False, height=620,
#                 paper_bgcolor='#F0F2F6',
#                 plot_bgcolor='#F0F2F6'
#             )
#             st.plotly_chart(fig_map, use_container_width=True)
#         else:
#             # Show a warning only if a search was attempted and failed
#             if search_button and name_query:
#                 st.warning(
#                     f"No data found for '{name_query}'. Please try another name.")
#             st.markdown(
#                 f"<div class='map-placeholder'>Search for a name to view the global distribution map.</div>", unsafe_allow_html=True)

#     with right_col:
#         if search_data is not None and not search_data.empty:
#             gender_dist = search_data.groupby(
#                 "gender")["count"].sum().reset_index()
#             fig_pie = px.pie(gender_dist, values="count", names="gender",
#                              title="Gender Distribution",
#                              color_discrete_map={"F": "#FFB6C1", "M": "#87CEFA", "U": "#D3D3D3"})
#             fig_pie.update_layout(
#                 margin=dict(l=10, r=10, t=35, b=10),
#                 showlegend=False,
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 title_font_size=18,
#                 title_x=0.05,
#             )
#             fig_pie.update_traces(
#                 textposition="inside", textinfo="percent+label", textfont_color='black')
#             st.plotly_chart(fig_pie, use_container_width=True,
#                             config={'displayModeBar': False})
#         else:
#             st.markdown(
#                 '<div class="card-title">Gender Distribution</div>', unsafe_allow_html=True)
#             st.markdown(
#                 "<div class='placeholder-text'>Search for a name to see gender data.</div>", unsafe_allow_html=True)

#         st.markdown(
#             '<div class="card-title">Top Countries by Count</div>', unsafe_allow_html=True)
#         if search_data is not None and not search_data.empty:
#             total_counts_by_country = search_data.groupby(
#                 "country")["count"].sum().sort_values(ascending=False).reset_index()
#             st.dataframe(total_counts_by_country.head(10),
#                          use_container_width=True,
#                          hide_index=True)
#         else:
#             st.markdown(
#                 "<div class='placeholder-text'>Search for a name to see country data.</div>", unsafe_allow_html=True)


# # =============================================================================
# # TAB 2: LOCAL NAMING TRENDS [SIMPLIFIED & STABLE]
# # =============================================================================
# with tab2:
#     st.header("Discover Local Naming Trends")
#     st.markdown(
#         "Use the dropdown to select countries and see them highlighted on the map. The charts below will update to show trends for your selection."
#     )

#     control_col, map_col = st.columns([1, 1.5])

#     with control_col:
#         available_countries = sorted(names_df["country"].unique())
#         selected_countries = st.multiselect(
#             "Select countries to explore:",
#             available_countries,
#             default=["Sweden", "Japan"],
#             key="local_trends_countries",
#         )

#     with map_col:
#         # Build and display the lightweight, non-interactive map
#         static_map_fig = build_static_country_map(geojson, selected_countries)
#         st.plotly_chart(static_map_fig, use_container_width=True,
#                         config={'displayModeBar': False})

#     st.divider()

#     if not selected_countries:
#         st.info(
#             "Please select one or more countries from the dropdown to see local trends.")

#     elif len(selected_countries) == 1:
#         selected_country = selected_countries[0]
#         st.markdown(f"### Showing Stats for **{selected_country}**")

#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader(f"Most Common First Names")
#             country_first_names = names_df[names_df["country"] == selected_country].nlargest(
#                 10, "count")
#             if not country_first_names.empty:
#                 fig_bar = px.bar(
#                     country_first_names.sort_values("count", ascending=True),
#                     y="name", x="count", color="gender",
#                     title=f"Top 10 First Names",
#                     labels={"count": "Count", "name": "Name"},
#                     color_discrete_map={"F": "#FFB6C1",
#                                         "M": "#87CEFA", "U": "#D3D3D3"},
#                     orientation='h'
#                 )
#                 st.plotly_chart(fig_bar, use_container_width=True)
#             else:
#                 st.info("No first name data available for this country.")
#         with col2:
#             st.subheader(f"Most Common Last Names")
#             country_last_names = last_names_df[last_names_df["country"]
#                                                == selected_country]
#             if not country_last_names.empty:
#                 st.dataframe(country_last_names[["rank", "lastname"]].head(
#                     20), use_container_width=True, hide_index=True)
#             else:
#                 st.info("No last name data available for this country.")

#     else:  # This block handles multiple selected countries
#         num_countries = len(selected_countries)
#         st.markdown(
#             f"### Cross-examining Names Across **{num_countries}** Countries")
#         st.write(
#             f"Showing names that exist in all selected countries: {', '.join(selected_countries)}")

#         first_names_filtered = names_df[names_df['country'].isin(
#             selected_countries)]
#         name_counts_per_country = first_names_filtered.groupby('name')[
#             'country'].nunique()
#         common_first_names_list = name_counts_per_country[name_counts_per_country ==
#                                                           num_countries].index
#         common_first_names_df = first_names_filtered[first_names_filtered['name'].isin(
#             common_first_names_list)]

#         last_names_filtered = last_names_df[last_names_df['country'].isin(
#             selected_countries)]
#         lastname_counts_per_country = last_names_filtered.groupby('lastname')[
#             'country'].nunique()
#         common_last_names_list = lastname_counts_per_country[
#             lastname_counts_per_country == num_countries].index
#         common_last_names_df = last_names_filtered[last_names_filtered['lastname'].isin(
#             common_last_names_list)]

#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("Common First Names")
#             if not common_first_names_df.empty:
#                 aggregated_first_names = common_first_names_df.groupby(
#                     'name')['count'].sum().nlargest(10).reset_index()
#                 fig_bar_common = px.bar(
#                     aggregated_first_names.sort_values(
#                         "count", ascending=True),
#                     y="name", x="count",
#                     title=f"Top 10 Common First Names (Total Count)",
#                     labels={"count": "Total Count", "name": "Name"},
#                     orientation='h'
#                 )
#                 st.plotly_chart(fig_bar_common, use_container_width=True)
#             else:
#                 st.info(
#                     "No first names were found to be common across all selected countries.")

#         with col2:
#             st.subheader("Common Last Names")
#             if not common_last_names_df.empty:
#                 st.write(
#                     "Common last names and their rank in each country (Top 20 shown):")
#                 pivot_df = common_last_names_df.pivot(
#                     index='lastname', columns='country', values='rank').reset_index()
#                 st.dataframe(pivot_df.head(
#                     20), use_container_width=True, hide_index=True)
#             else:
#                 st.info(
#                     "No last names were found to be common across all selected countries.")


# # =============================================================================
# # TAB 3: CROSS-CULTURAL NAMES
# # =============================================================================
# with tab3:
#     st.header("Names Spanning Multiple Cultures")
#     st.markdown(
#         "Discover names that are common in many distinct regions. Use the search bar below to filter the list.")

#     widespread_names = names_df.groupby(
#         "name")["country"].nunique().sort_values(ascending=False)
#     widespread_names_df = widespread_names.reset_index().rename(
#         columns={"country": "country_count"})

#     name_search_query = st.text_input(
#         "Search for a name in the list:", "", placeholder="e.g. Maria")

#     if name_search_query:
#         display_df = widespread_names_df[widespread_names_df['name'].str.contains(
#             name_search_query, case=False, na=False)]
#     else:
#         display_df = widespread_names_df

#     st.write("Geographically widespread names:")
#     st.dataframe(display_df, use_container_width=True, hide_index=True,
#                  column_config={"name": "Name", "country_count": st.column_config.ProgressColumn("Number of Countries", format="%d", min_value=0, max_value=int(widespread_names_df["country_count"].max()))})


# with tab4:
#     st.header("Gender-Neutral Name Finder")
#     st.markdown(
#         "Discover names with a close to 50/50 gender split in our dataset. Sort by gender-neutrality to find the most balanced names."
#     )

#     # Find names that appear for both Male and Female
#     mf_names_df = names_df[names_df['gender'].isin(['M', 'F'])]
#     name_gender_counts = mf_names_df.groupby('name')['gender'].nunique()
#     neutral_name_list = name_gender_counts[name_gender_counts > 1].index

#     if not neutral_name_list.empty:
#         neutral_df = mf_names_df[mf_names_df['name'].isin(
#             neutral_name_list)].copy()

#         # Pivot to get M and F counts per name
#         gender_pivot = neutral_df.pivot_table(
#             index='name',
#             columns='gender',
#             values='count',
#             aggfunc='sum',
#             fill_value=0
#         )

#         # Calculate totals, percentages, and neutrality score
#         gender_pivot['count'] = gender_pivot['M'] + gender_pivot['F']
#         gender_pivot['female %'] = (
#             gender_pivot['F'] / gender_pivot['count']) * 100
#         gender_pivot['male %'] = (
#             gender_pivot['M'] / gender_pivot['count']) * 100
#         # Neutrality: sum of both percentages (double the percentage of the minority group)
#         gender_pivot['neutrality %'] = 2 * \
#             gender_pivot[['female %', 'male %']].min(axis=1)
#         # Score: distance from perfect 50/50 split
#         gender_pivot['neutrality_score'] = abs(gender_pivot['female %'] - 50)

#         # Prepare final dataframe for display
#         display_df = gender_pivot.reset_index()[[
#             'name', 'count', 'female %', 'male %', 'neutrality %'
#         ]]

#         display_df.rename(columns={
#             'name': 'Name',
#             'count': 'Total Count',
#             'female %': 'Female %',
#             'male %': 'Male %',
#             'neutrality %': 'Neutrality %',
#         }, inplace=True)

#         display_df = display_df[[
#             'Name', 'Total Count', 'Female %', 'Male %', 'Neutrality %']]

#         # Show top 10 most neutral names by default
#         default_display_df = display_df.sort_values(
#             'Neutrality %', ascending=False).head()

#         num_names_to_show = st.slider(
#             "How many names to display?",
#             min_value=10,
#             max_value=len(display_df),
#             value=10,
#             step=10,
#             key="neutral_names_slider"
#         )

#         st.dataframe(
#             display_df.sort_values(
#                 'Neutrality %', ascending=False).head(num_names_to_show),
#             column_config={
#                 "Name": st.column_config.TextColumn("Name"),
#                 "Total Count": st.column_config.NumberColumn("Total Count", format="%d"),
#                 "Female %": st.column_config.ProgressColumn(
#                     "Female %",
#                     help="The percentage of times this name was recorded as female.",
#                     format="%.1f%%",
#                     min_value=0,
#                     max_value=100,
#                 ),
#                 "Male %": st.column_config.ProgressColumn(
#                     "Male %",
#                     help="The percentage of times this name was recorded as male.",
#                     format="%.1f%%",
#                     min_value=0,
#                     max_value=100,
#                 ),
#                 "Neutrality %": st.column_config.ProgressColumn(
#                     "Neutrality %",
#                     help="Double the percentage of the less common gender for this name.",
#                     format="%.1f%%",
#                     min_value=0,
#                     max_value=100,
#                 ),
                
#             },
#             use_container_width=True,
#             hide_index=True
#         )

#     else:
#         st.write("No names with both Male and Female entries found in the dataset.")


# pages/1_Name_Explorer.py
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
    page_title="Name Explorer",
    page_icon=None,
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

    /* Custom styling for the multiselect in Tab 2 */
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #800000 !important; /* Maroon border */
        border-radius: 8px;
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


st.title("Name Explorer")
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


def build_static_country_map(geojson_obj: dict, selected_countries: List[str]):
    """
    Creates a non-interactive map to display selected countries.
    It highlights selected countries and shows the rest in a neutral color.
    """
    # Get all country names from the GeoJSON to draw the base map
    all_geojson_countries = [
        feature['properties']['name'] for feature in geojson_obj['features']
        if 'name' in feature.get('properties', {})
    ]

    # Convert selected country names to the format used in GeoJSON
    selected_geo_names = [map_country_to_geojson_name(
        c) for c in selected_countries]

    fig = go.Figure()

    # Base layer: all countries in a neutral gray
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_obj,
        locations=all_geojson_countries,
        z=[0] * len(all_geojson_countries),  # Dummy data for a single color
        featureidkey="properties.name",
        colorscale=[[0, '#EAEBF0'], [1, '#EAEBF0']],  # Neutral light gray
        showscale=False,
        hoverinfo='skip',  # No hover info for the base layer
        marker_opacity=1,
        marker_line_width=0.5,
    ))

    # Highlight layer: selected countries in the primary app color
    if selected_geo_names:
        fig.add_trace(go.Choroplethmapbox(
            geojson=geojson_obj,
            locations=selected_geo_names,
            z=[1] * len(selected_geo_names),  # Dummy data for a single color
            featureidkey="properties.name",
            colorscale=[[0, '#4F8BF9'], [1, '#4F8BF9']],  # Primary blue
            showscale=False,
            hoverinfo='location',  # Show country name on hover
            hovertemplate="<b>%{location}</b><extra></extra>",
            marker_opacity=1,
            marker_line_width=1,
            marker_line_color='#262730',
        ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=0.8,
        mapbox_center={"lat": 40, "lon": 10},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=False,
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


@st.cache_data(show_spinner=False)
def get_name_analysis(name: str):
    """Calls the Gemini API to get a full analysis of a name."""
    api_key = st.secrets.get("GEMINI_API")
    if not api_key:
        return None  # Don't show st.error here, handle it in the UI.
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
        clean_response = response.text.strip().replace(
            "```json", "").replace("```", "")
        return json.loads(clean_response)
    except Exception as e:
        print(f"Gemini API Error: {e}")  # Log for debugging
        return None


# =============================================================================
# TABS FOR DIFFERENT FUNCTIONALITIES
# =============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Geographical Explorer", "Local Trends", "Cross-Cultural Names", "Gender Neutral Names"
])

# =============================================================================
# TAB 1: GEOGRAPHICAL NAME EXPLORATION (REDESIGNED)
# =============================================================================
with tab1:
    left_col, mid_col, right_col = st.columns([1.3, 3, 1.3])

    with left_col:
        st.markdown('<h2 class="geographical-title">Search Names</h2>',
                    unsafe_allow_html=True)
        # Use a form to prevent rerunning on every keystroke, which caused crashes.
        with st.form(key="name_search_form"):
            name_query = st.text_input(
                value='Aria',
                label="SEARCH",
                placeholder="Search names (e.g., Maria, Alex)",
                label_visibility="collapsed"
            )
            search_button = st.form_submit_button("Search")

        st.markdown(
            '<div class="info-box"><h3>HOW TO USE</h3>Search for one or more names (comma-separated) to see popularity hotspots on the map. The first name in your search will be analyzed by our AI below.</div>', unsafe_allow_html=True)

    search_data = None
    # Only perform the search when the form is submitted
    if search_button and name_query:
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

            # --- MEMORY OPTIMIZATION START ---
            all_plot_countries = dominant_name_df["geojson_name"].unique()
            filtered_geojson = {
                "type": "FeatureCollection",
                "features": [
                    feature for feature in geojson["features"]
                    if feature.get("properties", {}).get("name") in all_plot_countries
                ]
            }
            # --- MEMORY OPTIMIZATION END ---

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
                    geojson=filtered_geojson,
                    locations=dominant_countries_for_name["geojson_name"],
                    z=dominant_countries_for_name["count"],
                    featureidkey="properties.name", colorscale=color_scale,
                    colorbar=dict(title=f"{name_capitalized}", x=1.02, xanchor="left",
                                  len=colorbar_len, y=y_pos, yanchor="top", tickfont=dict(color='black')),
                    marker_opacity=0.8, marker_line_width=0,
                    hovertemplate=f"<b>Country:</b> %{{location}}<br><b>Dominant:</b> {name_capitalized}<br><b>Count:</b> %{{z}}<extra></extra>"
                ))
            fig_map.update_layout(
                mapbox_style="carto-positron", mapbox_zoom=1, mapbox_center={"lat": 40, "lon": 10},
                margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False, height=620,
                paper_bgcolor='#F0F2F6',
                plot_bgcolor='#F0F2F6'
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            # Show a warning only if a search was attempted and failed
            if search_button and name_query:
                st.warning(
                    f"No data found for '{name_query}'. Please try another name.")
            st.markdown(
                f"<div class='map-placeholder'>Search for a name to view the global distribution map.</div>", unsafe_allow_html=True)

    with right_col:
        if search_data is not None and not search_data.empty:
            gender_dist = search_data.groupby(
                "gender")["count"].sum().reset_index()
            fig_pie = px.pie(gender_dist, values="count", names="gender",
                             title="Gender Distribution",
                             color_discrete_map={"F": "#FFB6C1", "M": "#87CEFA", "U": "#D3D3D3"})
            fig_pie.update_layout(
                margin=dict(l=10, r=10, t=35, b=10),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font_size=18,
                title_x=0.05,
            )
            fig_pie.update_traces(
                textposition="inside", textinfo="percent+label", textfont_color='black')
            st.plotly_chart(fig_pie, use_container_width=True,
                            config={'displayModeBar': False})
        else:
            st.markdown(
                '<div class="card-title">Gender Distribution</div>', unsafe_allow_html=True)
            st.markdown(
                "<div class='placeholder-text'>Search for a name to see gender data.</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="card-title">Top Countries by Count</div>', unsafe_allow_html=True)
        if search_data is not None and not search_data.empty:
            total_counts_by_country = search_data.groupby(
                "country")["count"].sum().sort_values(ascending=False).reset_index()
            st.dataframe(total_counts_by_country.head(10),
                         use_container_width=True,
                         hide_index=True)
        else:
            st.markdown(
                "<div class='placeholder-text'>Search for a name to see country data.</div>", unsafe_allow_html=True)

    # --- AI ANALYSIS SECTION ---
    st.divider()
    st.markdown('<h2 class="geographical-title">AI-Powered Name Analysis</h2>',
                unsafe_allow_html=True)

    if search_button and name_query:
        first_name_to_analyze = name_query.split(",")[0].strip().title()

        if "GEMINI_API" not in st.secrets:
            st.error(
                "Google API Key not found. Please add it to your Streamlit secrets (`.streamlit/secrets.toml`) to use this feature.")
        else:
            with st.spinner(f"Asking Gemini AI about '{first_name_to_analyze}'..."):
                analysis = get_name_analysis(first_name_to_analyze)

            if analysis:
                st.subheader(f"Analysis of '{first_name_to_analyze}'")
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
                st.error(
                    f"Could not retrieve AI analysis for '{first_name_to_analyze}'. This may be a temporary API issue.")
    else:
        st.info("Search for a name above to see the AI analysis.")


# =============================================================================
# TAB 2: LOCAL NAMING TRENDS [SIMPLIFIED & STABLE]
# =============================================================================
with tab2:
    st.header("Discover Local Naming Trends")
    st.markdown(
        "Use the dropdown to select countries and see them highlighted on the map. The charts below will update to show trends for your selection."
    )

    control_col, map_col = st.columns([1, 1.5])

    with control_col:
        available_countries = sorted(names_df["country"].unique())
        selected_countries = st.multiselect(
            "Select countries to explore:",
            available_countries,
            default=["Sweden", "Japan"],
            key="local_trends_countries",
        )

    with map_col:
        # Build and display the lightweight, non-interactive map
        static_map_fig = build_static_country_map(geojson, selected_countries)
        st.plotly_chart(static_map_fig, use_container_width=True,
                        config={'displayModeBar': False})

    st.divider()

    if not selected_countries:
        st.info(
            "Please select one or more countries from the dropdown to see local trends.")

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

    else:  # This block handles multiple selected countries
        num_countries = len(selected_countries)
        st.markdown(
            f"### Cross-examining Names Across **{num_countries}** Countries")
        st.write(
            f"Showing names that exist in all selected countries: {', '.join(selected_countries)}")

        first_names_filtered = names_df[names_df['country'].isin(
            selected_countries)]
        name_counts_per_country = first_names_filtered.groupby('name')[
            'country'].nunique()
        common_first_names_list = name_counts_per_country[name_counts_per_country ==
                                                          num_countries].index
        common_first_names_df = first_names_filtered[first_names_filtered['name'].isin(
            common_first_names_list)]

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
    st.header("Names Spanning Multiple Cultures")
    st.markdown(
        "Discover names that are common in many distinct regions. Use the search bar below to filter the list.")

    widespread_names = names_df.groupby(
        "name")["country"].nunique().sort_values(ascending=False)
    widespread_names_df = widespread_names.reset_index().rename(
        columns={"country": "country_count"})

    name_search_query = st.text_input(
        "Search for a name in the list:", "", placeholder="e.g. Maria")

    if name_search_query:
        display_df = widespread_names_df[widespread_names_df['name'].str.contains(
            name_search_query, case=False, na=False)]
    else:
        display_df = widespread_names_df

    st.write("Geographically widespread names:")
    st.dataframe(display_df, use_container_width=True, hide_index=True,
                 column_config={"name": "Name", "country_count": st.column_config.ProgressColumn("Number of Countries", format="%d", min_value=0, max_value=int(widespread_names_df["country_count"].max()))})


with tab4:
    st.header("Gender-Neutral Name Finder")
    st.markdown(
        "Discover names with a close to 50/50 gender split in our dataset. Sort by gender-neutrality to find the most balanced names."
    )

    # Find names that appear for both Male and Female
    mf_names_df = names_df[names_df['gender'].isin(['M', 'F'])]
    name_gender_counts = mf_names_df.groupby('name')['gender'].nunique()
    neutral_name_list = name_gender_counts[name_gender_counts > 1].index

    if not neutral_name_list.empty:
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
        # Neutrality: sum of both percentages (double the percentage of the minority group)
        gender_pivot['neutrality %'] = 2 * \
            gender_pivot[['female %', 'male %']].min(axis=1)
        # Score: distance from perfect 50/50 split
        gender_pivot['neutrality_score'] = abs(gender_pivot['female %'] - 50)

        # Prepare final dataframe for display
        display_df = gender_pivot.reset_index()[[
            'name', 'count', 'female %', 'male %', 'neutrality %'
        ]]

        display_df.rename(columns={
            'name': 'Name',
            'count': 'Total Count',
            'female %': 'Female %',
            'male %': 'Male %',
            'neutrality %': 'Neutrality %',
        }, inplace=True)

        display_df = display_df[[
            'Name', 'Total Count', 'Female %', 'Male %', 'Neutrality %']]

        # Show top 10 most neutral names by default
        default_display_df = display_df.sort_values(
            'Neutrality %', ascending=False).head()

        num_names_to_show = st.slider(
            "How many names to display?",
            min_value=10,
            max_value=len(display_df),
            value=10,
            step=10,
            key="neutral_names_slider"
        )

        st.dataframe(
            display_df.sort_values(
                'Neutrality %', ascending=False).head(num_names_to_show),
            column_config={
                "Name": st.column_config.TextColumn("Name"),
                "Total Count": st.column_config.NumberColumn("Total Count", format="%d"),
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
                "Neutrality %": st.column_config.ProgressColumn(
                    "Neutrality %",
                    help="Double the percentage of the less common gender for this name.",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),

            },
            use_container_width=True,
            hide_index=True
        )

    else:
        st.write("No names with both Male and Female entries found in the dataset.")
