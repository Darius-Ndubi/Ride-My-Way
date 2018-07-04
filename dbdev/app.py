from flask import Flask,request,jsonify,session
import json
from flask_restplus import Api,Resource,fields,reqparse
from models import DbManager,User
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from werkzeug.security import check_password_hash
#create an instance of flask
app=Flask(__name__)
api=Api(app)
jwt = JWTManager(app)

"""Add a secret key for the app"""
app.secret_key = '\xaa\x98\xfb\xf7\xcb\xce\xd3\xdf\x96'
app.config['JWT_SECRET_KEY'] = '\xe7\x06K\x86>\xe5\x98/\x11\x06\xfbJA-\x86'

class Manage_rides(object):
    parser = reqparse.RequestParser()

    def __init__(self):
        pass

    def get_user_login(self):

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
        self.parser.add_argument('no_seats', required=True,
                             help="Number of seats cannot be blank!")
        """self.parser.add_argument('r_id', required=True,
                            help="ID cannot be blank!")"""
        self.parser.add_argument('start_time', required=True,
                                 help="start_time cannot be blank!")
        self.parser.add_argument('arrival_time', required=True,
                            help="arrival_time cannot be blank!")
        self.parser.add_argument('ride_price', required=True,
                            help="ride_price cannot be blank!")
        self.parser.add_argument('car_lisense', required=True,
                            help="car_lisense cannot be blank!")

        self.args = self.parser.parse_args()

        return self.args

R=Manage_rides()

@api.route('/auth/signin')
class Signin(Resource):
    def post (self):
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
        
        ##check users existance in db
        self.loginuser=DbManager()

        self.exist=self.loginuser.signinusercheck(self.args['email'],self.args['email'])
            
        if self.exist:
            #print (self.exist[0][3])
            #compare the has with the one entered
            if check_password_hash(self.exist[0][3],self.args['password']):
                #if there is a match give user an access token using there registered username
                access_token = create_access_token(self.exist[0][2])
                return({self.args.email: {"Use this token to create a ride":access_token}})
            #if the hashes dont match
            else:
               return ({"Error":"Invalid password"})
        else:
            return({"Error":"User does not exist please register"})


@api.route('/rides')
class Add_ride(Resource):
    #securing endpoint with jwt_required
    #@jwt_required
    def post(self):
        self.args = R.get_ride_fields()
        #print (session[username])
        self.new_ride=User()
        #check if title to be entered exists
        self.exist=self.new_ride.checkRideExistance(self.args['title'])
        if self.exist:
            return ({"Error":"A Title like the one you want to enter exists,Let it Be unique"})
        #if ride is unique let the user post it
        else:
            #save the rides details
            self.new_ride.create_ride(car_lisense=self.args['car_lisense'],title=self.args['title'],ride_date=self.args['ride_date'],distance=self.args['distance'],no_seats=self.args['no_seats'],start_time=self.args['start_time'],arrival_time=self.args['arrival_time'],ride_price=self.args['ride_price'],creator="Yagami_Light",)
            return ({"Success":"Your ride has been created and posted"})

        
if __name__=='__main__':
    app.run(debug=True)