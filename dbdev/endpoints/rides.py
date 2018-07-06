
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from app.models import User
from flask_restplus import Api,Namespace,Resource,fields,reqparse

class Rides_fields(object):
    parser = reqparse.RequestParser()

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


R=Rides_fields()
api=Namespace("rides",description="Rides endpoints")

"""
    A class to create the ride from a logged in user adn store it in the database
    Usr is authenticated trough jwt tokens before creating a ride
"""
class Add_ride(Resource):

    #securing endpoint with jwt_required
    @jwt_required
    def post(self):
        args = R.get_ride_fields()
        username=get_jwt_identity()

        #checking if all the fields are entered
        if args['car_license'] == "":
            return ({"Error": "car License field cannot be empty"})
        elif args['title'] == "":
            return ({"Error": "The title cannot be empty"})
        elif args['ride_date']=="":
            return ({"Error":"The date of the ride cannot be empty"})
        elif args['num_seats']=="":
            return ({"Error":"The number of  available seats cannot be empty"})
        elif args['distance']=="":
            return ({"Error":"The Distance to be covered must be filled"})
        elif args['start_time']=="":
            return ({"Error":"Please specify when the ride will start"})
        elif args['arrival_time']=="":
            return ({"Error":"Estimate the time we would arrive"})
        elif args['ride_price']=="":
            return ({"Info":"Filled cant be empty but if ride is free just input 0"})
        
        new_ride=User(car_license=args['car_license'],title=args['title'],ride_date=args['ride_date'],distance=args['distance'],num_seats=args['num_seats'],start_time=args['start_time'],arrival_time=args['arrival_time'],ride_price=args['ride_price'],creator=username)
        
        exist=new_ride.checkRideExistance(args['title'])
        
        #if the ride title exists give user an error message why not to use the title
        if exist:
            return ({"Error":"A Title like the one you want to enter exists,Let it Be unique"}),406
        
        #if ride is unique let the user post it
        else:
            #save the rides details
            new_ride.create_ride()
            return ({"Success":"Your ride has been created and posted"}),200
        return ({"Error":"Token validation failure"}),403

class Get_rides(Resource):
    def get(self):
        return (User.get_rides())


class Get_ride(Resource):
    def get(self,id):
        self.id=id

        search_ride=User.get_ride(self.id)

        #if ride is found show the ride to user
        if search_ride:
            return search_ride
        else:
            return ({"Error":"Ride does not exist"}),404


class Ride_requests(Resource):
#securing endpoint with jwt_required
    @jwt_required
    def get(self,id):
        
        creator_name=get_jwt_identity()
        #print(creator_name)
        found=User.view_requests(creator_name)
        if found :
            #print(found)
            return (found)
        else:
            return ({"Error":"No requests have been made to your ride yet"}),400


    @jwt_required
    def post(self,id):
        self.id=id
        requester_name=get_jwt_identity()
        
        #find the ride if the ride exists
        search_ride=User.get_ride(self.id)
        #user cant request there own ride
        if requester_name==search_ride[0][9]:
            return ({"Error":"You cannot request your own ride"}),403
        
        User.create_requests(ride_id=search_ride[0][0],car_licence=search_ride[0][1],title=search_ride[0][2],requester_name=get_jwt_identity(),ride_date=search_ride[0][3],num_seats=search_ride[0][5],ride_price=search_ride[0][8],creator=search_ride[0][9])

        return({"Successful":"Request posted successfull"})


class Ride_response(Resource):
    #@jwt_required
    def put(self,req_id,ride_id):
        self.req_id=req_id
        exist=User.ride_reponse(req_id)
        print (exist)
        pass


        #search if the ride req_id exists







api.add_resource(Add_ride, '/rides')
api.add_resource(Get_rides, '/rides')
api.add_resource(Get_ride, '/rides/<int:id>')
api.add_resource(Ride_requests, '/rides/<int:id>/requests')
api.add_resource(Ride_response, '/rides/<int:ride_id>/requests/<int:req_id>')