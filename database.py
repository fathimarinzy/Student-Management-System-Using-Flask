import sqlite3
connection=sqlite3.connect("studentmanagement.db")
cursor = connection.cursor()
print("database created")


cursor.execute("CREATE TABLE  Login(loginid INTEGER PRIMARY KEY AUTOINCREMENT,username text,password varchar,usertype text,status integer)") 
print("logintable created")

cursor.execute("""
CREATE TABLE Student (
    studid INTEGER PRIMARY KEY AUTOINCREMENT,
    logid INTEGER,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    address TEXT,
    phone_number BIGINT,
    guardian TEXT,
    FOREIGN KEY (logid) REFERENCES Login(loginid)
)
""")
print("studenttable created")

cursor.execute("""
CREATE TABLE Teacher (
    teachid INTEGER PRIMARY KEY AUTOINCREMENT,
    logid INTEGER,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    address TEXT,
    phone_number BIGINT,
    salary FLOAT,
    experience INTEGER,
    FOREIGN KEY (logid) REFERENCES Login(loginid)
)
""")
print("teachertable created")




# cursor.execute("DROP TABLE IF EXISTS Login")
# connection.commit()
# print("deleted")