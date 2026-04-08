import sqlite3
def init_db():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS searches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temp REAL,
        condition TEXT
            ) """)
    
    conn.commit()
    conn.close()