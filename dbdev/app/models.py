import psycopg2
from flask_jwt_extended import create_access_token
from flask import abort,Response,jsonify
from werkzeug.security import check_password_hash,generate_password_hash

connect = psycopg2.connect("dbname='ridemyway' host='localhost' user='dario' password='riot'")
curs = connect.cursor()


"""
    A class to handle the registration of users
    The login of users to the site
"""
class DbManager(object):
    def __init__(self,email,username,password):
        self.email=email
        self.password=password
        self.username=username

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

    @staticmethod
    def login(email,password):
        exist=signinusercheck(email)
        if exist:
            #print (self.exist[0][3])
            #compare the has with the one entered
            if check_password_hash(exist[0][3],password):
                #if there is a match give user an access token using there registered username
                access_token = create_access_token(exist[0][2])
                return({exist[0][2]: {"Use this token to create a ride":access_token}})
            #if the hashes dont match
            else:
               return ({"Error":"Invalid password"})
        else:
            return({"Error":"User does not exist please register"})

    
    
def signinusercheck(email):

        curs = connect.cursor()
        #check if email exists 
        curs.execute("SELECT * FROM new_user WHERE email =%(email)s",{'email':email})
        #find the whole row
        existance = curs.fetchall()
        #print (existance)
        
        return existance


#class user to show the responsibilities of s user
class User(object):


    #class constructor
    def __init__(self,creator, car_license, title, ride_date,num_seats, distance, start_time, arrival_time, ride_price):
        self.car_license = car_license
        self.title = title
        self.ride_date =ride_date
        self.num_seats=num_seats
        self.distance = distance
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.ride_price = ride_price
        self.creator=creator
        

    #method to query if ride exists
    def checkRideExistance(self,title):
        self.title=title
        curs=connect.cursor()
        curs.execute("SELECT * FROM ride WHERE title=%(title)s",{'title':self.title})
        self.existance = curs.fetchone()
        return self.existance

     
    #create a ride method for user
    def create_ride(self,):
        curs=connect.cursor()
        
        curs.execute("INSERT INTO ride (car_license,title,ride_date,num_seats,distance,start_time,arrival_time,ride_price,creator) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.car_license,self.title,self.ride_date,self.num_seats,self.distance,self.start_time,self.arrival_time,self.ride_price,self.creator))

        connect.commit()
        curs.close()

    #method to find all rides in db
    @staticmethod
    def get_rides():
        curs=connect.cursor()
        curs.execute("SELECT * FROM ride")
        rides=curs.fetchall()
        #print (self.rides)
        curs.close()
        return jsonify(rides)

    #method to find specific ride in db
    @staticmethod
    def get_ride(search_id):
        #locate ride with the matching id in the db and return it (email)s",{'email':self.email}
        curs=connect.cursor()
        curs.execute("SELECT * FROM ride WHERE r_id=%(r_id)s",{'r_id':search_id})
        #get the whole row
        found=curs.fetchall()
        #print (self.found)
        return found
    
    @staticmethod
    def create_requests(ride_id,car_licence,requester_name,ride_date,title,num_seats,ride_price,creator):
        curs=connect.cursor()
        curs.execute("INSERT INTO requestss (ride_id,car_license,requester_name,ride_date,title,num_seats,ride_price,creator) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(ride_id,car_licence,requester_name,ride_date,title,num_seats,ride_price,creator))
        connect.commit()
        curs.close()
    
    @staticmethod
    def view_requests(creator):
        curs=connect.cursor()
        curs.execute("SELECT * FROM requestss WHERE creator=%(creator)s",{'creator':creator})
        rows=curs.fetchall()
        if rows:
            for i in rows:
                for j in i:
                    if j == creator:
                       your_ride=i 
            return [your_ride]
        elif rows is None:
            return ({"Info":"You have not created any ride"}),204
        else:
            return ({"Info":"No requests have been made to your rides yet"}),204
    
    
    @staticmethod
    def ride_reponse(req_id):
        curs=connect.cursor()
        curs.execute("SELECT * FROM requestss WHERE req_id=%(req_id)s and ride_id=%(ride_id)s",{'req_id':req_id,'ride_id':req_id})
        row=curs.fetchall()
        if row:
            return row
        else:
            return ({"Error":"Request not found"}),404
