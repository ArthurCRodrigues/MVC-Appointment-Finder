# MVC-Appointment-Finder
![Build Status](https://github.com/ArthurCRodrigues/MVC-Appointment-Finder/actions/workflows/tests.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)



### This application helps you find an available appointment in New Jersey Motor Vehicle Commission (NJ-MVC) appointment wizard.
This is a python-based CLI application that continuously monitors and notifies users of available appointments within a specified date range.The project uses web scraping to retrieve real-time appointment data from a government website and filters the results based on user-defined parameters
## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [License](#license)

## Features 
- Scrapes appointment data from a website using `BeautifulSoup` and `requests`.
- Filters appointments based on user-defined date ranges.
- Sends desktop notifications for available appointments using `plyer`
- Command-line interface for easy configuration

## Technologies Used
- Python 3.8+
- BeautifulSoup for web scraping
- Requests for HTTP requests
- Plyer for desktop notifications
- Argparse for CLI interface

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/MVC-Appointment-Finder.git
    cd MVC-Appointment-Finder
    ```
2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate  # Windows
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python main.py --days 10 --interval 15
    ```
## Usage
The application takes two command-line arguments:

- `--days`: Number of days to search for available appointments (required).
- `--interval`: Time in seconds between each check (default is 10 seconds).

### Example:
```bash
python main.py --days 5 --interval 20
```
This will check for appointments within the next 5 days and notify you every 20 seconds if new slots are found

## Project Structure
- `main.py`: CLI interface that starts the continuous search process
- `model.py`: Defined the `Location` class and handles data validation
- `locationRetriever.py`: Contains the `LocationRetriever` class for scraping and parsing data and `Filter` class for filtering the available locations found in the previous class based on specified day range
- `searcher.py`: Implements the continuous search logic and sends desktop notifications
- `requirements.txt`: List of project dependencies

## Testing
This project includes unit tests for key components to ensure reliability and correct functionality.

### Running Tests
To run the tests, execute the following command:
```bash
python -m unittest discover tests
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Contact
Developed by Arthur(https://github.com/ArthurCRodrigues). Feel free to reach out for collaboration or questions.




