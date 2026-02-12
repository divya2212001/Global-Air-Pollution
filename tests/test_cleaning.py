"""Tests for cleaning and continent mapping."""
import pandas as pd
import pytest

from cleaning import (
    country_name_to_alpha2,
    country_to_continent,
    parse_coordinates,
    fill_missing_coordinates,
    clean_raw_data,
)


def test_country_name_to_alpha2():
    assert country_name_to_alpha2("Germany") == "DE"
    assert country_name_to_alpha2("United States") == "US"
    assert country_name_to_alpha2("India") == "IN"
    assert country_name_to_alpha2("Nonexistent Country XYZ") is None


def test_country_to_continent():
    assert country_to_continent("Germany") == "Europe"
    assert country_to_continent("United States") == "North America"
    assert country_to_continent("India") == "Asia"
    assert country_to_continent("Unknown Country XYZ") == "Unknown"


def test_parse_coordinates():
    df = pd.DataFrame({
        "Coordinates": ["45.1, -122.8", "6.25, -75.57"],
        "Country Label": ["US", "CO"],
        "Pollutant": ["PM2.5", "PM10"],
        "Value": [10.0, 20.0],
    })
    out = parse_coordinates(df)
    assert "Latitude" in out.columns and "Longitude" in out.columns
    assert out["Latitude"].iloc[0] == pytest.approx(45.1)
    assert out["Longitude"].iloc[0] == pytest.approx(-122.8)


def test_clean_raw_data_returns_continent_and_positive_values():
    raw = pd.DataFrame({
        "Country Label": ["United States", "Germany", "India"],
        "Pollutant": ["PM2.5", "PM2.5", "PM10"],
        "Value": [5.0, -1.0, 25.0],
        "Coordinates": ["40.0, -74.0", "52.5, 13.4", "28.6, 77.2"],
    })
    out = clean_raw_data(raw)
    assert not out.empty
    assert "Continent" in out.columns
    assert (out["Value"] >= 0).all()
    assert "Unknown" not in out["Continent"].values
