from his.__init__ import cur

# mydb = mysql.connector.connect(
#         host = "localhost",
#         user = "root",
#         passwd = "mysql",
#         database = "HISDB")
# cur = mydb.cursor()


def class User:
    def __init__(self, name, phone, username, password, email, FformID, DdoctorID, FpatientID):
        script = '''INSERT INTO Accounts (name, phone, username, password, email, FformID, DdoctorID, FpatientID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        val = (name, phone, username, password, email, FformID, DdoctorID, FpatientID)
        self.name = name
        self.phone = phone
        self.username = username
        self.password = password
        self.email = email
        self.FformID = FformID
        self.DdoctorID = DdoctorID
        self.FpatientID = FpatientID
        cur.execute(script, val)
        mydb.commit()
    
