from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/eventus_db'
app.secret_key = 'your_secret_key'
mongo = PyMongo(app)

# Add club admin credentials to the database
club_admins = [
    {'username': 'atelier', 'password': generate_password_hash('atelier2024')},
    {'username': 'ieee', 'password': generate_password_hash('ieee2024')},
    {'username': 'iedc', 'password': generate_password_hash('iedc2024')},
    {'username': 'gdsc', 'password': generate_password_hash('gdsc2024')},
    {'username': 'tinkerhub', 'password': generate_password_hash('tinkerhub2024')},
    {'username': 'yuva', 'password': generate_password_hash('yuva2024')}
]

for admin in club_admins:
    if not mongo.db.club_admins.find_one({'username': admin['username']}):
        mongo.db.club_admins.insert_one(admin)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials')
        return redirect(url_for('index'))

@app.route('/club_admin_login', methods=['POST'])
def club_admin_login():
    username = request.form['club_username']
    password = request.form['club_password']
    admin = mongo.db.club_admins.find_one({'username': username})
    if admin and check_password_hash(admin['password'], password):
        session['club_admin'] = username
        return redirect(url_for('club_dashboard'))
    else:
        flash('Invalid club admin credentials')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        events = mongo.db.events.find()
        clubs = mongo.db.club_admins.distinct('username')
        return render_template('dashboard.html', events=events, clubs=clubs)
    return redirect(url_for('index'))

@app.route('/club_dashboard')
def club_dashboard():
    if 'club_admin' in session:
        # Retrieve all events for the club
        events = list(mongo.db.events.find({'club': session['club_admin']}))
        return render_template('club_dashboard.html', events=events)
    return redirect(url_for('club_login'))

@app.route('/add_event', methods=['POST'])
def add_event():
    if 'club_admin' in session:
        event_data = {
            'name': request.form['event_name'],
            'date': request.form['event_date'],
            'time': request.form['event_time'],
            'venue': request.form['event_venue'],
            'details': request.form['event_details'],
            'club': session['club_admin'],
            'participants': []
        }
        mongo.db.events.insert_one(event_data)
        return redirect(url_for('club_dashboard'))
    return redirect(url_for('club_login'))

@app.route('/modify_event', methods=['POST'])
def modify_event():
    if 'club_admin' in session:
        event_id = request.form['event_id']
        event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
        if event:
            return render_template('club_dashboard.html', event=event)
    return redirect(url_for('club_dashboard'))

@app.route('/update_event', methods=['POST'])
def update_event():
    if 'club_admin' in session:
        event_id = request.form['event_id']
        event_data = {
            'name': request.form['event_name'],
            'date': request.form['event_date'],
            'time': request.form['event_time'],
            'venue': request.form['event_venue'],
            'details': request.form['event_details'],
            'club': session['club_admin']
        }
        mongo.db.events.update_one({'_id': ObjectId(event_id)}, {'$set': event_data})
        return redirect(url_for('club_dashboard'))
    return redirect(url_for('club_login'))

@app.route('/remove_event', methods=['POST'])
def remove_event():
    if 'club_admin' in session:
        event_id = request.form['event_id']
        mongo.db.events.delete_one({'_id': ObjectId(event_id)})
        return redirect(url_for('club_dashboard'))
    return redirect(url_for('club_login'))

@app.route('/past_events')
def past_events():
    if 'club_admin' in session:
        # Retrieve past events for the club
        events = mongo.db.events.find({'club': session['club_admin']})
        return render_template('club_dashboard.html', events=events)
    return redirect(url_for('club_login'))

@app.route('/register_event/<event_id>', methods=['POST'])
def register_event(event_id):
    if 'user' in session:
        event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
        if event:
            mongo.db.events.update_one(
                {'_id': ObjectId(event_id)},
                {'$addToSet': {'participants': {'username': session['user']}}}
            )
            return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/unregister_event/<event_id>', methods=['POST'])
def unregister_event(event_id):
    if 'user' in session:
        event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
        if event:
            mongo.db.events.update_one(
                {'_id': ObjectId(event_id)},
                {'$pull': {'participants': {'username': session['user']}}}
            )
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
    
    user = {
        'fullname': fullname,
        'email': email,
        'mobile': mobile,
        'batch': batch,
        'department': department,
        'username': username,
        'password': password
    }
    
    mongo.db.users.insert_one(user)
    return redirect(url_for('index'))

@app.route('/get_event/<event_id>', methods=['GET'])
def get_event(event_id):
    event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
    if event:
        return jsonify({
            'name': event['name'],
            'date': event['date'],
            'time': event['time'],
            'venue': event['venue'],
            'details': event['details']
        })
    else:
        return jsonify({'error': 'Event not found'}), 404

@app.route('/remove_event/<event_id>', methods=['DELETE'])
def remove_event_by_id(event_id):
    result = mongo.db.events.delete_one({'_id': ObjectId(event_id)})
    if result.deleted_count:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 404

if __name__ == '__main__':
    app.run(debug=True)
