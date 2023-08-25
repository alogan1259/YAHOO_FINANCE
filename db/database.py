import sqlite3

def create_database():
    conn = sqlite3.connect('stock_data.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS stocks')
    c.execute('''
        CREATE TABLE stocks (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            ticker TEXT,
            name TEXT,
            value TEXT,
            time TEXT,
            change TEXT,
            percent_change TEXT,
            volume TEXT,
            market_cap TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_to_database(data_frame):
    conn = sqlite3.connect('stock_data.db')
    data_frame.to_sql('stocks', conn, if_exists='append', index=False)
    conn.close()
