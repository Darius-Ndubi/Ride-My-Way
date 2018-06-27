from flask import Flask,jsonify,request
from data import rides,requested,users
import json
from flask_restplus import Api, Resource, fields,reqparse



#Create an instace of flask
app=Flask(__name__)
api = Api(app)




"""Add a secret key for the app"""
app.secret_key = '\xaa\x98\xfb\xf7\xcb\xce\xd3\xdf\x96'

#input fields
ride_fields=api.model('Ride_data',{
    'id':fields.Integer,
    'car_license': fields.String,
    'title': fields.String,
    'ride_date': fields.String,
    'distance': fields.Integer,
    'start_time': fields.String,
    'arrival_time': fields.String,
    'ride_price': fields.Integer,
    'ride_requester':fields.String

})

user_data=api.model('User SignUp',{
    'email':fields.String,
    'username':fields.String,
    'password':fields.String
})

user_login=api.model("User SignIN",{
    'email':fields.String,
    'password':fields.String
})

class Get_rides(object):

    all_rides={}

    def __init__(self):
        pass

    def get_list(self):
        return rides
    
    def get_specific_ride(self,id):
        self.id=id

        for self.ride in rides:
            #loop through the dictionary and get the rides
            #using .get method to pick out the ride id
            if self.ride.get('id') == self.id:
                #store the ride details in variable
                self.search = self.ride
                # return the data in json format
                return self.search

            

R=Get_rides()


@api.route('/allrides')
class View_rides(Resource):
    def get(self):
        return R.get_list()
    
    @api.marshal_with(ride_fields)
    @api.expect(ride_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ride_date', required=True,
                            help="Date cannot be blank!")
        parser.add_argument('distance', required=True,
                            help="Distance cannot be blank!")
        parser.add_argument('title', required=True,
                            help="Title cannot be blank!")
        parser.add_argument('id', required=True,
                            help="ID cannot be blank!")
        parser.add_argument('arrival_time', required=True,
                            help="arrival_time cannot be blank!")
        parser.add_argument('ride_price', required=True,
                            help="ride_price cannot be blank!")
        parser.add_argument('car_license', required=True,
                            help="car_license cannot be blank!")
        parser.add_argument('ride_requester', required=True,
                            help="ride_request cannot be blank!")
        
        args = parser.parse_args()
        rides.append(args)
        #print args['ride_date']
        return rides
        

#show details of a ride
@api.route('/oneride/<int:id>')
class View_ride(Resource):
    def get(self,id):
        #loop through the rides and find ride with the id
        return R.get_specific_ride(id)

#create a ride
@api.route('/rides')
class Add_ride(Resource):
    @api.marshal_with(ride_fields)
    @api.expect(ride_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ride_date', required=True,
                            help="Date cannot be blank!")
        parser.add_argument('distance', required=True,
                        help="Distance cannot be blank!")
        parser.add_argument('title', required=True,
                            help="Title cannot be blank!")
        parser.add_argument('id', required=True,
                            help="ID cannot be blank!")
        parser.add_argument('arrival_time', required=True,
                            help="arrival_time cannot be blank!")
        parser.add_argument('ride_price', required=True,
                            help="ride_price cannot be blank!")
        parser.add_argument('car_license', required=True,
                            help="car_license cannot be blank!")

        args = parser.parse_args()
        rides.append(args)
        #print args['ride_date']
        return rides

       
#Ride deletion
@api.route('/rides/<int:id>')
class Delete_ride(Resource):
    def delete(self,id):
        self.id=id 

        for self.ride in rides:
            
            if self.ride.get('id') == self.id:
                self.to_delete = self.ride
                print self.to_delete
                #find the index of the ride
                self.ride_index = rides.index(self.to_delete)

                #delete the ride entry
                rides.pop(self.ride_index)

            return 'Success'

@api.route('/rides/edit/<int:id>')
class Edit_ride(Resource):
    @api.marshal_with(ride_fields)
    @api.expect(ride_fields)
    def put(self,id):        
        parser = reqparse.RequestParser()
        parser.add_argument('ride_date', required=True,
                            help="Date cannot be blank!")
        parser.add_argument('distance', required=True,
                            help="Distance cannot be blank!")
        parser.add_argument('title', required=True,
                            help="Title cannot be blank!")
        parser.add_argument('id', required=True,
                            help="ID cannot be blank!")
        parser.add_argument('arrival_time', required=True,
                            help="arrival_time cannot be blank!")
        parser.add_argument('ride_price', required=True,
                            help="ride_price cannot be blank!")
        parser.add_argument('car_license', required=True,
                            help="car_license cannot be blank!")
        parser.add_argument('ride_requester', required=True,
                            help="car_license cannot be blank!")

        args = parser.parse_args()
        
        for self.ride in rides:
            if self.ride.get('id')==args['id']:
                rides.append(args)
                return rides         

@api.route('/signup')
class Signup(Resource):
    @api.marshal_with(user_data)
    @api.expect(user_data)
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help="Username cannot be blank!")
        parser.add_argument('password', required=True,
                            help="Password cannot be blank!")
        parser.add_argument('email', required=True,
                            help="Email cannot be blank!")
        
        args = parser.parse_args()
        
        users.append(args)
        return users
        
@api.route('/signin')
class Signin(Resource):
    @api.marshal_with(user_login)
    @api.expect(user_login)
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('password', required=True,
                            help="password cannot be blank!")
        parser.add_argument('email', required=True,
                            help="email cannot be blank!")
        args = parser.parse_args()
        
        for self.user in users:
            if self.user.get('password')==args['password']:
                return args


if __name__=='__main__':
    app.run(debug=True)
