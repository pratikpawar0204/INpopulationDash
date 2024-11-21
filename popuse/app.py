# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="India Population Dashboard",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load dataset
def load_data():
    return pd.read_csv("inpop - Sheet1.csv")

df = load_data()

# Ensure 'year' column exists
if 'year' not in df.columns:
    st.error("The 'year' column is missing from the dataset.")
else:
    # Sidebar configuration
    with st.sidebar:
        st.title("🌟India Population Dashboard")
        st.markdown("Explore India's population insights interactively!")

        # Available years from the dataset
        available_years = sorted(df['year'].unique())
        selected_year = st.select_slider(
            "Select Year", options=available_years, value=max(available_years)
        )

        # Color theme
        color_themes = ['viridis', 'plasma', 'cividis', 'blues', 'reds', 'turbo']
        selected_color_theme = st.selectbox("Color Theme", color_themes, index=0)

        # State selection
        states = sorted(df['Name'].unique())
        selected_state = st.selectbox("Select State", states)

        # Multi-selection for comparison
        selected_states = st.multiselect("Compare States", states, default=states[:3])

    # Main layout
    st.title("India's Population Dashboard")
    st.markdown("## 📊 Data Insights and Visualizations")

    # Filter data for selected year
    df_year = df[df['year'] == selected_year]

    # Metrics: Total and average population
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Population", f"{df_year['population'].sum():,}")
    with col2:
        st.metric("Average Population", f"{df_year['population'].mean():,.0f}")

    # Choropleth map: Full map of India
    st.markdown("### 🗺️ Population Distribution Across Indian States")
    fig_map = px.choropleth(
        df_year,
        geojson="https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson",
        featureidkey="properties.NAME_1",
        locations="Name",
        color="population",
        color_continuous_scale=selected_color_theme,
        labels={'population': 'Population'},
        title="Population Distribution Across States",
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, use_container_width=True)

    # Single state map
    st.markdown(f"### 🗺️ Population Map for {selected_state}")
    df_state = df[(df['Name'] == selected_state) & (df['year'] == selected_year)]
    if not df_state.empty:
        fig_state_map = px.choropleth(
            df_state,
            geojson="https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson",
            featureidkey="properties.NAME_1",
            locations="Name",
            color="population",
            color_continuous_scale=selected_color_theme,
            labels={'population': 'Population'},
            title=f"Population Map for {selected_state}",
        )
        fig_state_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_state_map, use_container_width=True)
    else:
        st.warning(f"No data available for {selected_state} in {selected_year}.")

    # Line chart: Population trend for selected state
    st.markdown(f"### 📈 Population Growth Over Time: {selected_state}")
    state_data = df[df['Name'] == selected_state]
    fig_line = px.line(
        state_data,
        x="year",
        y="population",
        title=f"Population Trend in {selected_state}",
        markers=True,
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Bar chart: Comparison of selected states
    st.markdown("### 📊 State-wise Population Comparison")
    df_comparison = df[(df['year'] == selected_year) & (df['Name'].isin(selected_states))]
    fig_bar = px.bar(
        df_comparison,
        x="Name",
        y="population",
        color="Name",
        title="Population Comparison",
        text="population",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # User guide section
    st.markdown("## 📖 User Guide")
    st.markdown(
        """
        - **Year Selector**: Choose a year to filter the data (e.g., 1951, 1961, ... 2011).
        - **State Selector**: Analyze trends for a specific state.
        - **Comparison Tool**: Compare multiple states for the selected year.
        - **Color Themes**: Personalize the map colors for better readability.
        - **Interactive Charts**: Hover over charts for detailed insights.
        """
    )
