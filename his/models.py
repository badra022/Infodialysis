import sqlite3

class User:
    def __init__(self, username, email, img_file, type):
        self.username = username
        self.email = email
        self.img_file = img_file
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
        return f"User('{self.username}', '{self.email}', '{self.image_file}','{self.type}')"

    @classmethod
    def get_by_id(self, user_id):
        ## init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        q_res = cur.execute('''
        SELECT username, email, img_file, type FROM users WHERE id = ?
        ''', (user_id,)).fetchone()
        u = User(q_res[0], q_res[1], q_res[2], q_res[3])
        return u

    @classmethod
    def getUser(self, email):
        # # init the database
        conn = sqlite3.connect('database.sqlite')
        cur = conn.cursor()
        print("retrieving the user account from doctors and patients accounts....")
        cur.execute('''SELECT username, email FROM doctor_account WHERE email=?''', (email,))
        try:
            result = cur.fetchone()
            return User(result[0], result[1], 'None', 'doctor')
        except:
            pass
        cur.execute('''SELECT username, email FROM patient_account WHERE email=?''', (email,))
        try:
            result = cur.fetchone()
            return User(result[0], result[1], 'None', 'patient')
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
