import sqlite3

# Connect to DB
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Create table Tasks if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS Tasks (
id INTEGER PRIMARY KEY,
task TEXT NOT NULL,
name TEXT NOT NULL,
time TEXT NOT NULL
)
''')

# Save changes and close connections
connection.commit()
connection.close()

# View tasks
def view_tasks():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Tasks')
    tasks = cursor.fetchall()
    connection.close()
    return tasks

# Add new task
def add_new_task(task, name, time):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Tasks (task, name, time) VALUES (?, ?, ?)', (task, name, time))
    connection.commit()
    connection.close()



#cursor.execute('UPDATE Users SET age = ? WHERE username = ?', (29, 'newuser'))

#cursor.execute('DELETE FROM Users WHERE username = ?', ('newuser',))

#cursor.execute('INSERT INTO Tasks (task, name, time) VALUES (?, ?, ?)', ("Test task", "Test Name", "31.12"))

#cursor.execute('INSERT INTO Tasks (task, name, time) VALUES (?, ?, ?)', ("Test task2", "Test Name2", "31.10"))