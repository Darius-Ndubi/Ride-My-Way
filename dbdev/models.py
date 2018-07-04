import psycopg2
from werkzeug.security import generate_password_hash


connect = psycopg2.connect("dbname='ridemyway' host='localhost' user='dario' password='riot'")
curs = connect.cursor()



#Class to add new users to the db
class DbManager(object):
      
    #class methods
    def __init__(self,email,username,password):
        
        self.email=email
        self.username=username
        self.password=password

    def checkUser(self):
        curs = connect.cursor()
        #check if the user exists
        curs.execute("SELECT * FROM new_user WHERE email = %(email)s",{'email':self.email})
        self.exists=curs.fetchall()
        #close connection
        curs.close()
        #return what was found
        return (self.exists)

    def signupUser(self):
        curs = connect.cursor()

        #hashing the  password
        self.passwd_hash=generate_password_hash(self.password)
        
        curs.execute("INSERT INTO new_user (email,username,password) VALUES(%s,%s,%s)",(self.email,self.username,self.passwd_hash))
        #save user to db
        connect.commit()
        #close the connection
        curs.close()

        
                    
        

        
