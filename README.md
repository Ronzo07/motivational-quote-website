# Motivational Quote Website

## Features

1. Displays a motivational quote on the website homepage.
2. Automatically updates the quote daily at midnight.
3. Quotes are chosen based on the current day of the year.

## Built With

- HTML
- CSS
- Python, Flask

## Installation

1. Clone the repository:
    git clone https://github.com/ronzo07/motivational-quote-website.git
2. Install the required packages:
    pip install -r requirements.txt
3. Run the application:
    python app.py
4. Access the website in your browser at http://localhost:5000 to see the daily motivational quote.

## CSV File Format

The quotes are read from a CSV file located in the data/quotes.csv path. The CSV file should have the following format:

Quote,Author
"Quote 1",Author 1
"Quote 2",Author 2
...

## Usage

Upon accessing the website, the homepage will display the daily motivational quote.
The quote will automatically update daily at midnight.

## Contributing

Contributions are welcome! If you have any ideas, improvements, or bug fixes, please open an issue or submit a pull request.
