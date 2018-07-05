import psycopg2

from flask import abort,Response,jsonify


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
        curs.execute("SELECT * FROM new_user WHERE email =%(email)s",{'email':self.email})
        #find the whole row
        self.existance = curs.fetchall()
        #print (self.existance)
        
        return self.existance


#class user to show the responsibilities of s user
class User(object):


    #class constructor
    def __init__(self):
        pass

    #method to query if ride exists
    def checkRideExistance(self,title):
        self.title=title
        curs=connect.cursor()
        curs.execute("SELECT * FROM ride WHERE title=%(title)s",{'title':self.title})
        self.existance = curs.fetchone()
        
        return self.existance
     
    #create a ride method for user
    def create_ride(self,creator, car_license, title, ride_date,num_seats, distance, start_time, arrival_time, ride_price):
        self.car_license = car_license
        self.title = title
        self.ride_date =ride_date
        self.num_seats=num_seats
        self.distance = distance
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.ride_price = ride_price
        self.creator=creator
        #ensuring that all field are enterd

        curs=connect.cursor()
        
        curs.execute("INSERT INTO ride (car_license,title,ride_date,num_seats,distance,start_time,arrival_time,ride_price,creator) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.car_license,self.title,self.ride_date,self.num_seats,self.distance,self.start_time,self.arrival_time,self.ride_price,self.creator))

        connect.commit()
        curs.close()

    #method to find all rides in db
    def get_rides(self):
        curs=connect.cursor()
        curs.execute("SELECT * FROM ride")
        self.rides=curs.fetchall()
        #print (self.rides)
        curs.close()
        return jsonify(self.rides)

    #method to find specific ride in db
    def get_ride(self,search_id):
        self.search_id=search_id
        
        #locate ride with the matching id in the db and return it (email)s",{'email':self.email}
        curs=connect.cursor()
        curs.execute("SELECT * FROM ride WHERE r_id=%(r_id)s",{'r_id':self.search_id})
        #get the whole row
        self.found=curs.fetchall()
        #print (self.found)
        return self.found

    
        
            




    