from flask import Flask, jsonify, request
from data import resgisterd_users, loggedin, rides, requested
from models import AppManager,User
from werkzeug.exceptions import BadRequest
from flask_restplus import Api, Resource, fields, reqparse

#Create an instace of flask
app = Flask(__name__)
api = Api(app)


"""Add a secret key for the app"""
app.secret_key = '\xaa\x98\xfb\xf7\xcb\xce\xd3\xdf\x96'


#input fields
#shows user parameters to be entered
ride_fields = api.model('Ride_data', {
    'car_license': fields.String,
    'title': fields.String,
    'ride_date': fields.String,
    'distance': fields.Integer,
    'num_seats':fields.Integer,
    'start_time': fields.String,
    'arrival_time': fields.String,
    'ride_price': fields.Integer
})

user_data = api.model('User SignUp', {
    'username': fields.String,
    'password': fields.String,
    'email': fields.String
})

user_login = api.model("User SignIN", {
    'email': fields.String,
    'password': fields.String
})

user_ride_request=api.model("Your ride request",{
   "num_seats":fields.Integer  
})


class Manage_rides(object):

    def __init__(self):
        pass

    def get_list(self):
        return rides
    
    def get_specific_ride(self, id):
        self.id = id

        #a list to store all ride ids
        self.l = []


        for self.detail in rides:

            #take all the id values and add them to thelist
            self.l.append(self.detail.get('r_id'))
             

        #for a ride to be displayed it should be in the list above
        if self.id in self.l:
            for self.ride in rides:
                #loop through the dictionary and get the rides
                #using .get method to pick out the ride id
                if self.ride.get('r_id') == self.id:
                    #store the ride details in variable
                    self.search = self.ride
                    return self.search
        #if id not found
        else:
            return jsonify({"Error":"Ride does not exist"})
    
    def get_user_dits(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required=True,
                            help="Username cannot be blank!")
        self.parser.add_argument('password', required=True,
                            help="Password cannot be blank!")
        self.parser.add_argument('email', required=True,
                            help="Email cannot be blank!")

        self.args = self.parser.parse_args()
        
        return self.args

    def get_user_login(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True,
                            help="email cannot be blank!")
        self.parser.add_argument('password', required=True,
                            help="password cannot be blank!")
        
        self.args = self.parser.parse_args()

        return self.args

    def get_ride_fields(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ride_date', required=True,
                            help="Date cannot be blank!")
        self.parser.add_argument('distance', required=True,
                            help="Distance cannot be blank!")
        self.parser.add_argument('title', required=True,
                            help="Title cannot be blank!")
        self.parser.add_argument('num_seats', required=True,
                             help="Number of seats cannot be blank!")
        """self.parser.add_argument('r_id', required=True,
                            help="ID cannot be blank!")"""
        self.parser.add_argument('start_time', required=True,
                                 help="start_time cannot be blank!")
        self.parser.add_argument('arrival_time', required=True,
                            help="arrival_time cannot be blank!")
        self.parser.add_argument('ride_price', required=True,
                            help="ride_price cannot be blank!")
        self.parser.add_argument('car_license', required=True,
                            help="car_license cannot be blank!")

        self.args = self.parser.parse_args()

        return self.args
        
    def get_request_field(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('num_seats', required=True,
                                 help="numbe rof seats cannot be blank!")
        
        self.args = self.parser.parse_args()

        return self.args



R = Manage_rides()


@api.route('/user/signup')
class Signup(Resource):
    #@api.marshal_with(user_data)
    #@api.expect(user_data)
    def post(self):
        self.args = R.get_user_dits()

        #user id creation
        self.reg_num=len(resgisterd_users)

        self.id=self.reg_num+1
        #validating that  non of the enterd fields is empty
        if self.args['email'] ==  "":
            return jsonify({"Error": "Email field cannot be empty"})
        elif self.args['username'] == "":
            return jsonify({"Error": "Username field cannot be empty"})
        elif self.args['password'] == "":
            return jsonify({"Error":"Password fields cannot be empty"})

        #check if the email has @ and .com
        elif '@' and '.com' not in self.args['email']:
            return jsonify({"Error":"Email as enterd is not valid"})

        #if all the checks above pass check if the email is already registered
        #loop through the list of users
        for self.person in resgisterd_users:
            
            if self.person.__getitem__('email') == self.args['email']:
                return jsonify({"Error": "Please use another email that one is already linked to a user"})

        
        #if the email is unique
        #register the user

        self.user = AppManager()

        self.user.createUser(id=self.id, email=self.args['email'],
                            username=self.args['username'], password=self.args['password'])

            
        self.user.addUserReg(self.user)
        
        #increment the id by one
        self.reg_num += 1
        #print (resgisterd_users)        
        return jsonify({"Success": "Registration was successfull proceed to login"})
        

#sigin user
@api.route('/user/signin')
class Signin(Resource):
    #@api.marshal_with(user_login)
    #@api.expect(user_login)
    def post(self):
        self.args = R.get_user_login()

        #validating that  non of the enterd fields is empty
        if self.args['email'] == "":
            return jsonify({"Error": "Email field cannot be empty"})
        elif self.args['password'] == "":
            return jsonify({"Error": "Password fields cannot be empty"})

        elif '@' not in self.args['email']:
            return jsonify({"Error": "Email as enterd is not valid"})
        elif '.com' not in self.args['email']:
            return jsonify({"Error": "Email as enterd is not valid"})
        """
        #check if the email has @ and .com
        self.f = open('data.txt', 'r')
        self.reg_title = self.f.readlines()
        #find the list holding registerd members
        for self.i in self.reg_title:
            self.t= self.i
        print (type(self.t))
        self.l=self.t.get('Registerd')
        print (self.l)

        """ 
        #store registered emails in a list
        self.em_regis=[]
        self.ps_regis=[] 
        for self.person in resgisterd_users:
            self.em_regis.append(self.person.get('email'))
            self.ps_regis.append(self.person.get('password'))
    
        #print (self.em_regis)
        #print (self.ps_regis)

        if self.args['email']  not in  self.em_regis:
            return jsonify({"Error": "User not resgistered"})
        #if email is found but password is not found
        elif self.args['password'] not in self.ps_regis:
            return jsonify({"Error":"Incorrect password"})
        
        
        #if user  passes all check above login the user
        #get users user name
        for self.person in resgisterd_users:
            if self.person.get('email')==self.args['email']:
                self.uname=self.person.__getitem__('username')
       
        
        
        #login the user
        self.user = AppManager()

        #find the number of users
        self.num_users=len(loggedin)
        
        
        self.user.LoginUser(email=self.args['email'], username=self.uname)

        self.user.addUserLogin(self.user)

        self.new_numusers=len(loggedin)
        #check if user data is captured
        if self.num_users+1 == self.new_numusers:
            #print (loggedin)
            return jsonify ({"Success":"Welcome back...."+self.uname})

        else:
            return jsonify ({"Error":"You are not logged in, Please try again"})
        

@api.route('/user/addride')
class Add_ride(Resource):
    #@api.marshal_with(ride_fields)
    #@api.expect(ride_fields)
    def post(self):
        self.args = R.get_ride_fields()

        #check if a user is logged in beffore creating a ride
        if len(loggedin)==0:
            return jsonify({"Error":"Your are not logged in"})
           
        for self.i in loggedin:
            self.uname = self.i.get('username')
        print(self.uname)

        #find the number of rides that already exist
        self.ride_num = len(rides)

        self.args['r_id'] = self.ride_num+1

        #Create an instance of User class
        self.new_ride = User()

        self.new_ride.create_ride(r_id=self.args['r_id'],
                                    creator=self.uname,
                                    car_license=self.args['car_license'],
                                    title=self.args['title'],
                                    ride_date=self.args['ride_date'],
                                    num_seats=int(self.args['num_seats']),
                                    distance=self.args['distance'],
                                    start_time=self.args['start_time'],
                                    arrival_time=self.args['arrival_time'],
                                    ride_price=self.args['ride_price'])
        
        #see if ride existing has a matching title
        for self.ride in rides:
            if self.ride.get("title") == self.args['title']:
                return jsonify({"Error": "Let your title be unique, a Ride with a like yours  exists"})


        self.new_ride.addRide(self.new_ride)
            
        self.ride_num += 1

        #after adding a ride you should be shown a all the rides you have created
        self.your_rides=[]
        for self.ride in rides:
            if self.ride.get('creator')==self.uname:
                self.your_rides.append(self.ride)
        print (rides)
        return self.your_rides

@api.route('/user/rides/<int:id>')
class Delete_ride(Resource):
    def delete(self, id):

        self.id = id

        #a list to store all ride ids
        self.l = []
        for self.detail in rides:
            #take all the id values and add them to thelist
            self.l.append(self.detail.get('r_id'))
        
        print ("ids")
        print (self.l)

        if self.id not in self.l:
            return jsonify({"Error": "Ride does not exist"})

        #check if the uses is logged in
        if len(loggedin) == 0:
            return jsonify({"Error": "You are not logged in to delete this ride"})

        else:
            #get users username
            for self.i in loggedin:
                    self.uname = self.i.get('username')
            print(self.uname)
       
        #check if the ride has the users uname
        if self.id in self.l:
            for self.ride in rides:
                if self.ride.get('creator') == self.uname and self.ride.get('r_id') == self.id:
                    print self.ride
                    self.ride_index = rides.index(self.ride)
                    rides.pop(self.ride_index)
                    return ("Success"), 200
            
            return ({"Error":"Ride not linked to your account"})
        
        else:
            return jsonify({"Error":"Ride not linked to your account"})


@api.route('/user/rides/requests/<int:id>')
class Request_Ride(Resource):
    #@api.marshal_with(user_ride_request)
    #@api.expect(user_ride_request
    def post(self,id):
        self.args = R.get_request_field()
        self.id =id
        self.l=[]
        
        #check if a user is logged in before requesting a ride
        if len(loggedin) == 0:
            return jsonify({"Error": "Your are not logged in"})
        #if the user is logged in find thre username
        for self.i in loggedin:
            self.uname = self.i.get('username')
        print(self.uname)
        
        """
        #data  can be entered as
        {
            "num_seats":2
        }
        """

        #find all ride ids
        for self.ride in rides:
            self.l.append(self.ride.get('r_id'))
        
        #id id entered equals any id searcged previously
        #find the ride
        #try to find the id in the list
        if self.id in self.l:
            #if it passes locate the ride
            for self.ride in rides:
                if self.ride.get('r_id')== self.id:
                    
                    #pick the fields needed
                    self.ride_id=self.ride.get('r_id')
                    self.ride_title=self.ride.get('title')
                    self.num_seats=self.ride.get('num_seats')
                    self.car_reg = self.ride.get('car_license')
                    self.dated = self.ride.get('ride_date')
                    self.ride_price=self.ride.get('ride_price')
                    self.creator=self.ride.get('creator')
                    
                    #find the number of requests that already exist
                    self.req_num = len(requested)

                    #create arequests id based on the number of requests existing
                    self.req_id= self.req_num+1

                    self.new_req=User()
                    self.new_req.create_request(req_id=self.req_id,ride_id=self.ride_id,
                                                title=self.ride_title, num_seats=int(self.args['num_seats']),
                                                car_reg=self.car_reg,dated=self.dated,
                                                ride_price=self.ride_price, creator=self.creator,
                                                requester_name=self.uname)

                    self.new_req.addRequest(self.new_req)

                    self.req_num += 1
                    #print (requested)
                    return jsonify({"Success":"Your request has been created and posted"})
                
        else:
            return jsonify({"Sorry":"The ride you would likse to request doesnt exist"})

########------------------not up to work yet -----------#
#--not up to task yet ----#
@api.route('/user/rides/responses/<string:action>')
class Request_Ride(Resource):
    #to dislpay all the ride requests
    def get(self):
        """
        #check if the user is logged in and if logged in pick their username
        if len(loggedin) == 0:
            return jsonify({"Error": "Your are not logged in"})
        
        for self.i in loggedin:
            self.uname = self.i.get('username')
        print(self.uname)
        """
        #load all the ride requests

        for self.requestss in requested:
            if self.requestss.get('creator') == 'Yagami Light':
                return jsonify({self.requestss})
        pass
        

    def post(self, id,action):
        self.id =id
        self.action=action
        """
        #check if the user is logged in and if logged in pick their username
        if len(loggedin) == 0:
            return jsonify({"Error": "Your are not logged in"})
        
        for self.i in loggedin:
            self.uname = self.i.get('username')
        print(self.uname)
        """
        pass
        
        


#show user ride history since login
@api.route('/user/profile')
class User_Profile(Resource):
    def get(self):
        """
        #check if the user is logged in and if logged in pick their username
        if len(loggedin) == 0:
            return jsonify({"Error": "Your are not logged in"})

        for self.i in loggedin:
            self.uname = self.i.get('username')
        print(self.uname)
        """
        #---showing list of rides user as created -----#
        self.your_rides=[]
        for self.ride in rides:
            if self.ride.get('creator')=="Yagami Light":
                self.your_rides.append(self.ride)
        return jsonify({"Your Rides":self.your_rides})

#endpoint for user edit ride
#endpoint for user signou#
#------------------end of block to be fixed --------#


#a visitor can
@api.route('/rides')
class View_rides(Resource):
    def get(self):
        return R.get_list()


#A visitoe can 
@api.route('/ride/<int:id>')
class View_ride(Resource):
    def get(self, id):
        #loop through the rides and find ride with the id
        return R.get_specific_ride(id)


if __name__=='__main__':
    app.run(debug=True)
