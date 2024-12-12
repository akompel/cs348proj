from flask import Flask, g, request, redirect, url_for, render_template, flash
import sqlite3
import secrets
from db import (
    add_user, add_workshop, add_registration, initialize_database,
    get_all_users, get_all_workshops, get_user_by_id, get_workshop_by_id,
    get_registrations_by_workshop, update_workshop, delete_workshop, delete_registration
)

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generates a secure random key

# Database setup
DATABASE = '/Users/agastya/cs348/proj1/part1/data/database.db'

initialize_database()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/workshops')
def workshops():
  workshops = get_all_workshops()
  return render_template('workshops.html', workshops=workshops)

@app.route('/workshop/<int:workshop_id>')
def view_workshop(workshop_id):
    workshop = get_workshop_by_id(workshop_id)
    registrations = get_registrations_by_workshop(workshop_id)
    users = get_all_users()
    return render_template('workshop.html', workshop=workshop, registrations=registrations, users=users)

# Route to create a new workshop
@app.route('/add_workshop', methods=['GET', 'POST'])
def add_workshop_route():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        duration = int(request.form['duration'])
        add_workshop(title, date, duration)
        flash('Workshop added successfully!')
        return redirect(url_for('workshops'))
    return render_template('add_workshop.html')

# Route to edit an existing workshop
@app.route('/edit_workshop/<int:workshop_id>', methods=['GET', 'POST'])
def edit_workshop(workshop_id):
    workshop = get_workshop_by_id(workshop_id)
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        duration = int(request.form['duration'])
        update_workshop(workshop_id, title, date, duration)
        flash('Workshop updated successfully!')
        return redirect(url_for('view_workshop', workshop_id=workshop_id))
    return render_template('edit_workshop.html', workshop=workshop)

# Route to delete a workshop
@app.route('/delete_workshop/<int:workshop_id>')
def delete_workshop_route(workshop_id):
    delete_workshop(workshop_id)
    flash('Workshop deleted successfully!')
    return redirect(url_for('workshops'))

# Route to add a registration for a user to a workshop
@app.route('/register_user', methods=['POST'])
def register_user():
    user_id = int(request.form['user_id'])
    workshop_id = int(request.form['workshop_id'])
    add_registration(workshop_id, user_id)
    flash('User registered successfully!')
    return redirect(url_for('view_workshop', workshop_id=workshop_id))

# Route to delete a registration
@app.route('/delete_registration/<int:workshop_id>/<int:registration_id>')
def delete_registration_route(workshop_id, registration_id):
    delete_registration(registration_id)
    flash('Registration deleted successfully!')
    return redirect(url_for('view_workshop', workshop_id=workshop_id))

@app.route('/')
def home():
    return redirect(url_for('workshops'))

if __name__ == '__main__':
    app.run(debug=True, port = 8080)