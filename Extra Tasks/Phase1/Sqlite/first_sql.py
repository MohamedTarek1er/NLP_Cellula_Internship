import sqlite3
# con=sqlite3.connect('movies.db')
# cursor=con.cursor()

# movies=[('The Shawshank Redemption', 1994, 'Drama'),
#         ('The Godfather', 1972, 'Crime'),
#         ('The Dark Knight', 2008, 'Action'),
#         ('Pulp Fiction', 1994, 'Crime'),
#         ('Forrest Gump', 1994, 'Drama')]

# data = cursor.execute("Update movie set genre = 2011 where text ='Inception'")
# data = cursor.execute("Select * from movie")
# for row in data:
#     print(row[1])
# print(data.fetchone())
# print(data.fetchmany(2)) 
# data = cursor.fetchall()

# cursor.execute("DELETE FROM movie WHERE rowid = 3")
# data = cursor.execute("Select rowid,* from movie")
# for row in data:
#     print(row)

# con.commit()
# con.close()


db=sqlite3.connect('movies.db')
cursor=db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
)""")

