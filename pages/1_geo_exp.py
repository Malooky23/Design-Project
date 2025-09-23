# pages/1_geo_exp.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pages.utils import load_data, get_geojson
import colorsys  # Import colorsys for color manipulation

# =============================================================================
# GEOGRAPHICAL NAME EXPLORATION PAGE
# =============================================================================
# This page allows users to explore the geographical distribution of names
# across different countries using interactive maps and visualizations.
#
# Features:
# - Interactive world map showing name popularity by country
# - Search functionality for multiple names simultaneously
# - Gender distribution analysis for searched names
# - Top countries ranking by name count
# - Dynamic color coding for different names on the map
# =============================================================================


# =============================================================================
# DATA LOADING AND CONFIGURATION
# =============================================================================

# Load the processed name data from CSV files
# names_df: Contains name, gender, country, count, latitude, and longitude data
# The other return values (meanings_df, last_names_df) are not used in this page
names_df, _, _ = load_data()

# Load GeoJSON data for country boundaries to enable choropleth mapping
geojson = get_geojson()

# Configure the Streamlit page layout and metadata
st.set_page_config(page_title="Geographical Explorer",
                   page_icon="🌍", layout="wide")


# Helper function to lighten a hex color
def lighten_hex_color(hex_color, factor=0.5):
    """
    Lightens a hex color by a given factor.
    Factor 0.0 means original color, 1.0 means pure white.
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Convert RGB (0-255) to HLS (0-1.0)
    h, l, s = colorsys.rgb_to_hls(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)

    # Increase lightness, capping at 1.0 (pure white)
    l = min(1.0, l + (1.0 - l) * factor)

    # Convert back to RGB (0-1.0), then to 0-255
    r, g, b = (int(x*255) for x in colorsys.hls_to_rgb(h, l, s))

    # Return as hex string
    return f'#{r:02x}{g:02x}{b:02x}'


# =============================================================================
# PAGE HEADER AND DESCRIPTION
# =============================================================================

st.title("🗺️ Geographical Name Exploration")
st.markdown(
    "Search for one or more names to see its popularity hotspots on the map. "
    "This tool visualizes name distribution patterns across countries and provides "
    "insights into cultural and geographical naming trends."
)

# =============================================================================
# USER INPUT SECTION
# =============================================================================

# Create a text input for users to search for names
# Supports multiple names separated by commas (e.g., "Maria, Mohammed, Alex")
name_query = st.text_input(
    "Search for one or more names, comma-separated (e.g., Maria, Mohammed, Alex):",
    "",
    help="Enter one or more names to see their global distribution. "
         "Names are case-insensitive and will be automatically capitalized."
)

# =============================================================================
# MAIN APPLICATION LOGIC - DUAL MODE INTERFACE
# =============================================================================
# The application operates in two modes:
# 1. SEARCH MODE: When user enters name(s) - shows detailed analysis
# 2. DEFAULT MODE: When no input - shows empty world map
# =============================================================================

if name_query:
    # =============================================================================
    # MODE 1: NAME SEARCH AND ANALYSIS
    # =============================================================================

    # Parse the input: split by commas, remove whitespace, filter empty strings
    name_queries = [name.strip()
                    for name in name_query.split(",") if name.strip()]

    # Convert to lowercase for case-insensitive matching
    lower_case_names = [name.lower() for name in name_queries]

    # Filter the dataset to include only the searched names
    # Using case-insensitive comparison to match user input with data
    search_data = names_df[names_df["name"].str.lower().isin(lower_case_names)]

    # =============================================================================
    # ERROR HANDLING - NO DATA FOUND
    # =============================================================================
    if search_data.empty:
        st.warning(
            f"No data found for the names '{name_query}'. Please try another name.")
    else:
        # =============================================================================
        # DATA PREPARATION FOR VISUALIZATION
        # =============================================================================

        # Create a list of properly capitalized names that were found in the data
        capitalized_names_found = sorted(
            [name.capitalize()
             for name in search_data["name"].str.lower().unique()]
        )

        # Display the header with the names that were actually found
        st.header(
            f"Popularity Hotspots for: {', '.join(capitalized_names_found)}")

        # =============================================================================
        # DOMINANT NAME CALCULATION
        # =============================================================================
        # For each country, find which of the searched names is most popular
        # This prevents overlapping on the map when multiple names exist in same country

        # Group by country and name, sum the counts for each combination
        country_name_counts = (
            search_data.groupby(["country", "name"], observed=True)[
                "count"].sum().reset_index()
        )

        # For each country, find the name with the highest count
        # This gives us the "dominant" name per country for cleaner visualization
        dominant_name_df = country_name_counts.loc[
            country_name_counts.groupby("country", observed=True)[
                "count"].idxmax()
        ].copy()

        # =============================================================================
        # GEOJSON COUNTRY NAME MAPPING
        # =============================================================================
        # Map our standardized country names to the names used in the GeoJSON file
        # This is necessary because GeoJSON files may use different naming conventions
        country_name_map = {
            "USA": "United States of America",  # Corrected mapping for USA
            "UK": "United Kingdom",            # Corrected mapping for UK
            "Russia": "Russian Federation",
            # Add more mappings as needed for proper choropleth display
            # A full list of GeoJSON country names can be found by inspecting the geojson object
            # For example: print([feature['properties']['name'] for feature in geojson['features']])
        }
        dominant_name_df["geojson_name"] = dominant_name_df["country"].replace(
            country_name_map
        )

        # =============================================================================
        # COLOR SCHEME SETUP
        # =============================================================================
        # Create a consistent color mapping for different names
        # Each unique name gets assigned a distinct color from Plotly's palette
        unique_names_found = sorted(
            list(dominant_name_df["name"].str.lower().unique())
        )
        colors = px.colors.qualitative.Plotly
        name_color_map = {
            name: colors[i % len(colors)] for i, name in enumerate(unique_names_found)
        }

        # =============================================================================
        # CHOROPLETH MAP CREATION
        # =============================================================================
        # Create the main interactive map showing name distribution by country

        fig = go.Figure()

        # Calculate layout parameters for multiple color bars
        # When showing multiple names, each gets its own color bar on the right side
        num_names = len(unique_names_found)
        gap = 0.05 if num_names > 1 else 0  # Gap between color bars
        total_space = 0.8  # Total vertical space for color bars
        colorbar_len = (
            (total_space - (num_names - 1) * gap) /
            num_names if num_names > 0 else 0
        )
        y_top = 0.9  # Top position for the first color bar

        # Create a separate choropleth layer for each unique name
        for i, name_lower in enumerate(unique_names_found):
            name_capitalized = name_lower.capitalize()

            # Get data for countries where this name is dominant
            dominant_countries_for_name = dominant_name_df[
                dominant_name_df["name"].str.lower() == name_lower
            ]

            if dominant_countries_for_name.empty:
                continue  # Skip if no countries for this name

            base_color_hex = name_color_map[name_lower]

            # Generate a sequential color scale based on the base color
            # Starts with a very light version, progresses through a medium version,
            # and ends with the full base color. This creates a smoother "heatmap" effect.
            lighter_color = lighten_hex_color(
                base_color_hex, 0.7)  # Very light tint
            medium_color = lighten_hex_color(
                base_color_hex, 0.3)  # Moderately light tint

            color_scale = [
                # Start with the lightest tint of the base color
                [0.0, lighter_color],
                [0.5, medium_color],    # Mid-point with a medium tint
                [1.0, base_color_hex]   # End with the full base color
            ]

            # Calculate position for this name's color bar
            y_pos = y_top - i * (colorbar_len + gap)

            # Create custom hover template for better user experience
            hovertemplate = f"<b>Country:</b> %{{location}}<br><b>Dominant Name:</b> {name_capitalized}<br><b>Count:</b> %{{z}}<extra></extra>"

            # Add the choropleth trace for this name
            fig.add_trace(
                go.Choroplethmap(
                    geojson=geojson,  # Country boundary data
                    # Country identifiers
                    locations=dominant_countries_for_name["geojson_name"],
                    # Values to color-code
                    z=dominant_countries_for_name["count"],
                    featureidkey="properties.name",  # Key in GeoJSON for country names
                    colorscale=color_scale,  # Custom sequential color mapping
                    colorbar=dict(
                        title=f"{name_capitalized}<br>Count",
                        x=1.02,  # Position to the right of the map
                        xanchor="left",
                        len=colorbar_len,  # Height of color bar
                        y=y_pos,  # Vertical position
                        yanchor="top",
                    ),
                    marker_opacity=0.8,  # Slight transparency for better visuals
                    marker_line_width=0,  # No country border lines
                    hovertemplate=hovertemplate,
                    hoverinfo="all",
                )
            )

        # =============================================================================
        # MAP LAYOUT CONFIGURATION
        # =============================================================================
        # Configure the overall appearance and behavior of the map
        fig.update_layout(
            mapbox_style="carto-positron",  # Clean, minimal map style
            mapbox_zoom=1,  # World view zoom level
            mapbox_center={"lat": 25, "lon": 20},  # Center on Africa/Europe
            # Remove margins for full width
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            showlegend=False,  # Disable legend (using color bars instead)
        )

        # Display the interactive map
        st.plotly_chart(fig, width='stretch')

        # Add visual separator
        st.divider()

        # =============================================================================
        # INSIGHTS AND ANALYTICS SECTION
        # =============================================================================
        # Provide additional statistical insights about the searched names

        st.header("Insights for Searched Names")

        # Create two columns for side-by-side display of different analytics
        col1, col2 = st.columns(2)

        # =============================================================================
        # LEFT COLUMN: GENDER DISTRIBUTION ANALYSIS
        # =============================================================================
        with col1:
            st.subheader("Gender Distribution")

            # Aggregate counts by gender across all searched names and countries
            # This shows the overall gender breakdown for the searched names
            gender_dist = search_data.groupby(
                "gender")["count"].sum().reset_index()

            if not gender_dist.empty:
                # Create an interactive pie chart showing gender distribution
                fig_pie = px.pie(
                    gender_dist,
                    values="count",
                    names="gender",
                    title="Gender Distribution Across All Countries",
                    # Use intuitive colors: pink for female, blue for male, gray for unspecified
                    color_discrete_map={"F": "lightpink",
                                        "M": "lightblue", "U": "lightgray"},
                )

                # Customize the pie chart appearance
                fig_pie.update_traces(
                    textposition="inside",  # Place labels inside pie slices
                    textinfo="percent+label"  # Show both percentage and gender label
                )
                st.plotly_chart(fig_pie, width='stretch')
            else:
                st.write("No gender distribution data available.")

        # =============================================================================
        # RIGHT COLUMN: TOP COUNTRIES ANALYSIS
        # =============================================================================
        with col2:
            st.subheader("Top Countries by Count")

            # Calculate total name counts per country across all searched names
            # This identifies which countries have the highest concentration of these names
            total_counts_by_country = (
                search_data.groupby("country")["count"]
                .sum()
                .sort_values(ascending=False)  # Sort from highest to lowest
                .reset_index()
            )

            if not total_counts_by_country.empty:
                # Create a horizontal bar chart showing top 10 countries
                fig_dist = px.bar(
                    total_counts_by_country.head(10).sort_values(
                        by="count", ascending=True),
                    y="country",
                    x="count",
                    orientation='h',
                    title="Top 10 Countries by Total Name Count",
                    labels={"count": "Total Count", "country": "Country"},
                )

                st.plotly_chart(fig_dist, width='stretch')
            else:
                st.write("No country distribution data available.")
else:
    # =============================================================================
    # MODE 2: DEFAULT VIEW - EMPTY WORLD MAP
    # =============================================================================
    # When no search query is entered, show a basic world map as a starting point

    st.header("Global Map")
    st.markdown(
        "👆 **Enter a name above to start exploring!** "
        "The map will show the global distribution and popularity of your searched names."
    )

    # Create a simple, empty world map for visual appeal
    # fig = go.Figure(go.Scattermapbox())
    fig = go.Figure(go.Scattermap())
    fig.update_layout(
        mapbox_style="open-street-map",  # Use OpenStreetMap style for default view
        mapbox_center={"lat": 25, "lon": 20},  # Center on Africa/Europe
        mapbox_zoom=2,  # Slightly more zoomed in than search results
        margin={"r": 0, "t": 0, "l": 0, "b": 0},  # Full width display
    )
    st.plotly_chart(fig, width='stretch')

# =============================================================================
# END OF APPLICATION
# =============================================================================
