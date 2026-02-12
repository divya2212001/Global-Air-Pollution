"""Charts and plots for air quality dashboard."""
import io
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LogNorm
import pandas as pd


def fig_to_png_bytes(fig: plt.Figure) -> bytes:
    """Save figure to PNG bytes for download."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    return buf.read()


def plot_value_histogram(df: pd.DataFrame, value_col: str = "Value", bins: int = 50) -> plt.Figure:
    """Distribution of pollution values (log scale)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df[value_col].dropna(), bins=bins)
    ax.set_yscale("log")
    ax.set_title("Distribution of Pollution Values (Log Scale)")
    return fig


def plot_pollutant_frequency(df: pd.DataFrame, pollutant_col: str = "Pollutant") -> Optional[plt.Figure]:
    """Bar chart of pollutant counts."""
    counts = df[pollutant_col].value_counts()
    if counts.empty:
        return None
    fig, ax = plt.subplots(figsize=(8, 5))
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Frequency of Pollutants")
    return fig


def plot_continent_heatmap(continent_group: pd.DataFrame) -> Optional[plt.Figure]:
    """Heatmap of average pollutant levels by continent."""
    if continent_group.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(continent_group, cmap="magma", norm=LogNorm(), ax=ax)
    ax.set_title("Average Pollutant Levels by Continent")
    return fig


def plot_correlation_heatmap(corr_matrix: pd.DataFrame) -> Optional[plt.Figure]:
    """Correlation matrix heatmap between pollutants."""
    if corr_matrix.empty or corr_matrix.shape[0] < 2:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlation Between Pollutants")
    return fig


def plot_time_series(
    df: pd.DataFrame,
    date_col: str = "Date",
    value_col: str = "Value",
    group_col: Optional[str] = None,
    title: str = "Pollution Over Time",
) -> Optional[plt.Figure]:
    """Time series of pollution. If group_col (e.g. Continent), one line per group (mean)."""
    if date_col not in df.columns or value_col not in df.columns:
        return None
    plot_df = df[[date_col, value_col]].copy()
    if group_col and group_col in df.columns:
        plot_df[group_col] = df[group_col]
        agg = plot_df.groupby([date_col, group_col])[value_col].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        for name, g in agg.groupby(group_col):
            g = g.sort_values(date_col)
            ax.plot(g[date_col], g[value_col], label=name, alpha=0.8)
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    else:
        agg = plot_df.groupby(date_col)[value_col].mean().reset_index().sort_values(date_col)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(agg[date_col], agg[value_col])
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig


def plot_anomaly_days(
    series: pd.Series,
    threshold_quantile: float = 0.95,
    title: str = "Anomaly Detection: High Pollution Days",
) -> plt.Figure:
    """Mark values above a quantile threshold as anomalies."""
    fig, ax = plt.subplots(figsize=(10, 4))
    threshold = series.quantile(threshold_quantile)
    ax.plot(series.index, series.values, color="steelblue", alpha=0.7, label="Daily mean")
    anomalies = series[series >= threshold]
    if not anomalies.empty:
        ax.scatter(anomalies.index, anomalies.values, color="red", s=30, zorder=5, label=f"Anomaly (≥ {threshold:.1f})")
    ax.axhline(threshold, color="red", linestyle="--", alpha=0.6, label=f"Threshold (p{int(threshold_quantile*100)})")
    ax.set_title(title)
    ax.legend()
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    return fig
