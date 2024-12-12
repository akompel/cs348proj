import sqlite3
from contextlib import closing
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

# Connect to the database (creates the file if it doesn't exist)
DATABASE = '/Users/agastya/cs348/proj1/part1/data/database.db'

# DATABASE_URI = 'sqlite:///Users/agastya/cs348/proj1/part1/data/database.db'
# engine = create_engine(DATABASE_URI)
# Base = declarative_base()
# Session = sessionmaker(bind=engine)

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String)

# class Workshop(Base):
#     __tablename__ = 'workshops'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     date = Column(Date)
#     duration = Column(Float)
    
# class Registration(Base):
#     __tablename__ = 'registrations'
#     id = Column(Integer, primary_key=True)
#     workshop_id = Column(Integer, ForeignKey('workshops.id'))
#     user_id = Column(Integer, ForeignKey('users.id'))
#     status = Column(String)

#     workshop = relationship("Workshop", back_populates="registrations")
#     user = relationship("User", back_populates="registrations")

# Workshop.registrations = relationship("Registration", order_by=Registration.id, back_populates="workshop")
# User.registrations = relationship("Registration", order_by=Registration.id, back_populates="user")

# Create all tables
# Base.metadata.create_all(engine)

def initialize_database():
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      # Create Users table
      c.execute('''
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE
        )
      ''')
      
      # Create Workshops table
      c.execute('''
        CREATE TABLE IF NOT EXISTS workshops (
          workshop_id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          date DATE NOT NULL,
          duration INTEGER NOT NULL
        )
      ''')
      
      # Create Registrations table
      c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
          registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
          workshop_id INTEGER NOT NULL,
          user_id INTEGER NOT NULL,
          status TEXT NOT NULL,
          FOREIGN KEY (workshop_id) REFERENCES workshops (workshop_id),
          FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
      ''')
      conn.commit()

def add_user(name, email):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
      conn.commit()

# def add_user(name, email):
#     session = Session()
#     new_user = User(name=name, email=email)
#     session.add(new_user)
#     session.commit()
#     session.close()

def add_workshop(title, date, duration):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute("INSERT INTO workshops (title, date, duration) VALUES (?, ?, ?)", (title, date, duration))
      conn.commit()

def add_registration(workshop_id, user_id, status="Registered"):
  try:
    with closing(sqlite3.connect(DATABASE)) as conn:
        c = conn.cursor()
        c.execute(
          "INSERT INTO registrations (workshop_id, user_id, status) VALUES (?, ?, ?)",
          (workshop_id, user_id, status)
        )
        conn.commit()
  except sqlite3.Error as e:
    print(f"Error adding registration: {e}")

# Functions to retrieve data (using prepared statements)
def get_all_users():
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      stmt = "SELECT * FROM users"
      c.execute(stmt)
      return c.fetchall()
# def get_all_users():
#     session = Session()
#     users = session.query(User).all()
#     session.close()
#     return users

def get_user_by_id(user_id):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
      return c.fetchone()

def get_all_workshops():
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      stmt = "SELECT * FROM workshops"
      c.execute(stmt)
      return c.fetchall()

def get_workshop_by_id(workshop_id):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute("SELECT * FROM workshops WHERE workshop_id = ?", (workshop_id,))
      return c.fetchone()

def get_registrations_by_workshop(workshop_id):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute(
        "SELECT users.user_id, users.name, registrations.status "
        "FROM registrations "
        "JOIN users ON registrations.user_id = users.user_id "
        "WHERE registrations.workshop_id = ?",
        (workshop_id,)
      )
      return c.fetchall()

def get_registrations_by_user(user_id):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute(
        "SELECT workshops.workshop_id, workshops.title, registrations.status "
        "FROM registrations "
        "JOIN workshops ON registrations.workshop_id = workshops.workshop_id "
        "WHERE registrations.user_id = ?",
        (user_id,)
      )
      return c.fetchall()

# Functions to update data
def update_user(user_id, name, email):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute("UPDATE users SET name = ?, email = ? WHERE user_id = ?", (name, email, user_id))
      conn.commit()

def update_workshop(workshop_id, title, date, duration):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute("UPDATE workshops SET title = ?, date = ?, duration = ? WHERE workshop_id = ?", (title, date, duration))
      conn.commit()

def update_registration_status(registration_id, new_status):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute(
        "UPDATE registrations SET status = ? WHERE registration_id = ?",
        (new_status, registration_id)
      )
      conn.commit()

# Functions to delete data
def delete_user(user_id):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

def delete_workshop(workshop_id):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute("DELETE FROM workshops WHERE workshop_id = ?", (workshop_id,))
      conn.commit()

def delete_registration(registration_id):
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      c.execute("DELETE FROM registrations WHERE registration_id = ?", (registration_id,))
      conn.commit()

def get_user_names_for_dropdown():
  with closing(sqlite3.connect(DATABASE)) as conn:
      c = conn.cursor()
      stmt = "SELECT user_id, name FROM users"
      c.execute(stmt)
      return c.fetchall()  # Returns a list of tuples (user_id, name)

initialize_database()

'''
DATABASE DESIGN:
1. Users
  * user_id (Primary Key, Integer, Auto-increment): Unique identifier for each user.
  * name (Text, Not Null): Full name of the user.
  * email (Text, Unique, Not Null): Email address of the user.

2. Workshops
  * workshop_id (Primary Key, Integer, Auto-increment): Unique identifier for each workshop.
  * title (Text, Not Null): Title of the workshop.
  * date (Date, Not Null): Date of the workshop.
  * duration (Integer, Not Null): Duration of the workshop in minutes.

3. Registrations
  * registration_id (Primary Key, Integer, Auto-increment): Unique identifier for each registration.
  * workshop_id (Foreign Key, References Workshops.workshop_id, Not Null): ID of the workshop.
  * user_id (Foreign Key, References Users.user_id, Not Null): ID of the user registered for the workshop.
  * status (Text, Not Null): Status of registration ('Registered', 'Canceled').
'''