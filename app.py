from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import pandas as pd

# Importing Suhas's Analytics Engine
from analytics_engine import assign_doctors, calculate_lab_etas, generate_symptom_chart

app = Flask(__name__)
# A secret key is required by Flask to keep login sessions secure
app.secret_key = "bridgecare_super_secret" 

# --- HELPER FUNCTION: Get DB Connection ---
def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# SHIVAM'S DOMAIN: AUTHENTICATION ROUTES
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role'] # 'Doctor' or 'Patient'
        
        conn = get_db_connection()
        
        # Check if the username is already taken
        existing_user = conn.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
        
        if existing_user:
            flash('That username is already taken! Try another one.', 'danger')
        else:
            # Save the brand new user to the database!
            conn.execute('INSERT INTO Users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            conn.close()
            
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
            
        conn.close()
        
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check the database to see if the user exists
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            # Login successful! Save their identity in the session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again!', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() # Wipe the session clean
    return redirect(url_for('login'))

# ==========================================
# THE DASHBOARD ROUTER (Handles both Doctors & Patients)
# ==========================================
@app.route('/')
def dashboard():
    # 🚨 SECURITY CHECK: If they aren't logged in, kick them to the login page!
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 👨‍⚕️ IF A DOCTOR LOGS IN (Suhas's Domain)
    if session['role'] == 'Doctor':
        # Connect to DB for Suhas's Engine
        conn = sqlite3.connect('hospital.db')
        df = pd.read_sql("SELECT patient_id, name, symptom FROM Patients", conn)
        queue_df = pd.read_sql("SELECT patient_name, test_type FROM LabQueue", conn)
        conn.close()

        # Run Suhas's Engine Logic
        processed_patients = assign_doctors(df)
        processed_queue = calculate_lab_etas(queue_df)
        generate_symptom_chart(processed_patients)
        
        return render_template('dashboard.html', 
                               patients=processed_patients.to_dict(orient='records'), 
                               lab_queue=processed_queue.to_dict(orient='records'), 
                               current_user=session['username'])
                               
    # 🤒 IF A PATIENT LOGS IN (Teammate 4's Domain)
    elif session['role'] == 'Patient':
        conn = get_db_connection()
        # Find this specific patient's medical record
        patient_record = conn.execute('SELECT * FROM Patients WHERE name = ?', (session['username'],)).fetchone()
        conn.close()
        
        return render_template('patient_dashboard.html', 
                               current_user=session['username'],
                               record=patient_record)

if __name__ == '__main__':
    app.run(debug=True)