from flask import Flask,jsonify,request
from app import app
from data import rides,requested,users
import json



"""Endpoint to view all rides"""
@app.route('/api/v1/rides',methods=['GET'])
def view_rides():
    #get all titles
    #new dictionary to add id and title
    all_rides = {}
    #loop through the dictionary and get the rides
    #using .get method to pick out the required fields per ride
    for ride in rides:
        ride_id = ride.get('id')
        ride_title = ride.get('title')
    
        #add the id and title to dictionary
        all_rides.update({ride_id: ride_title})
    return jsonify(all_rides)
  
    
#show details of a ride
@app.route('/api/v1/rides/<int:id>', methods=['GET'])
def view_ride(id):
    #loop through the rides and find ride with the id
    for ride in rides:
        #loop through the dictionary and get the rides
        #using .get method to pick out the ride id
        if ride.get('id') == id:
            #store the ride details in variable
            search = ride
            # return the data in json format
            return jsonify({'You searched': search})                               


#create a ride
@app.route('/api/v1/rides', methods=['POST'])
def add_ride():
    new_ride = {
        'id': request.json['id'],
        'car_license': request.json['car_license'],
        'title': request.json['title'],
        'ride_date': request.json['ride_date'],
        'distance': request.json['distance'],
        'start_time': request.json['start_time'],
        'arrival_time': request.json['arrival_time'],
        'ride_price': request.json['ride_price']
    }

    """Append to the list holdng all ride details"""
    rides.append(new_ride)

    #new dictionary to add id and title
    all_rides = {}
    #loop through the dictionary and get the rides
    #using .get method to pick out the required fields per ride

    for ride in rides:
        ride_id = ride.get('id')
        ride_title = ride.get('title')

        #add the id and title to dictionary
        all_rides.update({ride_id: ride_title})
    return jsonify(all_rides)


@app.route('/api/v1/rides/<int:id>/<string:requests>', methods=['GET', 'POST'])
def ride_request(id, requests):
    #show the fields to be responded
    #join keyword should be used to request rides
    if request.method == 'GET' and requests == 'join':
        return jsonify({'You should fill': requested})
    ride_request = {
        'id': request.json['id'],
        'title':  request.json['title'],
        'requester': request.json['requester'],
        'ride_price': request.json['ride_price']
    }
    if request.method == 'POST' and requests == 'join':
        requested.append(ride_request)
    return jsonify({'Created request': ride_request})


@app.route('/api/v1/rides/<int:id>', methods=['DELETE'])
def delete_ride(id):
    #loop through the dictionary and get the rides
    #using .get method to pick out the ride with id entered
    for ride in rides:
        if ride.get('id')==id:
            to_delete = ride
            #find the index of the ride
            ride_index = rides.index(to_delete)

            #delete the ride entry
            ride_deleted = rides.pop(ride_index)

    return jsonify({'You deleted': ride_deleted})



@app.route('/api/v1/rides/edit/<int:id>',methods=['GET','PUT'])
def edit_ride(id):
    #loop through the dictionary and get the rides
    #using .get method to pick out the ride required to be requested
    if request.method=='GET':
        for ride in rides:
            if ride.get('id') == id:
                to_edit=ride
                return jsonify({"You want to edit":to_edit})

    elif request.method=='PUT':
        edit_details = {
            'id': request.json['id'],
            'car_license_': request.json['car_license'],
            'title': request.json['title'],
            'ride_date': request.json['ride_date'],
            'distance': request.json['distance'],
            'start_time': request.json['start_time'],
            'arrival_time': request.json['arrival_time'],
            'ride_price': request.json['ride_price']
        }

        """Append to the list holdng all ride details"""
        rides.append(edit_details)

        #new dictionary to add id and title
        all_rides = {}
        #loop through the dictionary and find all ids and titles

        for ride in rides:
            ride_id = ride.get('id')
            ride_title = ride.get('title')

            #add the id and title to dictionary
            all_rides.update({ride_id: ride_title})
        return jsonify(all_rides)


@app.route('/api/v1/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return jsonify({'fields to fill': users})
    elif request.method == 'POST':
        new_user = {
            'id': request.json['id'],
            'email': request.json['email'],
            'username': request.json['username'],
            'password': request.json['password']
        }

    #add the new use to list of users
    users.append(new_user)
    return jsonify({'users': users})


@app.route('/api/v1/signin', methods=['GET', 'POST'])
def signin():
    known_user = {
        'email': '',
        'password': ''
    }
    if request.method=='GET':
        return jsonify({'Enter this':known_user})

    elif request.method == 'POST':
        known_user = {
            'email': request.json['email'],
            'password': request.json['password']
        }
        #loop through users to find user email and password
        #using password for authentication illustration
        for user in users:
            #check if the password got == password registered
            if user.get('password') == known_user.get('password'):
                return jsonify({'Yeey! welcome back!!': known_user.get('email')})

        return jsonify({'Please signup to join us': known_user.get('email')})

                           



