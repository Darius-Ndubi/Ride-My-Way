from flask import Flask, jsonify, request
from data import rides, requested, users
from models import Users,UsersSchema
import json
from werkzeug.exceptions import BadRequest
from flask_restplus import Api, Resource, fields, reqparse

#Create an instace of flask
app = Flask(__name__)
api = Api(app)


"""Add a secret key for the app"""
app.secret_key = '\xaa\x98\xfb\xf7\xcb\xce\xd3\xdf\x96'


#input fields
ride_fields = api.model('Ride_data', {
    'id': fields.Integer,
    'car_license': fields.String,
    'title': fields.String,
    'ride_date': fields.String,
    'distance': fields.Integer,
    'start_time': fields.String,
    'arrival_time': fields.String,
    'ride_price': fields.Integer,
    'ride_requester': fields.String

})

user_data = api.model('User SignUp', {
    'id':fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'email': fields.String
})

user_login = api.model("User SignIN", {
    'email': fields.String,
    'password': fields.String
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
            self.l.append(self.detail.get('id'))

            #for a ride to be displayed it should be in the list above
            if self.id in self.l:
                for self.ride in rides:
                    #loop through the dictionary and get the rides
                    #using .get method to pick out the ride id
                    if self.ride.get('id') == self.id:
                        #store the ride details in variable
                        self.search = self.ride
                        return self.search
            else:
                return ("Error"), 404
    
    def list_id(self):
        self.l=[]
        for self.detail in rides:

            #take all the id values and add them to thelist
            self.l.append(self.detail.get('id'))
        return self.l

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

    def get_ride_data(self):
        pass



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
        print R.get_specific_ride(id)

#Ride deletion
@api.route('/rides/<int:id>')
class Delete_ride(Resource):
    def delete(self, id):
        
        self.id = id
        #a list to store all ride ids
        self.l = []
        for self.detail in rides:

            #take all the id values and add them to thelist
            self.l.append(self.detail.get('id'))

        # Before deletion check if id is in the list
        if self.id in self.l:
            #if it is found save it to avariable for use
            self.to_delete = self.id
            #find teh ride with maching id from the rides list
            for self.ride in rides:
                if self.ride.get('id') == self.to_delete:
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


@api.route('/signup')
class Signup(Resource):
    #@api.marshal_with(user_data)
    @api.expect(user_data)
    def post(self):
        #self.email=request.json['email']


        self.args=R.get_user_dits()       
        em=self.args.get('email')
        print em
        """# without schema
        users.append(self.args)"""
       
        user = Users(id =self.args.get('id'), email=self.args.get(
            'email'),password= self.args.get('password'), username=self.args.get('username'))

        schema=UsersSchema()
        result=schema.dumps(user)
        print result
        users.append(result)

        return users


@api.route('/signin')
class Signin(Resource):
    pass

if __name__=='__main__':
    app.run(debug=True)
