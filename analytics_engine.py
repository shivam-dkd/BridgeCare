import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

# 1. The "Chemistry" - Our rules for who goes where
symptom_mapping = {
    "Fever": "General Physician",
    "Headache": "General Physician",
    "Chest Pain": "Cardiologist",
    "Broken Bone": "Orthopedist",
    "Skin Rash": "Dermatologist",
    "Toothache": "Dentist",
    "Stomach Ache": "Gastroenterologist"
}

# ==========================================
# STEP 1.5: DATABASE CONNECTION
# ==========================================
# Connecting to Vikash's (our) new database!
conn = sqlite3.connect('hospital.db')
df = pd.read_sql("SELECT patient_id, name, symptom FROM Patients", conn)
queue_df = pd.read_sql("SELECT patient_name, test_type FROM LabQueue", conn)
conn.close()

# ==========================================
# STEP 1: ANALYTICS ENGINE LOGIC
# ==========================================
def assign_doctors(patient_data):
    patient_data['assigned_doctor'] = patient_data['symptom'].map(symptom_mapping).fillna("General Physician")
    return patient_data

# ==========================================
# STEP 2: SMART LAB QUEUE ETA CALCULATOR
# ==========================================
def calculate_lab_etas(queue_data):
    time_per_test_mins = 15
    queue_data['wait_time_mins'] = queue_data.index * time_per_test_mins
    queue_data['eta_display'] = queue_data['wait_time_mins'].astype(str) + " mins"
    return queue_data

# ==========================================
# STEP 3: CLINIC ANALYTICS & GRAPHS
# ==========================================
if not os.path.exists('static'):
    os.makedirs('static')

def generate_symptom_chart(patient_data):
    print("\nGenerating Clinic Analytics...")
    symptom_counts = patient_data['symptom'].value_counts()
    
    plt.figure(figsize=(8, 5))
    symptom_counts.plot(kind='bar', color=['#4CAF50', '#2196F3', '#FF9800', '#F44336', '#9C27B0'])
    
    plt.title('Daily Patient Symptoms Overview', fontsize=14, fontweight='bold')
    plt.xlabel('Symptoms', fontsize=12)
    plt.ylabel('Number of Patients', fontsize=12)
    plt.xticks(rotation=45) 
    plt.tight_layout() 
    
    image_path = 'static/symptom_chart.png'
    plt.savefig(image_path)
    print(f"✅ SUCCESS: Chart saved to '{image_path}'")