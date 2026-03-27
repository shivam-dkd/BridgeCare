import sqlite3

# Connect to Vikash's database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# The exact credentials we want to guarantee exist
users_to_add = [
    ("dr_suhas", "password123", "Doctor"),
    ("Rahul", "patient123", "Patient")
]

print("Forging master keys...")

for username, password, role in users_to_add:
    # First, check if the user is already in there
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()
    
    if existing_user is None:
        # If they don't exist, create them!
        cursor.execute('INSERT INTO Users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        print(f"✅ CREATED: {username} as a {role}")
    else:
        # If they do exist, forcefully update their password and role just in case!
        cursor.execute('UPDATE Users SET password = ?, role = ? WHERE username = ?', (password, role, username))
        print(f"🔄 UPDATED: {username} reset to password '{password}'")

# Save and close
conn.commit()
conn.close()
print("\n🎉 Database unlocked. You are clear to log in!")