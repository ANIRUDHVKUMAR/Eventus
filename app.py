from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '************'
app.config['MYSQL_DB'] = 'eventus_db'

mysql = MySQL(app)

# Initialize Club Admin Credentials
club_admins = [
    ('atelier', generate_password_hash('atelier2024')),
    ('ieee', generate_password_hash('ieee2024')),
    ('iedc', generate_password_hash('iedc2024')),
    ('gdsc', generate_password_hash('gdsc2024')),
    ('tinkerhub', generate_password_hash('tinkerhub2024')),
    ('yuva', generate_password_hash('yuva2024'))
]

with app.app_context():
    cur = mysql.connection.cursor()
    for username, password in club_admins:
        cur.execute("SELECT * FROM club_admins WHERE username = %s", (username,))
        if not cur.fetchone():
            cur.execute("INSERT INTO club_admins (username, password) VALUES (%s, %s)", (username, password))
    mysql.connection.commit()
    cur.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user[6], password):
        session['user'] = username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials')
        return redirect(url_for('index'))

@app.route('/club_admin_login', methods=['POST'])
def club_admin_login():
    username = request.form['club_username']
    password = request.form['club_password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM club_admins WHERE username = %s", (username,))
    admin = cur.fetchone()
    cur.close()

    if admin and check_password_hash(admin[2], password):
        session['club_admin'] = username
        return redirect(url_for('club_dashboard'))
    else:
        flash('Invalid club admin credentials')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM events")
        events = cur.fetchall()
        cur.execute("SELECT username FROM club_admins")
        clubs = cur.fetchall()
        cur.close()
        return render_template('dashboard.html', events=events, clubs=[club[0] for club in clubs])
    return redirect(url_for('index'))

@app.route('/club_dashboard')
def club_dashboard():
    if 'club_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM events WHERE club = %s", (session['club_admin'],))
        events = cur.fetchall()
        cur.close()
        return render_template('club_dashboard.html', events=events)
    return redirect(url_for('club_admin_login'))

@app.route('/add_event', methods=['POST'])
def add_event():
    if 'club_admin' in session:
        name = request.form['event_name']
        date = request.form['event_date']
        time = request.form['event_time']
        venue = request.form['event_venue']
        details = request.form['event_details']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO events (name, date, time, venue, details, club) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, date, time, venue, details, session['club_admin']))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('club_dashboard'))
    return redirect(url_for('club_admin_login'))

@app.route('/register_event/<event_id>', methods=['POST'])
def register_event(event_id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO participants (event_id, username) VALUES (%s, %s)", (event_id, session['user']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/unregister_event/<event_id>', methods=['POST'])
def unregister_event(event_id):
    if 'user' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM participants WHERE event_id = %s AND username = %s", (event_id, session['user']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    fullname = request.form['fullname']
    email = request.form['email']
    mobile = request.form['mobile']
    batch = request.form['batch']
    department = request.form['department']
    username = request.form['username']
    password = generate_password_hash(request.form['password'])

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (fullname, email, mobile, batch, department, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (fullname, email, mobile, batch, department, username, password))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
