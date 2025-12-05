# Global Air Pollution Analysis

A comprehensive analysis of global air pollution patterns across 23,463 cities in 175 countries, examining PM2.5, CO, Ozone, and NO2 pollutants.

## 🌍 Project Overview

This project analyzes global air quality data to:
- Identify pollution hotspots worldwide
- Understand relationships between different pollutants
- Provide data-driven insights for public health policy
- Generate actionable recommendations for interventions

## 📊 Key Findings

- **18.4%** of cities have concerning air quality levels (unhealthy or worse)
- **PM2.5** is the dominant pollutant with mean AQI of 68.52
- **South Asia** (India, Pakistan) faces the most severe challenges
- **2,556 cities** (10.9%) have concerning PM2.5 levels
- Moderate pollutant correlations suggest common emission sources
- **191 cities** in hazardous category requiring urgent intervention

## 🗂️ Dataset

- **Source:** Global Air Pollution Dataset
- **Size:** 23,463 records
- **Coverage:** 175 countries, 23,462 cities
- **Pollutants:** PM2.5, CO, Ozone, NO2
- **Download:** https://drive.google.com/file/d/1JUI96rqrpij1IhlplOq9Qpe2IMEv_iNc/view?usp=sharing

## 🛠️ Technologies Used

- **Python 3.12**
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Statistical Analysis:** SciPy
- **Environment:** Google Colab

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/divya2212001/Global-Air-Pollution.git
cd air-pollution-analysis
```

2. Install dependencies:
```bash
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0
scipy>=1.10.0
gdown>=4.7.0
```

3. Download the dataset:
```bash
# Using gdown
!gdown "https://drive.google.com/uc?id=1JUI96rqrpij1IhlplOq9Qpe2IMEv_iNc" -O "global air pollution dataset.csv"
```

## 📈 Visualizations

The analysis generates the following visualizations:

1. **AQI Distribution** - Global air quality category breakdown
2. **Top Polluted Cities** - 15 most polluted cities worldwide
3. **Country Rankings** - Countries ranked by mean AQI
4. **Pollutant Comparison** - Distribution of PM2.5, CO, Ozone, NO2
5. **PM2.5 Health Risk** - Category distribution pie chart
6. **Correlation Heatmap** - Relationships between pollutants

## 📊 Results Summary

### Global Air Quality Distribution
| Category | Percentage |
|----------|------------|
| Good | 42.3% |
| Moderate | 39.3% |
| Unhealthy for Sensitive | 6.8% |
| Unhealthy | 9.5% |
| Very Unhealthy | 1.2% |
| Hazardous | 0.8% |

### Most Polluted Regions
1. **South Asia** (India, Pakistan) - PM2.5 dominated
2. **Middle East** (Bahrain, UAE, Kuwait) - Multi-pollutant challenges
3. **East Asia** (Republic of Korea) - Highest mean AQI

### Pollutant Statistics
| Pollutant | Mean AQI | Max AQI | Std Dev |
|-----------|----------|---------|---------|
| PM2.5     | 68.52    | 500     | 54.80   |
| Ozone     | 35.19    | 235     | 28.10   |
| NO2       | 3.06     | 91      | 5.25    |
| CO        | 1.37     | 133     | 1.83    |

### Pollutant Correlations
- **CO ↔ NO2:** 0.488 (strongest - common combustion sources)
- **PM2.5 ↔ CO:** 0.439 (moderate - traffic/industrial)
- **PM2.5 ↔ Ozone:** 0.340 (weak - different mechanisms)

## 🎯 Recommendations

### Immediate Actions
1. Emergency interventions in 191 hazardous cities
2. Public health advisories for 2,556 high-PM2.5 cities
3. Enhanced monitoring in underrepresented regions (Africa, South America)

### Long-term Strategies
1. Integrated multi-pollutant control targeting common sources
2. Regional cooperation, especially in South Asia
3. Technology transfer to developing nations
4. Expansion of monitoring networks
5. Source-specific regulations (traffic, industry, agriculture)

## 🔬 Methodology

1. **Data Preprocessing:** Automated column detection, quality checks, validation
2. **Descriptive Statistics:** Mean, median, std dev for all pollutants
3. **Geographic Analysis:** City and country-level aggregations
4. **Correlation Analysis:** Pearson coefficients between pollutants
5. **Comparative Analysis:** Pollutant distributions and patterns

## 📄 Project Deliverables

- ✅ Data Analysis Code
- ✅ 15 Visualizations
- ✅ Statistical Reports (CSV)
- ✅ Presentation Slides
- ✅ Project Report (PDF)
- ✅ Video Presentation

## 👥 Team Members

Sneha Chepurwar
Shubhanshu Dubey
Divyanjali Gopisetty

## 📚 References

1. World Health Organization. (2021). *WHO Global Air Quality Guidelines.*
2. Global Air Pollution Dataset. Retrieved from Kaggle

**Note:** This project was completed as part of Applied Mathematics at Newton School of Technology.
