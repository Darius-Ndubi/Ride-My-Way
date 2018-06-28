from flask import Flask, jsonify, request
from data import rides, requested, users
from models import Users, Rides, RequestedRides
import json
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
    'r_id': fields.Integer,
    'car_license': fields.String,
    'title': fields.String,
    'ride_date': fields.String,
    'distance': fields.Integer,
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
    'req_id':fields.Integer,
    'title': fields.String,
    'car_reg': fields.String,
    'dated': fields.String,
    'ride_price': fields.Integer,
    'requester_name':fields.String
    
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
            self.l.append(self.detail.__getitem__('r_id'))
             

        #for a ride to be displayed it should be in the list above
        if self.id in self.l:
            for self.ride in rides:
                #loop through the dictionary and get the rides
                #using .get method to pick out the ride id
                if self.ride.__getitem__('r_id') == self.id:
                    #store the ride details in variable
                    self.search = self.ride
                    return self.search
            else:
                return ("Error"), 404
    
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
        self.parser.add_argument('r_id', required=True,
                            help="ID cannot be blank!")
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

        self.parser.add_argument('req_id', required=True,
                                 help=" cannot be blank!")
        self.parser.add_argument('title', required=True,
                                 help="title cannot be blank!")
        self.parser.add_argument('car_reg', required=True,
                                 help="Car registration cannot be blank!")
        self.parser.add_argument('dated', required=True,
                                 help="Date cannot be blank!")
        self.parser.add_argument('ride_price', required=True,
                                 help="Your name cannot be blank!")
        self.parser.add_argument('requester_name', required=True,
                                 help="Your name cannot be blank!")
        self.args = self.parser.parse_args()

        return self.args



R = Manage_rides()

@api.route('/allrides')
class View_rides(Resource):
    def get(self):
        return R.get_list()

#show details of a ride
@api.route('/oneride/<int:id>')
class View_ride(Resource):
    def get(self, id):
        #loop through the rides and find ride with the id
        return R.get_specific_ride(id)

#Ride deletion
@api.route('/user/rides/<int:id>')
class Delete_ride(Resource):
    def delete(self, id):
        
        self.id = id
        #a list to store all ride ids
        self.l = []
        for self.detail in rides:

            #take all the id values and add them to thelist
            self.l.append(self.detail.__getitem__('r_id'))

        # Before deletion check if id is in the list
        if self.id in self.l:
            #find the ride with maching id from the rides list
            for self.ride in rides:
                if self.ride.__getitem__('r_id') == self.id:
                    self.ride_index = rides.index(self.ride)
                    
                    rides.pop(self.ride_index)
                    return ("Success"), 200

        #if id is not in list, Error out
        #error in restplus
        else:
            #return jsonify({"404": {"Error": "Ride id not found"}})
            e = BadRequest('Unfound ID')
            e.data = {'Reason': 'Ride is not found since its been already deleted or does not exist'}
            raise e


@api.route('/user/signup')
class Signup(Resource):
    @api.marshal_with(user_data)
    @api.expect(user_data)
    def post(self):
        self.args=R.get_user_dits()

        self.user=Users(email=self.args['email'],
                        username=self.args['username']
                        ,password=self.args['password']) 

        self.user.addUser(self.user)      
  
        return  users

#sigin
@api.route('/user/signin')
class Signin(Resource):
    @api.marshal_with(user_login)
    @api.expect(user_login)
    def post(self):
        self.args = R.get_user_login()

        for self.i in users:
            if str(self.i.__getitem__('password')) == str(self.args['password']):
                return self.args
            
        
        e = BadRequest('Wrong password')
        e.data = {'Reason': 'Password is wrong or you are not registered'}
        raise e

#create a ride
@api.route('/rides')
class Add_ride(Resource):
    @api.marshal_with(ride_fields)
    @api.expect(ride_fields)
    def post(self):
        self.args=R.get_ride_fields()

        #find the number of rides that already exist
        self.ride_num = len(rides)
        
        self.real_id = self.ride_num+1
        self.args['r_id'] = self.real_id

        
        #user should be able to add a ride not this way
        #Ride should not add itself
        #Use a 
        self.new_ride = Rides(r_id=self.args['r_id'],
                            car_license=self.args['car_license'],
                            title=self.args['title'],
                            ride_date=self.args['ride_date'],
                            distance=self.args['distance'],
                            start_time=self.args['start_time'],
                            arrival_time=self.args['arrival_time'],
                            ride_price=self.args['ride_price'])

        self.new_ride.addRide(self.new_ride)

        self.ride_num += 1
        

        return rides

#user should not add them selves in

@api.route('/rides/edit/<int:id>')
class Edit_ride(Resource):
    @api.marshal_with(ride_fields)
    @api.expect(ride_fields)
    def put(self, id):
        self.id=id

        self.args = R.get_ride_fields()
        
        #check id any If
        for self.ride in rides:
            
            if self.ride.__getitem__('r_id')==self.id:
                self.args['r_id']=self.id
                
                #accept data from user
                self.edited_ride = Rides(r_id=self.args['r_id'],
                                        car_license=self.args['car_license'],
                                        title=self.args['title'],
                                        ride_date=self.args['ride_date'],
                                        distance=self.args['distance'],
                                        start_time=self.args['start_time'],
                                        arrival_time=self.args['arrival_time'],
                                        ride_price=self.args['ride_price'])
                
                self.id = id
                #a list to store all ride ids
                self.l = []
                for self.detail in rides:
                    #take all the id values and add them to thelist
                    self.l.append(self.detail.__getitem__('r_id'))

                # Before deletion check if id is in the list
                if self.id in self.l:
                    #find the ride with maching id from the rides list
                    for self.ride in rides:
                        if self.ride.__getitem__('r_id') == self.id:
                            self.ride_index = rides.index(self.ride)

                            rides.pop(self.ride_index)
                        

                #save the data
                self.edited_ride.addRide(self.edited_ride)

                return rides
                

@api.route('/user/rides/request/<int:id>')
class Requset_ride(Resource):
    @api.marshal_with(user_ride_request)
    @api.expect(user_ride_request)
    def post(self, id):
        self.args = R.get_request_field()
        self.id = id
        self.l = []
        
        for self.detail in rides:
            #take all the id values and append them to thelist
            self.l.append(self.detail.__getitem__('r_id'))
            # Before requesting  check if id is in the list
        if self.id in self.l:
            #find the ride with maching id from the rides list
            for self.ride in rides:
                if self.ride.__getitem__('r_id') == self.id:

                    #get the required fields to fill request data
                    self.ride_title = self.ride.__getitem__('title')

                    self.car_reg = self.ride.__getitem__('car_license')

                    self.dated = self.ride.__getitem__('ride_date')
                    self.ride_price = self.ride.__getitem__('ride_price')
        
        self.args = R.get_request_field()

        self.args['req_id']=self.id
        
        self.args['title'] = self.ride_title
        
        self.args['car_reg'] = self.car_reg
    
        self.args['dated'] = self.dated
        self.args['ride_price'] = self.ride_price

        self.ride_req = RequestedRides(req_id=self.args['req_id'], title=self.args['title'], car_reg=self.args['car_reg'],
                                       dated=self.args['dated'], ride_price=self.args['ride_price'],
                                       requester_name=self.args['requester_name'])

        self.ride_req.addRequest(self.ride_req)

        return requested

if __name__=='__main__':
    app.run(debug=True)
