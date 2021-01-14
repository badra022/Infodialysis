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
DROP TABLE IF EXISTS img;
DROP TABLE IF EXISTS post;

CREATE TABLE doctor_account(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    username TEXT,
    email TEXT,
    name TEXT,
    phone TEXT,
    password TEXT
);

CREATE TABLE patient_account(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    username TEXT,
    email TEXT,
    name TEXT,
    phone TEXT,
    password TEXT
);

CREATE TABLE examinations(
    doctor_id INTEGER,
    patient_id INTEGER,
    time TEXT
);

CREATE TABLE form(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    email TEXT,
    script TEXT
);

CREATE TABLE scans(
    patient_id INTEGER,
    img_id TEXT,
    doctor_id INTEGER
);

CREATE TABLE users(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    username TEXT,
    email TEXT,
    img_id TEXT,
    type TEXT
);

CREATE TABLE img(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    img TEXT,
    imagename TEXT,
    mimetype TEXT
);

CREATE TABLE post(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    user_id INTEGER,
    post TEXT
);
'''

cur.executescript(script)
conn.commit()
cur.executescript(''' INSERT INTO users (username, email, type) VALUES ('admin', 'admin@his.com', 'admin')''')
