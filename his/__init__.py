from flask import Flask
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] =  '5791628bb0b13ce0c676dfde280ba245'

# init the database
mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "mysql")
cur = mydb.cursor()

cur.execute('''
DROP DATABASE IF EXISTS HISDB;
CREATE DATABASE HISDB;
''', multi=True)

mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "mysql",
        database = "HISDB")
cur = mydb.cursor()


script = '''
DROP TABLE IF EXISTS scans;
DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS special_forms;
DROP TABLE IF EXISTS examinations;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;

CREATE TABLE special_forms(
    script TEXT,
    formID INT NOT NULL
);

CREATE TABLE doctors(
    doctorID INT NOT NULL UNIQUE
);

CREATE TABLE scans(
    scanID INT NOT NULL,
    state TEXT,
    date TEXT
);

CREATE TABLE patients(
    patientID INT NOT NULL UNIQUE,
    FscanID INT NOT NULL UNIQUE
);

CREATE TABLE examinations(
    FdoctorID INT NOT NULL,
    FpatientID INT NOT NULL
);

CREATE TABLE Accounts(
    name VARCHAR(50),
    phone VARCHAR(11),
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(30) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    FformID INT UNIQUE,
    FdoctorID INT UNIQUE,
    FpatientID INT UNIQUE
);
'''

cur.execute(script, multi=True)

cur.close()




from his import routes
