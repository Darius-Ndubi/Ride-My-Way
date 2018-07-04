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
    def create_ride(self,creator, car_lisense, title, ride_date,no_seats, distance, start_time, arrival_time, ride_price):
        self.car_lisense = car_lisense
        self.title = title
        self.ride_date = ride_date
        self.no_seats=no_seats
        self.distance = distance
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.ride_price = ride_price
        self.creator=creator
        curs=connect.cursor()

        curs.execute("INSERT INTO ride (car_lisense,title,ride_date,no_seats,distance,start_time,arrival_time,ride_price,creator) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.car_lisense,self.title,self.ride_date,self.no_seats,self.distance,self.start_time,self.arrival_time,self.ride_price,self.creator))

        connect.commit()
        curs.close()
        
            




    