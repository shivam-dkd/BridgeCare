import sqlite3

# 1. Create the database file (this creates hospital.db in your folder)
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

print("Building tables...")

# 2. Create Patients Table (For your Analytics Engine)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    symptom TEXT NOT NULL
)
''')

# 3. Create Lab Queue Table (For your ETA Calculator)
cursor.execute('''
CREATE TABLE IF NOT EXISTS LabQueue (
    queue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    test_type TEXT NOT NULL
)
''')

# 4. Create Users Table (We are setting this up for Shivam's Login page later!)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')

# --- INJECTING THE DUMMY DATA ---
print("Injecting dummy data...")

# Clear tables first just in case you run this script more than once
cursor.execute('DELETE FROM Patients')
cursor.execute('DELETE FROM LabQueue')

# Insert Patient Data
patients_data = [
    ('Rahul', 'Chest Pain'),
    ('Aditi', 'Fever'),
    ('Karan', 'Broken Bone'),
    ('Priya', 'Skin Rash'),
    ('Amit', 'Stomach Ache')
]
cursor.executemany('INSERT INTO Patients (name, symptom) VALUES (?, ?)', patients_data)

# Insert Lab Queue Data
queue_data = [
    ('Suresh', 'Blood Test'),
    ('Ramesh', 'X-Ray'),
    ('Anita', 'MRI'),
    ('Gita', 'Blood Test')
]
cursor.executemany('INSERT INTO LabQueue (patient_name, test_type) VALUES (?, ?)', queue_data)

# Save (commit) the changes and close the connection
conn.commit()
conn.close()

print("✅ SUCCESS: Database 'hospital.db' created and populated!")