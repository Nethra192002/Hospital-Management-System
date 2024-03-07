from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)



db = mysql.connector.connect(
    #your details
)

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        option = request.form['option']
        if option == 'doctor':
            return redirect('/index') 
        elif option == 'patient':
            return redirect('/patientindex')  
    else:
        return render_template('welcome.html')

@app.route('/index', methods=['GET', 'POST'])
def clear():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute('SELECT doctor_id, doctor_name FROM Doctor WHERE email=%s AND password=%s', (email, password))
        doctor = cursor.fetchone()
        if doctor:
            session['doctor_id'] = doctor[0]
            session['doctor_name'] = doctor[1]
            return redirect('/dashboard')
        else:
            return render_template('index.html', error='Invalid credentials')
    else:
        return render_template('index.html')
    
@app.route('/patientindex', methods=['GET', 'POST'])
def patientindex():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute('SELECT name FROM Patient WHERE email=%s AND password=%s', (email, password))
        patient = cursor.fetchone()
        if patient:
            session['name'] = patient[0]
            return redirect('/pdashboard')
        else:
            return render_template('patientindex.html', error='Invalid credentials')
    else:
        return render_template('patientindex.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        doctor_name = request.form['doctor_name']
        department_id = request.form['department_id']
        email = request.form['email']
        gender = request.form['gender']
        password = request.form['password']
        
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO Doctor VALUES (%s, %s, %s, %s, %s, %s)',
                           (doctor_id,doctor_name, department_id, email, gender, password))
            db.commit()
            return redirect('/index')
        except Exception as e:
            db.rollback()
            return render_template('register.html', error=str(e))
    else:
        return render_template('register.html')
    
@app.route('/patientreg', methods=['GET', 'POST'])
def patientreg():
    if request.method == 'POST':
        name = request.form['name']
        addr = request.form['addr']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO Patient VALUES (%s, %s, %s, %s, %s)',
                           (name,addr, gender, email, password))
            db.commit()
            return redirect('/patientindex')
        except Exception as e:
            db.rollback()
            return render_template('patientreg.html', error=str(e))
    else:
        return render_template('patientreg.html')

@app.route('/auth', methods=['POST'])
def authenticate():
    cursor = db.cursor()
    email = request.form['email']
    password = request.form['password']
    cursor.execute('SELECT doctor_id, doctor_name FROM Doctor WHERE email=%s AND password=%s', (email, password))
    doctor = cursor.fetchone()
    if doctor:
        session['doctor_id'] = doctor[0]
        session['doctor_name'] = doctor[1]
        return redirect('/dashboard')
    else:
        error = 'Invalid credentials. Please try again.'
        return render_template('index.html', error=error)
    
@app.route('/pauth', methods=['POST'])
def pauthenticate():
    cursor = db.cursor()
    email = request.form['email']
    password = request.form['password']
    cursor.execute('SELECT name,email FROM Patient WHERE email=%s AND password=%s', (email, password))
    patient = cursor.fetchone()
    if patient:
        session['name'] = patient[0]
        session['email'] = patient[1]
        return redirect('/patientdash') 
    else:
        error = 'Invalid credentials. Please try again.'
        return render_template('patientindex.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        cursor = db.cursor()
        cursor.execute('''
            SELECT Doctor.*, Department.dept_name 
            FROM Doctor 
            JOIN Department ON Doctor.department_id = Department.dept_id 
            WHERE Doctor.doctor_id = %s
        ''', (doctor_id,))
        doctor_info = cursor.fetchone()
        cursor.execute('SELECT * FROM Schedule WHERE id=%s', (doctor_id,))
        schedule_info = cursor.fetchall()
        cursor.execute('SELECT * FROM Department')
        dept_info = cursor.fetchall()
        cursor.execute('SELECT * FROM Staff')
        staff_info = cursor.fetchall()
        cursor.execute('SELECT * FROM Diagnose WHERE doctor_id=%s', (doctor_id,))
        diagnose_info = cursor.fetchall()
        cursor.execute('SELECT * FROM Patientlist WHERE doctor_id=%s', (doctor_id,))
        patlist_info = cursor.fetchall()
        cursor.execute('SELECT * FROM Appointment WHERE doctor_id=%s', (doctor_id,))
        appt_info = cursor.fetchall()

        return render_template('dashboard.html', doctor_info=doctor_info, schedule_info=schedule_info,dept_info=dept_info,staff_info=staff_info,diagnose_info=diagnose_info,patlist_info=patlist_info,appt_info=appt_info)
    else:
        return redirect('/index')
    
@app.route('/patientdash')
def patientdash():
    if 'email' in session:
        email = session['email']
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Patient WHERE email=%s', (email,))
        patient_info = cursor.fetchone()
        cursor.execute('SELECT * FROM Appointment WHERE p_email=%s', (email,))
        appt_info = cursor.fetchall()
        cursor.execute('SELECT * FROM Department')
        dept_info = cursor.fetchall()
        cursor.execute('SELECT * FROM Diagnose WHERE p_email=%s', (email,))
        diagnose_info = cursor.fetchall()
        cursor.execute('SELECT * FROM Patientlist WHERE p_email=%s', (email,))
        patientlist_info = cursor.fetchall()
        return render_template('patientdash.html', patient_info=patient_info,appt_info=appt_info,diagnose_info=diagnose_info,patientlist_info=patientlist_info,dept_info=dept_info)
    else:
        return redirect('/patientindex')
    
@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        if request.method == 'POST':
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            break_time = request.form['break_time']
            day = request.form['day']
            cursor = db.cursor()
            cursor.execute('INSERT INTO Schedule (id, starttime, endtime, breaktime, day) VALUES (%s, %s, %s, %s, %s)',
                           (doctor_id, start_time, end_time, break_time, day))
            db.commit()
            return redirect('/dashboard')
    else:
        return redirect('/index')


@app.route('/delete_schedule', methods=['POST'])
def delete_schedule():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        break_time = request.form['break_time']
        day = request.form['day']
        cursor = db.cursor()
        cursor.execute('DELETE FROM Schedule WHERE id=%s AND starttime=%s AND endtime=%s AND breaktime=%s AND day=%s',
                       (doctor_id, start_time, end_time, break_time, day))
        db.commit()
        return redirect('/dashboard')
    else:
        return redirect('/index')


@app.route('/add_appt', methods=['POST'])
def add_appt():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        p_name = request.form['p_name']
        p_email = request.form['p_email']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        status = request.form['status']
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO Appointment (doctor_id, p_name, p_email, date, starttime, endtime, status) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                           (doctor_id, p_name, p_email, date, start_time, end_time, status))
            db.commit()
        except mysql.connector.Error as err:
            print("Failed to insert record into MySQL table: {}".format(err))
            db.rollback()
        return redirect('/dashboard')
    else:
        return redirect('/index')
    

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    if 'email' in session:
        p_email = session['email']
        doctor_id = request.form['doctor_id']
        p_name = request.form['p_name']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        status = request.form['status']
        cursor = db.cursor()
        try:
            cursor.execute('''INSERT INTO Appointment (doctor_id, p_name, p_email, date, starttime, endtime, status) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           (doctor_id, p_name, p_email, date, start_time, end_time, status))
            db.commit()
        except mysql.connector.Error as err:
            print("Failed to insert record into MySQL table: {}".format(err))
            db.rollback()
        return redirect('/patientdash')
    else:
        return redirect('/patientindex')



@app.route('/delete_appt', methods=['POST'])
def delete_appt():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        p_name = request.form['p_name']
        p_email = request.form['p_email']
        date = request.form['date']
        cursor = db.cursor()
        cursor.execute('DELETE FROM Appointment WHERE doctor_id=%s AND p_name=%s AND p_email=%s and date=%s',
                       (doctor_id, p_name,p_email,date))
        db.commit()
        return redirect('/dashboard')
    else:
        return redirect('/index')
    
@app.route('/delete_appointment', methods=['POST'])
def delete_appointment():
    if 'email' in session:
        p_email = session['email']
        doctor_id = request.form['doctor_id']
        p_name = request.form['p_name']
        date = request.form['date']
        cursor = db.cursor()
        try:
            cursor.execute('DELETE FROM Appointment WHERE doctor_id=%s AND p_name=%s AND p_email=%s and date=%s',
                        (doctor_id, p_name, p_email,date))
            db.commit()
        except mysql.connector.Error as err:
            print("Error:", err)
            db.rollback()
        return redirect('/patientdash')
    else:
        return redirect('/patientindex')


@app.route('/add_diagnose', methods=['POST'])
def add_diagnose():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        p_name = request.form['p_name']
        p_email = request.form['p_email']
        diagnosis = request.form['diagnosis']
        prescription = request.form['prescription']

        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO Diagnose VALUES (%s, %s, %s, %s, %s)',
                        (doctor_id,p_name, p_email, diagnosis, prescription))
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)  
        return redirect('/dashboard')
    
@app.route('/delete_diagnose', methods=['POST'])
def delete_diagnose():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        p_name = request.form['p_name']
        p_email = request.form['p_email']
        cursor = db.cursor()
        cursor.execute('DELETE FROM Diagnose WHERE doctor_id=%s AND p_name=%s AND p_email=%s',
                       (doctor_id, p_name,p_email))
        db.commit()
        return redirect('/dashboard')
    else:
        return redirect('/index')

@app.route('/add_patient', methods=['POST'])
def add_patient():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        p_name = request.form['p_name']
        p_email = request.form['p_email']
        prev_doc=request.form['prev_doc']
        date = request.form['date']
        conditions = request.form['conditions']
        surgeries = request.form['surgeries']
        medication = request.form['medication']
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Patientlist 
                        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)''', 
                        (doctor_id, p_name, p_email,prev_doc, date, conditions, surgeries, medication))
        db.commit()
        return redirect('/dashboard')
    else:
        return redirect('/index')

@app.route('/delete_patient', methods=['POST'])
def delete_patient():
    if 'doctor_id' in session:
        doctor_id = session['doctor_id']
        p_name = request.form['p_name']
        p_email = request.form['p_email']
        cursor = db.cursor()
        cursor.execute('DELETE FROM Patientlist WHERE doctor_id=%s AND p_name=%s AND p_email=%s',
                       (doctor_id, p_name,p_email))
        db.commit()
        return redirect('/dashboard')
    else:
        return redirect('/index')
    

@app.route('/add_patient1', methods=['POST'])
def add_patient1():
    if 'email' in session:
        doctor_id = request.form['doctor_id']
        p_name = request.form['p_name']
        p_email = session['email']
        prev_doc=request.form['prev_doc']
        date = request.form['date']
        conditions = request.form['conditions']
        surgeries = request.form['surgeries']
        medication = request.form['medication']
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Patientlist 
                        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)''', 
                        (doctor_id, p_name, p_email,prev_doc, date, conditions, surgeries, medication))
        db.commit()
        return redirect('/patientdash')
    else:
        return redirect('/patientindex')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/welcome')

if __name__ == '__main__':
    app.run(debug=True)
