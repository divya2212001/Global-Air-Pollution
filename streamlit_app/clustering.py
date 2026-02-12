"""K-Means clustering and PCA for air quality locations."""
from typing import Tuple

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

import seaborn as sns
import matplotlib.pyplot as plt

from config import DEFAULT_N_CLUSTERS, CLUSTER_RANDOM_STATE


def build_location_pivot(
    df: pd.DataFrame,
    index_cols: Tuple[str, str] = ("Latitude", "Longitude"),
    columns_col: str = "Pollutant",
    value_col: str = "Value",
) -> pd.DataFrame:
    """Pivot to one row per location, columns = pollutants, values = mean."""
    pivot = df.pivot_table(
        index=list(index_cols),
        columns=columns_col,
        values=value_col,
        aggfunc="mean",
    ).fillna(0)
    return pivot


def fit_kmeans_with_metrics(
    pivot: pd.DataFrame,
    n_clusters: int = DEFAULT_N_CLUSTERS,
    random_state: int = CLUSTER_RANDOM_STATE,
) -> Tuple[pd.DataFrame, np.ndarray, StandardScaler, KMeans]:
    """
    Scale, fit KMeans, add Cluster column. Returns (pivot_with_cluster, scaled, scaler, kmeans).
    """
    scaler = StandardScaler()
    scaled = scaler.fit_transform(pivot)
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = kmeans.fit_predict(scaled)
    out = pivot.copy()
    out["Cluster"] = labels
    return out, scaled, scaler, kmeans


def elbow_silhouette_scores(
    pivot: pd.DataFrame,
    k_range: range = range(2, 11),
    random_state: int = CLUSTER_RANDOM_STATE,
) -> Tuple[list, list]:
    """Compute inertia and silhouette for each k. Returns (inertias, silhouettes)."""
    scaler = StandardScaler()
    scaled = scaler.fit_transform(pivot)
    inertias = []
    silhouettes = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = kmeans.fit_predict(scaled)
        inertias.append(kmeans.inertia_)
        if k >= 2 and len(np.unique(labels)) == k:
            silhouettes.append(silhouette_score(scaled, labels))
        else:
            silhouettes.append(np.nan)
    return inertias, silhouettes


def plot_elbow_and_silhouette(
    pivot: pd.DataFrame,
    k_range: range = range(2, 11),
    random_state: int = CLUSTER_RANDOM_STATE,
) -> plt.Figure:
    """Two subplots: elbow curve and silhouette score vs k."""
    inertias, silhouettes = elbow_silhouette_scores(pivot, k_range, random_state)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(k_range, inertias, "bo-")
    ax1.set_xlabel("Number of clusters (k)")
    ax1.set_ylabel("Inertia")
    ax1.set_title("Elbow Method")
    ax2.plot(k_range, silhouettes, "go-")
    ax2.set_xlabel("Number of clusters (k)")
    ax2.set_ylabel("Silhouette Score")
    ax2.set_title("Silhouette Score")
    plt.tight_layout()
    return fig


def fit_pca(scaled: np.ndarray, n_components: int = 2) -> Tuple[np.ndarray, PCA]:
    """Fit PCA and return transformed values and fitted PCA."""
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(scaled)
    return transformed, pca


def plot_cluster_scatter(
    pivot: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: str = "Cluster",
    log_scale: bool = False,
) -> plt.Figure:
    """Scatter plot colored by cluster."""
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.scatterplot(data=pivot, x=x_col, y=y_col, hue=hue_col, palette="tab10", ax=ax)
    if log_scale:
        ax.set_xscale("log")
        ax.set_yscale("log")
    ax.set_title("K-Means Clusters (Location × Pollutants)")
    return fig


def plot_pca_scatter(
    pivot: pd.DataFrame,
    pc1_col: str = "PC1",
    pc2_col: str = "PC2",
    hue_col: str = "Cluster",
) -> plt.Figure:
    """PCA 2D scatter colored by cluster."""
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=pivot, x=pc1_col, y=pc2_col, hue=hue_col, palette="tab10", ax=ax)
    ax.set_title("PCA Visualization of Locations")
    return fig
