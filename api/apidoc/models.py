from flask_restplus import Api, Resource,reqparse
from marshmallow import Schema, fields

class Rides(object):
    def __init__(self, id, car_license,title,ride_date,distance,start_time,arrival_time,ride_price,ride_requester):
        self.id=id 
        self.car_license=car_license
        self.title=title
        self.ride_date=ride_date
        self.distance=distance
        self.start_time=start_time
        self.arrival_time=arrival_time
        self.ride_price=ride_price
        self.ride_requester=ride_requester


class RidesSchema(Schema):
    id= fields.Int(),
    car_license= fields.Str(),
    title= fields.Str(),
    ride_date= fields.Date(),
    distance= fields.Int(),
    start_time= fields.Time(),
    arrival_time= fields.Time(),
    ride_price= fields.Int(),
    ride_requester= fields.Str()





class Users(object):
    def __init__(self,id,email,username,password):
        self.email=email
        self.username=username
        self.password=password

class UsersSchema(Schema):
    id=fields.Int()
    email=fields.Email(),
    username=fields.Str()
    password=fields.Str()


class Requests(object):
    def __init__(self):
        pass
