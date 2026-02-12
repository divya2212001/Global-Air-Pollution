# Global Air Quality Dashboard – Continental Analysis
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit.components.v1 import html
import matplotlib.pyplot as plt

from config import (
    DATA_FILE,
    MAP_DEFAULT_LOCATION,
    MAP_DEFAULT_ZOOM,
    MAP_SAMPLE_SIZE,
    DEFAULT_N_CLUSTERS,
    WHO_PM25_ANNUAL_UGM3,
    WHO_PM10_ANNUAL_UGM3,
    PROJECT_ROOT,
)
from data_loading import load_data
from cleaning import clean_raw_data
from visualizations import (
    plot_value_histogram,
    plot_pollutant_frequency,
    plot_continent_heatmap,
    plot_correlation_heatmap,
    plot_time_series,
    plot_anomaly_days,
    fig_to_png_bytes,
)
from clustering import (
    build_location_pivot,
    fit_kmeans_with_metrics,
    elbow_silhouette_scores,
    plot_elbow_and_silhouette,
    fit_pca,
    plot_cluster_scatter,
    plot_pca_scatter,
)

st.set_page_config(page_title="Global Air Quality Dashboard", layout="wide")
st.title("Global Air Quality - Continental Analysis")

# Sidebar: About & Filters
with st.sidebar:
    st.header("About / Methodology")
    st.markdown("""
    **Data source:** OpenAQ (air quality measurements worldwide).  
    **Continents:** Mapped from country names via `pycountry` and `pycountry-convert`.  
    **Clustering:** K-Means on standardized pollutant levels per location; PCA for 2D visualization.  
    **Health metrics:** WHO annual guidelines (PM2.5 ≤ 5 µg/m³, PM10 ≤ 15 µg/m³).
    """)
    st.divider()
    st.header("Filters")
    st.caption("Apply filters to narrow the dataset used in charts and map.")

# Load and clean once
@st.cache_data
def get_cleaned_data():
    raw = load_data()
    return clean_raw_data(raw)

df_raw = load_data()
df = get_cleaned_data()

if df.empty:
    st.error("No data left after cleaning & continent mapping.")
    st.stop()

# Filters (apply to df for visualizations)
continents = sorted(df["Continent"].unique().tolist())
countries = sorted(df["Country Label"].unique().tolist())
pollutants = sorted(df["Pollutant"].unique().tolist())

with st.sidebar:
    selected_continents = st.multiselect("Continent", options=continents, default=continents)
    selected_countries = st.multiselect("Country", options=countries, default=[], key="country_filter")
    selected_pollutants = st.multiselect("Pollutant", options=pollutants, default=pollutants)

# Apply filters
filtered = df[
    df["Continent"].isin(selected_continents) &
    df["Pollutant"].isin(selected_pollutants)
].copy()
if selected_countries:
    filtered = filtered[filtered["Country Label"].isin(selected_countries)]

# Use filtered for all downstream; fallback to df if empty
display_df = filtered if not filtered.empty else df

st.subheader("Raw Data Preview")
st.dataframe(df_raw.head())

st.subheader("Cleaned Data (after filters)")
st.dataframe(display_df.head())
st.caption(f"Rows: {len(display_df):,} | Missing: {display_df.isnull().sum().to_string()}")

# ---- Health metrics: days above WHO ----
st.subheader("Health metrics – exposure above WHO guidelines")
st.caption("Share of locations (or country-continent pairs) with mean above WHO annual guideline.")

who_pm25 = display_df[display_df["Pollutant"] == "PM2.5"]
who_pm10 = display_df[display_df["Pollutant"] == "PM10"]
if not who_pm25.empty:
    above_pm25 = (who_pm25.groupby(["Country Label", "Continent"])["Value"].mean() > WHO_PM25_ANNUAL_UGM3).mean() * 100
    st.metric("Locations with mean PM2.5 above WHO (5 µg/m³)", f"{above_pm25:.1f}%")
if not who_pm10.empty:
    above_pm10 = (who_pm10.groupby(["Country Label", "Continent"])["Value"].mean() > WHO_PM10_ANNUAL_UGM3).mean() * 100
    st.metric("Locations with mean PM10 above WHO (15 µg/m³)", f"{above_pm10:.1f}%")

# Visualizations
st.subheader("Pollution Value Distribution")
fig = plot_value_histogram(display_df)
st.pyplot(fig)
plt.close(fig)

st.subheader("Pollutant Frequency")
fig = plot_pollutant_frequency(display_df)
if fig is not None:
    st.pyplot(fig)
    plt.close(fig)
else:
    st.warning("No pollutant data available.")

st.subheader("Average Pollutant Levels by Continent")
continent_group = (
    display_df.groupby(["Continent", "Pollutant"])["Value"]
    .mean()
    .unstack()
)
fig = plot_continent_heatmap(continent_group)
if fig is not None:
    st.pyplot(fig)
    plt.close(fig)
else:
    st.warning("Not enough data for heatmap.")

st.subheader("Correlation Between Pollutants")
if continent_group.shape[1] >= 2:
    corr_matrix = continent_group.corr()
    fig = plot_correlation_heatmap(corr_matrix)
    if fig is not None:
        st.pyplot(fig)
        plt.close(fig)
else:
    st.warning("Need at least two pollutants for correlation.")

# Time series
if "Date" in display_df.columns:
    st.subheader("Time series – pollution over time")
    ts_group = st.selectbox("Group time series by", ["None", "Continent", "Country Label"], key="ts_group")
    group_col = None if ts_group == "None" else ts_group
    fig = plot_time_series(
        display_df,
        date_col="Date",
        value_col="Value",
        group_col=group_col,
        title="Mean pollution over time",
    )
    if fig is not None:
        st.pyplot(fig)
        plt.close(fig)

# Anomaly detection
if "Date" in display_df.columns:
    st.subheader("Anomaly detection – high pollution days")
    daily = display_df.groupby("Date")["Value"].mean()
    if len(daily) > 10:
        fig = plot_anomaly_days(daily, threshold_quantile=0.95)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.caption("Not enough daily data for anomaly plot.")

# Clustering 
st.subheader("K-Means clustering")
pivot = build_location_pivot(display_df)

if pivot.shape[0] < 4:
    st.warning("Not enough data points for clustering.")
else:
    n_clusters = st.slider("Number of clusters", min_value=2, max_value=10, value=DEFAULT_N_CLUSTERS, key="n_clusters")
    pivot_clustered, scaled, scaler, kmeans = fit_kmeans_with_metrics(pivot, n_clusters=n_clusters)

    # Elbow & silhouette
    k_range = range(2, min(11, pivot.shape[0]))
    fig = plot_elbow_and_silhouette(pivot, k_range=k_range)
    st.pyplot(fig)
    plt.close(fig)

    feature_cols = [c for c in pivot.columns if c != "Cluster"]
    if len(feature_cols) >= 2:
        x_col, y_col = feature_cols[0], feature_cols[1]
        fig = plot_cluster_scatter(pivot_clustered, x_col, y_col, log_scale=True)
        st.pyplot(fig)
        plt.close(fig)

    # PCA
    if pivot.shape[1] >= 2:
        pc_vals, pca = fit_pca(scaled, n_components=2)
        pivot_clustered = pivot_clustered.copy()
        pivot_clustered["PC1"] = pc_vals[:, 0]
        pivot_clustered["PC2"] = pc_vals[:, 1]
        fig = plot_pca_scatter(pivot_clustered)
        st.pyplot(fig)
        plt.close(fig)
        st.caption(f"Explained variance ratio: {pca.explained_variance_ratio_}")

#  Map
st.subheader("Pollution map (sampled)")
if len(display_df) >= 10:
    sample_size = min(MAP_SAMPLE_SIZE, len(display_df))
    df_sample = display_df.sample(n=sample_size, random_state=42)
    m = folium.Map(location=MAP_DEFAULT_LOCATION, zoom_start=MAP_DEFAULT_ZOOM)
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df_sample.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            tooltip=f"{row['Pollutant']} = {row['Value']}",
        ).add_to(marker_cluster)
    map_path = PROJECT_ROOT / "map.html"
    m.save(str(map_path))
    with open(map_path, "r", encoding="utf-8") as f:
        html(f.read(), height=600)
else:
    st.warning("Not enough data points for map.")

# Export
st.subheader("Export")
col1, col2 = st.columns(2)
with col1:
    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download cleaned CSV", csv, "openaq_cleaned.csv", "text/csv", key="dl_csv")
with col2:
    st.caption("Export last chart as PNG (e.g. use browser screenshot or add a dedicated export button per chart).")
    # Export distribution chart as example
    fig = plot_value_histogram(display_df)
    png_bytes = fig_to_png_bytes(fig)
    plt.close(fig)
    st.download_button("Download distribution chart (PNG)", png_bytes, "pollution_distribution.png", "image/png", key="dl_png")
