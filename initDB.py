import sqlite3

# init the database
conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

script = '''
DROP TABLE IF EXISTS scans;
DROP TABLE IF EXISTS doctor_account;
DROP TABLE IF EXISTS form;
DROP TABLE IF EXISTS examinations;
DROP TABLE IF EXISTS patient_account;
DROP TABLE IF EXISTS users;

CREATE TABLE doctor_account(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    username TEXT,
    email TEXT,
    name TEXT,
    phone TEXT,
    password TEXT,
    form_id INTEGER
);

CREATE TABLE patient_account(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    username TEXT,
    email TEXT,
    name TEXT,
    phone TEXT,
    password TEXT,
    form_id INTEGER
);

CREATE TABLE examinations(
    doctor_id INTEGER,
    patient_id INTEGER
);

CREATE TABLE form(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    email TEXT,
    script TEXT
);

CREATE TABLE scans(
    patient_id INTEGER,
    file_link TEXT
);

CREATE TABLE users(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    username TEXT,
    email TEXT,
    img_file TEXT,
    type TEXT
);
'''

cur.executescript(script)
