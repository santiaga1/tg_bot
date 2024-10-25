import sqlite3

class DB_Connect:
    def __init__(self):
        # Connect to DB
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

        # Create table Tasks if not exists
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL,
            name TEXT NOT NULL,
            time TEXT NOT NULL
        )
        ''')
        
        # Save changes and close connections
        self.connection.commit()

    # View tasks
    def view_tasks(self):
        self.cursor.execute('SELECT * FROM Tasks')
        tasks = self.cursor.fetchall()
        return tasks

    # Add new task
    def add_new_task(self, task, name, time):
        self.cursor.execute('INSERT INTO Tasks (task, name, time) VALUES (?, ?, ?)', (task, name, time))
        self.connection.commit()

    # Delete task
    def del_task(self, id):
        self.cursor.execute('DELETE FROM Tasks WHERE id = ?', (id,))
        self.connection.commit()

    def __del__(self):
        self.connection.close()
        #print("Close DB")
