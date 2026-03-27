import sqlite3

# Connect to our existing database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

print("Upgrading BridgeCare Database to v2...")

# 1. The Appointments & Payments Table
# This stores who booked who, what their symptom is, and if they paid their dummy fee.
cursor.execute('''
CREATE TABLE IF NOT EXISTS Appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    symptom TEXT NOT NULL,
    appointment_date TEXT DEFAULT 'Pending',
    payment_status TEXT DEFAULT 'Unpaid'
)
''')

# 2. The Gamified Medicine Tracker Table
# This holds the custom medicines the patient adds for themselves.
cursor.execute('''
CREATE TABLE IF NOT EXISTS MedicineTracker (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    medicine_name TEXT NOT NULL,
    instructions TEXT NOT NULL,
    total_days INTEGER NOT NULL,
    days_completed INTEGER DEFAULT 0
)
''')

# 3. The Two-Way Communication Table (Follow-ups)
# This acts as the "bridge" where patients can report side effects to their doctor.
cursor.execute('''
CREATE TABLE IF NOT EXISTS FollowUpNotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    note_text TEXT NOT NULL,
    status TEXT DEFAULT 'Unread by Doctor'
)
''')

# Save and close
conn.commit()
conn.close()

print("✅ SUCCESS: Database upgraded! The plumbing is ready for the new features.")