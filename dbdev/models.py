import psycopg2

from flask import abort,Response


connect = psycopg2.connect("dbname='ridemyway' host='localhost' user='dario' password='riot'")
curs = connect.cursor()



#Class to add new users to the db
class DbManager(object):
      
    #class methods
    def __init__(self):
        pass

    def userRegDetails(self,email,username,password):
        
        self.email=email
        self.username=username
        self.password=password

    def signinusercheck(self,email,password):
        self.email=email
        self.password=password

        curs = connect.cursor()
        #check if email exists 
        curs.execute("SELECT password FROM new_user WHERE email =%(email)s",{'email':self.email})
        self.existance = curs.fetchone()
        #print (self.existance)
        return self.existance


                
    

        
            




    