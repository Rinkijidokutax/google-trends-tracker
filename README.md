# Google Trends Tracker

## Overview
A comprehensive tool for tracking and analyzing Google Trends data, focusing on top keywords, demographic insights, and trend analysis.

## Features
- Fetch top keywords across multiple regions
- Analyze demographic trends
- Generate comprehensive reports
- Visualize keyword interest

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Rinkijidokutax/google-trends-tracker.git
cd google-trends-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Trends Fetcher
```bash
python src/advanced_trends_fetcher.py
```

### Customizing Keywords and Regions
Modify the `main()` function in `advanced_trends_fetcher.py` to:
- Change regions
- Add custom keywords
- Adjust timeframes

## Output
The script generates:
- CSV files with top keywords
- Regional interest visualizations
- Time series data
- Summary reports

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## License
MIT License