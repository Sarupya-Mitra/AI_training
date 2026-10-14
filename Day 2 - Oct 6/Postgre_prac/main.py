# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="cinema_demo",
    user="postgres",
    password="Admin@123"
)

cursor = conn.cursor()

print("Connected to PostgreSQL")
######################### Create Table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS screenings (
#     screening_id SERIAL PRIMARY KEY,
#     movie_name VARCHAR(100),
#     screen_number INT,
#     show_time VARCHAR(20),
#     available_seats INT
# )
# """)

# conn.commit()
#
# print("Table created")
############################## Inserting
# cursor.execute("""
# INSERT INTO screenings
# (movie_name, screen_number, show_time, available_seats)
# VALUES
# ('Silent Horizon', 1, '10:00 AM', 65),
# ('Red Planet', 2, '01:30 PM', 42),
# ('Ocean Signal', 3, '04:00 PM', 18),
# ('Silent Horizon', 1, '07:00 PM', 25)
# """)
#
# conn.commit()
#
# print("Records inserted")

cursor.execute("SELECT * FROM screenings")

rows = cursor.fetchall()

for row in rows:
    print(row)
############### Selecting based on constraints
# cursor.execute("""
# SELECT movie_name, show_time, available_seats
# FROM screenings
# WHERE available_seats < 30
# """)
#
# for row in cursor.fetchall():
#     print(row)
################# Updating
# cursor.execute("""
# UPDATE screenings
# SET available_seats = available_seats - 5
# WHERE screening_id = 3
# """)
#
# conn.commit()
################# Deleting
# cursor.execute("""
# DELETE FROM screenings
# WHERE screening_id = 4
# """)
#
# conn.commit()
