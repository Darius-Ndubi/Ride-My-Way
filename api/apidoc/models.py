from data import resgisterd_users, loggedin, rides, requested, responses

#several clasess t manage user input  eG Manage to manage users
#rename classes to fit responsibility
# Ride class to hold details

class AppManager(object):
    new_user = {}
    
    def __init__(self):
        pass
    
    def createUser(self, id, email, username, password):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        

    def addUserReg(self, user_data):
        self.user_data = user_data
        self.new_user={"id":self.user_data.id,"email":self.user_data.email,
                "username":self.user_data.username,
                "password":self.user_data.password}
        #resgisterd_users.append(self.new_user)
        #self.f=open('data.txt','w')
        resgisterd_users.append(self.new_user)
        
        #self.f.write(str({"Registerd": (resgisterd_users)})) 
        #self.f.close()
        


    def LoginUser(self,username, email):
        self.email = email
        self.username=username

    def addUserLogin(self,user_login):
        self.user_login = user_login
        self.new_user = { "email": self.user_login.email,
                         "username": self.user_login.username}
        loggedin.append(self.new_user)


    def __getitem__(self, user_need):
        return getattr(self, user_need)


class User(object):
    new_ride = {}

    def __init__(self):
        pass

    def create_ride(self, r_id,creator, car_license, title, ride_date,num_seats, distance, start_time, arrival_time, ride_price):
        self.r_id = r_id
        self.creator=creator
        self.car_license = car_license
        self.title = title
        self.ride_date = ride_date
        self.num_seats=num_seats
        self.distance = distance
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.ride_price = ride_price

    
    def addRide(self, ride_data):
        self.ride_data = ride_data
        self.new_ride={"r_id":self.ride_data.r_id,
            "creator":self.ride_data.creator,
            "car_license": self.ride_data.car_license,
            "title ": self.ride_data.title,
            "ride_date": self.ride_data.ride_date,
            "num_seats":self.ride_data.num_seats,
            "distance": self.ride_data.distance,
            "start_time": self.ride_data.start_time,
            "arrival_time": self.ride_data.arrival_time,
            "ride_price": self.ride_data.ride_price}
        rides.append(self.new_ride)


    def create_request(self, req_id,ride_id, title, car_reg,num_seats, dated, ride_price,creator, requester_name):
        self.req_id = req_id
        self.ride_id=ride_id
        self.title = title
        self.car_reg = car_reg
        self.num_seats=num_seats
        self.dated = dated
        self.ride_price = ride_price
        self.creator=creator
        self.requester_name = requester_name

    def addRequest(self, request_data):
        self.request_data = request_data
        self.new_ride={"req_id":self.request_data.req_id,
                       "ride_id": self.request_data.ride_id,
                       "title": self.request_data.title,
                       "car_reg": self.request_data.car_reg,
                       "num_seats":self.request_data.num_seats,
                       "dated": self.request_data.dated,
                       "ride_price": self.request_data.ride_price,
                       "creator": self.request_data.creator,
                       "requester_name": self.request_data.requester_name}

        requested.append(self.new_ride)

    def create_response(self, resp_id, ride_id, title, num_seats,creator,requester_name,action):
        self.resp_id = resp_id
        self.ride_id = ride_id
        self.title = title
        self.num_seats = num_seats
        self.creator=creator
        self.requester_name = requester_name
        self.action=action


    def addResponse(self, response_data):
        self.response_data = response_data
        self.new_ride = {"resp_id": self.response_data.resp_id,
                         "ride_id": self.response_data.ride_id,
                         "title": self.response_data.title,
                         "num_seats": self.response_data.num_seats,
                         "creator": self.response_data.creator,
                         "requester_name": self.response_data.requester_name,
                         "status": self.response_data.action}

        responses.append(self.new_ride)
