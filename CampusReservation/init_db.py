import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')
    
    with open('schema.sql', 'w') as f:
        f.write('''
        DROP TABLE IF EXISTS Booking;
        DROP TABLE IF EXISTS Equipment;
        DROP TABLE IF EXISTS Room;
        DROP TABLE IF EXISTS User;
        
        CREATE TABLE User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'student' CHECK(role IN ('student', 'admin'))
        );
        
        CREATE TABLE Room (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'available'
        );
        
        CREATE TABLE Equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'available'
        );
        
        CREATE TABLE Booking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            room_id INTEGER,
            equipment_id INTEGER,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES User (id),
            FOREIGN KEY (room_id) REFERENCES Room (id),
            FOREIGN KEY (equipment_id) REFERENCES Equipment (id)
        );
        ''')
        
    with open('schema.sql', 'r') as f:
        connection.executescript(f.read())

    # Insert some mock data
    cur = connection.cursor()
    cur.execute("INSERT INTO User (username, email, password, role) VALUES (?, ?, ?, ?)", ('Admin User', 'admin@school.edu', '1234', 'admin'))
    cur.execute("INSERT INTO User (username, email, password, role) VALUES (?, ?, ?, ?)", ('Student A', 'student@school.edu', '1234', 'student'))
    
    cur.execute("INSERT INTO Room (name, capacity, description) VALUES (?, ?, ?)", ('Meeting Room A', 10, 'Standard meeting room with whiteboard'))
    cur.execute("INSERT INTO Room (name, capacity, description) VALUES (?, ?, ?)", ('Conference Hall', 100, 'Large hall for events'))
    
    cur.execute("INSERT INTO Equipment (name) VALUES (?)", ('Projector 1',))
    cur.execute("INSERT INTO Equipment (name) VALUES (?)", ('Wireless Microphone',))
    
    connection.commit()
    connection.close()
    
    import os
    if os.path.exists('schema.sql'):
        os.remove('schema.sql')

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
