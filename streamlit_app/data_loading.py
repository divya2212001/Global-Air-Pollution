"""Load OpenAQ air quality data."""
import pandas as pd

from config import DATA_FILE


def load_data() -> pd.DataFrame:
    """Load raw OpenAQ CSV. Uses semicolon separator."""
    return pd.read_csv(DATA_FILE, sep=";")
