import pyodbc

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=IN-5CG9524WSS;'
    'Database=students;'
    'Trusted_Connection=yes;'
    'user=sa;'
    'password=1234;'
)

cursor = conn.cursor()

print(cursor)

cursor.execute('SELECT * FROM student_details')

for i in cursor:
    print(i)

