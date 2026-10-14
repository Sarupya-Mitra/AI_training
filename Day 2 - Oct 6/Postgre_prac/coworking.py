import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    port=5432,
    database="coworking_demo",
    user = "postgres",
    password = "Admin@123"
)
cursor = conn.cursor()

print("Connected to PostgreSQL")

'''
cursor.execute("""CREATE TABLE IF NOT EXISTS rooms(
room_id INT PRIMARY KEY,
room_name TEXT,
capacity INT,
hourly_rate DECIMAL,
status TEXT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS BOOKINGS(
booking_id INTEGER PRIMARY KEY,
room_id INT,
Constraint room_id FOREIGN KEY (room_id) REFERENCES rooms(room_id),
booked_by TEXT,
booking_date DATE,
hours INT
)""")

conn.commit()


cursor.executemany("""
INSERT INTO rooms (room_id, room_name, capacity, hourly_rate, status)
VALUES (%s,%s,%s,%s,%s)
""", [
    (1, 'Conference Room A', 10, 500.00, 'Available'),
    (2, 'Meeting Room B', 6, 300.00, 'Available'),
    (3, 'Training Room', 20, 800.00, 'Booked'),
    (4, 'Executive Room', 8, 1000.00, 'Available'),
    (5, 'Seminar Hall', 50, 2000.00, 'Available')
])


# Insert sample bookings
cursor.executemany("""
INSERT INTO bookings (booking_id, room_id, booked_by, booking_date, hours)
VALUES (%s,%s,%s,%s,%s)
""", [
    (101, 3, 'Rahul', '2026-10-07', 3),
    (102, 1, 'Priya', '2026-10-08', 2),
    (103, 4, 'Arjun', '2026-10-08', 4),
    (104, 2, 'Sneha', '2026-10-09', 2),
    (105, 5, 'Kiran', '2026-10-10', 5)
])
cursor.execute("""INSERT INTO bookings (booking_id, room_id, booked_by, booking_date, hours)
VALUES (106,1,'Virat','2026-10-09',3)""")
# Save changes
conn.commit()
'''
######## Display all rooms and bookings:
# cursor.execute("Select * from rooms")
# print("Rooms:")
# for row in cursor.fetchall():
#     print(row)
#
#
# cursor.execute("Select * from bookings")
# print("Bookings:")
# for row in cursor.fetchall():
#     print(row)

#########  Display room with capacity more than 6

# cursor.execute("Select * from rooms where capacity>=6")
# for row in cursor.fetchall():
#     print(row)

######### display available rooms only
# cursor.execute("Select * from rooms where status='Available'")
# for row in cursor.fetchall():
#     print(row)
######### Show bookings by Arjun
# cursor.execute("select * from bookings where booked_by = 'Arjun'")
# for row in cursor.fetchall():
#     print(row)
'''
######### Update a room's status
cursor.execute("Update rooms set status = 'Maintenance' where room_id = 2")
######### Update hrly rate of a room
cursor.execute("Update rooms set hourly_rate = 1000.00 where room_id=1")
######### Update booked hours by a booker
cursor.execute("Update bookings set hours = 5 where booking_id=101")
print("Rooms table after updation:\n")
cursor.execute("Select * from rooms")
for row in cursor.fetchall():
    print(row)
print("Bookings table after updation:\n")
cursor.execute("Select * from bookings")
for row in cursor.fetchall():
    print(row)
'''

######### How many bookings does each room have?
# cursor.execute("Select rooms.room_name,COUNT(bookings.room_id) from rooms,bookings "
#                "where bookings.room_id = rooms.room_id "
#                "group by rooms.room_id")
# for row in cursor.fetchall():
#     print(row)


######### Room having maximum hrly rate
# cursor.execute("Select * from rooms where hourly_rate = "
#                "(Select MAX(hourly_rate) from rooms)")
# for row in cursor.fetchall():
#     print(row)

######### Calculating booking cost = hrs * hrly_rate
# cursor.execute("Select r.room_name,SUM(r.hourly_rate*b.hours) as booking_cost"
#                " from rooms r INNER JOIN bookings b ON r.room_id=b.room_id"
#                " group by r.room_id")
# for row in cursor.fetchall():
#     print(row)

######### DROP the tables
# cursor.execute("Drop table bookings ")
# cursor.execute("Drop table rooms")
# conn.commit()