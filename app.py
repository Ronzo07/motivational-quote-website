"""
Motivational Quote Website
--------------------------

This Flask application displays a motivational quote every day. The quotes are read from a CSV file and chosen based on the current day of the year. The chosen quote is then displayed on the website, and it updates automatically at midnight.

Usage:
- Run the Flask application by executing this script.
- Access the website at http://localhost:5000 to see the daily motivational quote.

Dependencies:
- Flask: A web framework for Python. Install using `pip install Flask`.
- Celery: A distributed task queue system. Install using `pip install celery`.
- Redis: A message broker for Celery. Install and configure a Redis server locally.

File Structure:
- app.py: The main Flask application that handles routing and rendering templates.
- tasks.py: Contains Celery tasks for updating the quotes and scheduling the updates.
- data/quotes.csv: A CSV file containing motivational quotes and authors.

"""

from flask import Flask, render_template
import csv
from datetime import datetime
from flask import make_response
from celery import Celery
from celery.schedules import crontab

# Flask application setup
app = Flask(__name__)
celery = Celery(app.name, broker='redis://localhost:6379/0')


@celery.task
def update_quotes():
    """
    Celery task to update the quotes daily at midnight.

    - Reads the quotes from the CSV file.
    - Chooses a quote based on the current day of the year.
    - Renders the index.html template with the chosen quote.
    - Sets a cookie with the quote text in the response.
    """
    with app.app_context():
        quotes = get_quotes()
        chosen_quote = choose_quote(quotes)
        response = make_response(render_template('index.html', quote=chosen_quote['text'], author=chosen_quote['author']))
        expires = datetime.now().replace(hour=12, minute=36, second=59, microsecond=0)
        response.set_cookie('quote', chosen_quote['text'], expires=expires)
        return response


# Celery configuration for scheduling the task
celery.conf.beat_schedule = {
    'update-quote-at-midnight': {
        'task': 'update_quotes',
        'schedule': crontab(hour=0, minute=0),
    },
}


def get_quotes():
    """
    Read the motivational quotes from the CSV file.

    Returns:
    - A list of dictionaries representing the quotes.
    """
    quotes = []
    with open('data/quotes.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quotes.append(row)
    return quotes


def choose_quote(quotes):
    """
    Choose a quote based on the current day of the year.

    Args:
    - quotes (list): A list of dictionaries representing the quotes.

    Returns:
    - A dictionary containing the chosen quote and author.
    """
    day_of_year = datetime.now().timetuple().tm_yday
    quote = quotes[day_of_year % len(quotes)]
    quote['text'] = '“' + str(quote['Quote']) + '”'
    return quote


@app.route('/')
def index():
    """
    Route handler for the homepage.

    - Reads the quotes from the CSV file.
    - Chooses a quote based on the current day of the year.
    - Renders the index.html template with the chosen quote.
    """
    quotes = get_quotes()
    chosen_quote = choose_quote(quotes)
    return render_template('index.html', quote=chosen_quote['text'], author=chosen_quote['Author'], date=datetime.now().strftime('%Y-%m-%d'))


if __name__ == '__main__':
    app.run()
