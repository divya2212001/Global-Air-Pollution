"""Tests for data loading."""
import pytest

from data_loading import load_data


def test_load_data_returns_dataframe():
    df = load_data()
    assert df is not None
    assert not df.empty


def test_load_data_has_expected_columns():
    df = load_data()
    expected = {"Country Label", "Pollutant", "Value", "Coordinates"}
    assert expected.issubset(set(df.columns))
