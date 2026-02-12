"""Configuration for Global Air Quality Dashboard."""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_FILE = DATA_DIR / "openaq.csv"  # OpenAQ export filename

# Clustering
DEFAULT_N_CLUSTERS = 4
CLUSTER_RANDOM_STATE = 42

# Map
MAP_DEFAULT_LOCATION = [20, 0]
MAP_DEFAULT_ZOOM = 2
MAP_SAMPLE_SIZE = 1000

# WHO annual guideline (µg/m³) for PM2.5 - used for health metrics
WHO_PM25_ANNUAL_UGM3 = 5.0
WHO_PM10_ANNUAL_UGM3 = 15.0
