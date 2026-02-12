"""Data cleaning and continent mapping for OpenAQ data."""
from typing import Optional

import pandas as pd
import pycountry
import pycountry_convert as pc


def country_name_to_alpha2(country_name: str) -> Optional[str]:
    """Convert country name to ISO alpha-2 code."""
    try:
        return pycountry.countries.lookup(country_name).alpha_2
    except (LookupError, AttributeError, KeyError):
        return None


def country_to_continent(country_name: str) -> str:
    """Map country name to continent name."""
    try:
        alpha2 = country_name_to_alpha2(country_name)
        if alpha2 is None:
            return "Unknown"
        continent_code = pc.country_alpha2_to_continent_code(alpha2)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except (KeyError, AttributeError, TypeError):
        return "Unknown"


def parse_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse Latitude/Longitude from Coordinates column if missing."""
    if "Latitude" in df.columns and "Longitude" in df.columns:
        return df.copy()
    if "Coordinates" not in df.columns:
        return df.copy()
    out = df.copy()
    parts = out["Coordinates"].str.split(",", expand=True)
    out["Latitude"] = pd.to_numeric(parts[0], errors="coerce")
    out["Longitude"] = pd.to_numeric(parts[1], errors="coerce")
    return out


def fill_missing_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing lat/lon by country median, then global median."""
    out = df.copy()
    out["Latitude"] = out.groupby("Country Label")["Latitude"].transform(
        lambda x: x.fillna(x.median())
    )
    out["Longitude"] = out.groupby("Country Label")["Longitude"].transform(
        lambda x: x.fillna(x.median())
    )
    out["Latitude"] = out["Latitude"].fillna(out["Latitude"].median())
    out["Longitude"] = out["Longitude"].fillna(out["Longitude"].median())
    return out


def parse_last_updated(df: pd.DataFrame) -> pd.DataFrame:
    """Parse 'Last Updated' into datetime and date for time series."""
    out = df.copy()
    if "Last Updated" not in out.columns:
        return out
    out["Last Updated"] = pd.to_datetime(out["Last Updated"], errors="coerce")
    out["Date"] = out["Last Updated"].dt.date
    return out


def clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full cleaning pipeline: coordinates, keep Date/Last Updated, continents, clip values.
    Returns DataFrame with Country Label, Pollutant, Value, Latitude, Longitude, Continent, and optionally Date.
    """
    # Keep columns we need (including Last Updated for time series)
    cols = ["Country Label", "Pollutant", "Value", "Coordinates"]
    if "Last Updated" in df.columns:
        cols.append("Last Updated")
    available = [c for c in cols if c in df.columns]
    out = df[available].copy()

    out = parse_coordinates(out)
    out = fill_missing_coordinates(out)
    out = parse_last_updated(out)

    # Select and ensure required columns
    base_cols = ["Country Label", "Pollutant", "Value", "Latitude", "Longitude"]
    if "Date" in out.columns:
        base_cols.append("Date")
    if "Last Updated" in out.columns:
        base_cols.append("Last Updated")
    out = out[[c for c in base_cols if c in out.columns]]

    out["Continent"] = out["Country Label"].apply(country_to_continent)
    out = out[out["Continent"] != "Unknown"].copy()
    out["Value"] = out["Value"].clip(lower=0)

    # Drop rows with invalid values (e.g. sentinel -9999)
    out = out[out["Value"].notna()].copy()
    return out
