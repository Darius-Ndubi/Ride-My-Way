import psycopg2

connect = psycopg2.connect("dbname='ridemyway' host='localhost' user='dario' password='riot'")
curs = connect.cursor()



#Class to add new users to the db
class DbManager(object):
      
    #class methods
    def __init__(self,email,username,password):
        
        self.email=email
        self.username=username
        self.password=password

    def signupUser(self):

        curs = connect.cursor()
        curs.execute("iNSERT INTO new_user (email,username,password) VALUES(%s,%s,%s)",(self.email,self.username,self.password))
        #save usr to db
        connect.commit()            
        curs.close()       

        
