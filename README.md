# FilmAffinity Ratings Exporter

A Python script to export your FilmAffinity movie ratings and details to a CSV file. This tool helps you download your personal movie ratings data for offline use or data analysis.

## Attribution

This project is based on the original work by [@renefs](https://gist.github.com/renefs/a10a3e9f17b30edf431619ddcc629f2e). The code has been modified and enhanced for improved functionality and maintainability.

## Features

- Exports movie titles, years, user ratings, average ratings, directors, and actors
- Handles pagination automatically
- Exports data in CSV format
- Simple command-line interface

## Requirements

- Python 3.x
- Required Python packages:
  - requests
  - beautifulsoup4
  - lxml

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/scrap-filmaffinity.git
cd scrap-filmaffinity
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python export.py USER_ID
```

With custom output file:
```bash
python export.py USER_ID --csv output.csv
```

Replace `USER_ID` with your FilmAffinity user ID (you can find it in your profile URL).

## Output

The script generates a CSV file with the following columns:
- Title
- Year
- UserRating
- AvgRating
- Directors
- Actors

## Disclaimer

This tool is intended for **personal use only**. Its sole purpose is to help the user **download their own movie ratings** from FilmAffinity for offline use, data analysis, or personal projects.

This project is **not affiliated with, endorsed by, or associated with FilmAffinity** in any way.

Please respect the terms of service of FilmAffinity. Use this code responsibly and **only to access your own data**.

If you are a representative of FilmAffinity and have any concerns, feel free to open an issue or contact me for prompt removal or modification.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 