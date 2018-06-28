from data import users,rides,requested


class Users(object):

    def __init__(self, email, username, password):

        self.email = email
        self.username = username
        self.password = password

    def addUser(self, user_data):
        self.user_data = user_data
        users.append(self.user_data)

    def __getitem__(self, user_detail):
        return getattr(self, user_detail)


class Rides(object):
    
    def __init__(self, r_id, car_license,title,ride_date,distance,start_time,arrival_time,ride_price):
        self.r_id=r_id 
        self.car_license=car_license
        self.title=title
        self.ride_date=ride_date
        self.distance=distance
        self.start_time=start_time
        self.arrival_time=arrival_time
        self.ride_price=ride_price
        

    #should be under user class
    def addRide(self,ride_data):
        self.ride_data=ride_data
        rides.append(self.ride_data)

    def __getitem__(self, ride_detail):
        return getattr(self, ride_detail)


class RequestedRides(object):
    def __init__(self,req_id,title,car_reg,dated,ride_price, requester_name):
        self.req_id=req_id
        self.title=title
        self.car_reg=car_reg
        self.dated=dated
        self.ride_price=ride_price
        self.requester_name=requester_name

        
    def addRequest(self,request_data):
        self.request_data=request_data
        requested.append(self.request_data)
