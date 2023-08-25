from flask import Flask, jsonify, request
import sqlite3
from api import scrape  # Import scrape module directly
from db import database
import json

app = Flask(__name__)

@app.route('/v1/save-data', methods=['POST'])
def save_data_to_database():
    data = scrape.create_df()
    database.save_to_database(data)
    return jsonify({'message': 'Data saved to the database successfully'})

@app.route('/v1/most-active-accounts', methods=['GET'])
def get_most_active():
    date_param = request.args.get('date')  # Get the date query parameter from the request
    conn = sqlite3.connect('stock_data.db')
    c = conn.cursor()
    
    if date_param:
        # If date parameter is provided, query data based on that date
        c.execute('SELECT timestamp, ticker, name, value, time, change, percent_change, volume, market_cap FROM stocks WHERE date(timestamp) = ?', (date_param,))
    else:
        # If date parameter is not provided, fetch all data
        c.execute('SELECT timestamp, ticker, name, value, time, change, percent_change, volume, market_cap FROM stocks')
    
    most_active = c.fetchall()
    conn.close()
    return json.dumps(most_active, indent=4)


@app.route('/v1/biggest-movers', methods=['GET'])
def get_biggest_movers():
    biggest_movers = scrape.get_biggest_movers()
    return biggest_movers


if __name__ == '__main__':
    database.create_database()  # Create the database when starting the app
    app.run()
