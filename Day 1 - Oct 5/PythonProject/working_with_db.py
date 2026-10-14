import sqlite3
import pandas as pd

conn = sqlite3.connect("cinema.db")

cursor = conn.cursor()

# cursor.execute("""CREATE TABLE IF NOT EXISTS bookings
# (bookings_id INTEGER PRIMARY KEY,
# movie TEXT,
# seats INTEGER,
# amount REAL)
# """)

# cursor.execute("""
# INSERT INTO bookings (movie, seats, amount)
# VALUES ('Solar Drift', 2, 700)
# """)
#
# cursor.execute("""
# INSERT INTO bookings (movie, seats, amount)
# VALUES ('Midnight Code', 4, 1200)
# """)
#
# conn.commit()

# cursor.execute("Select * from bookings")
# print(cursor.fetchall())

df = pd.read_sql_query("select * from bookings", conn)

print(df)

