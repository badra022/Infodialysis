import sqlite3
from services import bcrypt
from werkzeug.utils import secure_filename
from flask import request

# sqlite scripts that handles the insertion to the system database
newDoctorAccountScript = '''INSERT INTO doctor_account (username,email,name,phone,password) VALUES (?,?,?,?,?)'''
newPatientAccountScript = '''INSERT INTO patient_account (username,email,name,phone,password) VALUES (?,?,?,?,?)'''
newUserScript = '''INSERT INTO users (username, email,type) VALUES (?,?,?)'''



class User:
    def __init__(self, username, email, type):
        self.username = username
        self.email = email
        self.type = type
        ## init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute('''
        SELECT id FROM users WHERE username = ? AND email = ?
        ''', (self.username, self.email, ))
        # conn.commit()
        try:
            self.id = cur.fetchone()[0]
        except:
            self.id = -1

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.type}')"

    @classmethod
    def get_by_id(self, user_id):
        ## init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        q_res = cur.execute('''
        SELECT username, email,type FROM users WHERE id = ?
        ''', (user_id,)).fetchone()
        try:
            u = User(q_res[0], q_res[1], q_res[2])
        except:
            u = User('admin', 'admin@his.com', 'admin')
        return u

    @classmethod
    def getUser(self, email):
        # # init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        print("retrieving the user account from doctors and patients accounts....")
        cur.execute('''SELECT username, email, type FROM users WHERE email=?''', (email,))
        try:
            result = cur.fetchone()
            return User(result[0], result[1], result[2])
        except:
            pass
        return None

    @classmethod
    def getPassword(self, user):
        # # init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT password FROM doctor_account WHERE email=?''', (user.email,))
        try:
            return cur.fetchone()[0]
        except:
            pass
        cur.execute('''SELECT password FROM patient_account WHERE email=?''', (user.email,))
        try:
            return cur.fetchone()[0]
        except:
            pass
        pass


class Image:
    def __init__(self, img, name, mimetype):
        self.img = img
        self.name = name
        self.mimetype = mimetype

    @classmethod
    def create(self, pic, email):
        # pic = request.files[imgVarName]

        if not pic:
            return False
        self.filename = secure_filename(pic.filename)
        self.mimetype = pic.mimetype
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        Image.delete(email)
        cur.execute('''INSERT INTO img (img, imagename, mimetype,email) VALUES (?,?,?,?)''' ,
         (pic.read(),self.filename,self.mimetype,email, ) )
        conn.commit()
        cur.execute('''SELECT img.id FROM img WHERE email = ?''', (email, ))
        id = cur.fetchone()[0]
        print(id, '*********************************************')
        cur.execute('''UPDATE users SET img_id = ? WHERE email = ?''',(id,email, ) )
        conn.commit()

    @classmethod
    def delete(self, email):
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute('''DELETE FROM img WHERE email = ?''' ,(email, ) )
        conn.commit()
        cur.execute('''UPDATE users SET img_id = NULL WHERE email = ?''',(email, ) )
        conn.commit()



class Account:

    @classmethod
    def create(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key == 'username':
                    self.username = value
                if key == 'email':
                    self.email = value
                if key == 'name':
                    self.name = value
                if key == 'phone':
                    self.phone = value
                if key == 'password':
                    self.password = value
                # if key == 'img_id':
                    # self.username = value
                if key == 'type':
                    self.type = value
        else:
            pass
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        hashed_password = bcrypt.generate_password_hash(self.password).decode('utf-8')
        if self.type == 'patient':
            cur.execute(newPatientAccountScript, (self.username,
                                                 self.email,
                                                 self.name,
                                                 self.phone,
                                                 hashed_password, ))
            conn.commit()
            cur.execute(newUserScript, (self.username ,self.email , 'patient', ))
            conn.commit()
        elif self.type == 'doctor':
            cur.execute(newDoctorAccountScript, (self.username,
                                                 self.email,
                                                 self.name,
                                                 self.phone,
                                                 hashed_password, ))
            conn.commit()
            cur.execute(newUserScript, (self.username ,self.email , 'doctor', ))
            conn.commit()

    @classmethod
    def validate_username(self, username):
        # get a similar field in mydb
        # init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM users WHERE username = ?''', (username, ))
        try:
            return cur.fetchone()[0]
        except:
            return False

    @classmethod
    def validate_email(self, email):
        # get a similar field in mydb
        # init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM users WHERE email = ?''', (email, ))
        try:
            return cur.fetchone()[0]
        except:
            return False

    @classmethod
    def get_img(self, email):
        # get a similar field in mydb
        # init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT img.img, img.imagename, img.mimetype  FROM img WHERE email = ?''', (email, ))
        try:
            result = cur.fetchone()
            return Image(result[0], result[1], result[2])
        except:
            return False


    @classmethod
    def set_img(self, email, pic):
        Image.create(pic, email)

    @classmethod
    def update_img(self, email, pic):
        Image.delete(email)
        Image.create(pic, email)
