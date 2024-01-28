from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
conn = sqlite3.connect('medical_appointments.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        phone_number TEXT,
        appointment_time DATETIME NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('medical_appointments.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id, patient_name, phone_number, appointment_time FROM appointments ORDER BY appointment_time DESC')
    appointments = cursor.fetchall()
    conn.close()

    return render_template('index.html', appointments=appointments)

@app.route('/schedule', methods=['POST'])
def schedule():
    patient_name = request.form.get('patient_name')
    phone_number = request.form.get('phone_number')
    appointment_date_str = request.form.get('appointment_date')
    appointment_time_str = request.form.get('appointment_time')

    try:
        appointment_datetime_str = f"{appointment_date_str} {appointment_time_str}"
        appointment_datetime = datetime.strptime(appointment_datetime_str, '%Y-%m-%d %H:%M')
    except ValueError:
        return 'Invalid date format'

    conn = sqlite3.connect('medical_appointments.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO appointments (patient_name, phone_number, appointment_time) VALUES (?, ?, ?)',
                   (patient_name, phone_number, appointment_datetime))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:appointment_id>')
def delete(appointment_id):
    conn = sqlite3.connect('medical_appointments.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
 