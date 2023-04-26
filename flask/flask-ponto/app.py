from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'clock_in.db'
conn = sqlite3.connect('clock_in.db')
conn.execute('''CREATE TABLE IF NOT EXISTS students (
                rfID varchar(100) NOT NULL,
                RAStudent int,
                nameStudent varchar (255),
                presenceStudent int,
                absenceStudent int,
                lateStudent int,
                isPresent tinyint(1) default 0,
                PRIMARY KEY (rfID)
            )''')
conn.execute('''CREATE TABLE IF NOT EXISTS entrance_table (
                idEntrance INTEGER PRIMARY KEY AUTOINCREMENT,
                timeEntrance TIMESTAMP,
                rfID varchar (100),
                FOREIGN KEY (rfID) REFERENCES students(rfID)
            )''')
conn.execute('''CREATE TABLE IF NOT EXISTS general_attendance (
                rfID varchar(100) NOT NULL,
                nameStudent varchar (255),
                presenceStudent int,
                absenceStudent int,
                lateStudent int,
                FOREIGN KEY (rfID) REFERENCES students(rfID)
            )''')
conn.execute('''CREATE TABLE IF NOT EXISTS exit_table (
                idExit INTEGER PRIMARY KEY AUTOINCREMENT,
                timeExit TIMESTAMP,
                rfID varchar (100),
                FOREIGN KEY (rfID) REFERENCES students(rfID)
                )''')
conn.commit()
conn.close()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ra = request.form['ra']
        return redirect(url_for('registro', ra=ra))
    return render_template('login.html')


@app.route('/registro/<ra>')
def registro(ra):
    conn = sqlite3.connect('clock_in.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM general_attendance WHERE rfID = '{ra}'")
    student = cursor.fetchone()
    if student is not None:
        rfID = student[0]
        name = student[1]
        presence = student[2]
        absence = student[3]
        late = student[4]
        cursor.execute(f"SELECT COUNT(*) FROM entrance_table WHERE rfID = {rfID}")
        presence_count = cursor.fetchone()[0]
        cursor.execute(f"SELECT COUNT(*) FROM exit_table WHERE rfID = {rfID}")
        absence_count = cursor.fetchone()[0]

        cursor.execute(f"SELECT timeEntrance FROM entrance_table WHERE rfID = {rfID} ORDER BY timeEntrance DESC LIMIT 10")
        entrance_times = [row[0] for row in cursor.fetchall()]
        cursor.execute(f"SELECT timeExit FROM exit_table WHERE rfID = {rfID} ORDER BY timeExit DESC LIMIT 10")
        exit_times = [row[0] for row in cursor.fetchall()]

        conn.close()
        return render_template('registro.html', name=name, presence=presence, absence=absence, late=late, presence_count=presence_count, absence_count=absence_count, entrance_times=entrance_times, exit_times=exit_times)
    else:
        conn.close()
        return 'Aluno não encontrado'


@app.route('/get_student_data/')
def get_student_data():
    ra = request.args.get('ra')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM general_attendance WHERE rfID = '{ra}'")
    student = cursor.fetchone()
    if student:
        rfID = student[0]
        name = student[1]
        presence = student[2]
        absence = student[3]
        late = student[4]
        cursor.execute(f"SELECT COUNT(*) FROM entrance_table WHERE rfID = {rfID}")
        presence_count = cursor.fetchone()[0]
        cursor.execute(f"SELECT COUNT(*) FROM exit_table WHERE rfID = {rfID}")
        absence_count = cursor.fetchone()[0]
        conn.close()
        return jsonify({'status': 'success', 'name': name, 'presence_count': presence_count, 'absence_count': absence_count})
    else:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Aluno não encontrado'})


if __name__ == '__main__':
    app.run(debug=True)
