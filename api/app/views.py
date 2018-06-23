from flask import Flask,jsonify,request
from app import app
from data import rides,requested,users
import json



"""Endpoint to view all rides"""
@app.route('/api/v1/rides',methods=['GET'])
def view_rides():
    #get all titles
    #new dictionary to add id and title
    All_rides = {}
    #loop through the dictionary and find all ids and titles

    for ride in rides:
        for detail in ride:
            if detail == 'id':
                ride_id = ride[detail]
            elif detail == 'Title':
                ride_title = ride[detail]
    
        #add the id and title to dictionary
        All_rides.update({ride_id: ride_title})
    return jsonify(All_rides)
  
    
#show details of a ride
@app.route('/api/v1/rides/<int:id>', methods=['GET'])
def view_ride(id):
    #loop through the rides and find ride with the id
    for ride in rides:

        #loop through each key in a ride
        for detail in ride:

            #if key item is id
            if detail == 'id':

                #if key value == id entered
                if ride[detail] == id:

                    #store the ride details in variable
                    search = ride
                    # return the data in json format
                    return jsonify({'You searched': search})                               


#create a ride
@app.route('/api/v1/rides', methods=['POST'])
def add_ride():
    new_ride = {
        'id': request.json['id'],
        'car_license_no': request.json['car_license_no'],
        'Title': request.json['Title'],
        'Ride Date': request.json['Ride Date'],
        'Distance': request.json['Distance'],
        'Start_time': request.json['Start_time'],
        'Arrival_time': request.json['Arrival_time'],
        'Ride_price': request.json['Ride_price']
    }

    """Append to the list holdng all ride details"""
    rides.append(new_ride)

    #new dictionary to add id and title
    All_rides = {}
    #loop through the dictionary and find all ids and titles

    for ride in rides:
        for detail in ride:
            if detail == 'id':
                ride_id = ride[detail]
            elif detail == 'Title':
                ride_title = ride[detail]

        #add the id and title to dictionary
        All_rides.update({ride_id: ride_title})
    return jsonify(All_rides)


@app.route('/api/v1/rides/<int:id>/<string:requests>', methods=['GET', 'POST'])
def ride_request(id, requests):
    #show the fields to be responded
    #join keyword should be used to request rides
    if request.method == 'GET' and requests == 'join':
        return jsonify({'You should fill': requested})
    ride_request = {
        'id': request.json['id'],
        'Title':  request.json['Title'],
        'Requester': request.json['Requester'],
        'Ride_price': request.json['Ride_price']
    }
    if request.method == 'POST' and requests == 'join':
        requested.append(ride_request)
    return jsonify({'Created request': ride_request})


@app.route('/api/v1/rides/<int:id>', methods=['DELETE'])
def delete_ride(id):
    #loop through rides ad find ride with id given
    for ride in rides:
        for detail in ride:
            if detail == 'id':
                if ride[detail] == id:
                    to_delete = ride
                    #find the index of the ride
                    ride_index = rides.index(to_delete)

                    #delete the ride entry
                    ride_deleted = rides.pop(ride_index)

    return jsonify({'You deleted': ride_deleted})



@app.route('/api/v1/rides/edit/<int:id>',methods=['GET','PUT'])
def edit_ride(id):
    """Loop through all rides and find ride with entered id"""
    if request.method=='GET':
        for ride in rides:
            for detail in ride:
                if ride[detail]==id:
                    to_edit=ride
                    return jsonify({"You want to edit":to_edit})

    elif request.method=='PUT':
        edit_details = {
            'id': request.json['id'],
            'car_license_no': request.json['car_license_no'],
            'Title': request.json['Title'],
            'Ride Date': request.json['Ride Date'],
            'Distance': request.json['Distance'],
            'Start_time': request.json['Start_time'],
            'Arrival_time': request.json['Arrival_time'],
            'Ride_price': request.json['Ride_price']
        }

        """Append to the list holdng all ride details"""
        rides.append(edit_details)

        #new dictionary to add id and title
        All_rides = {}
        #loop through the dictionary and find all ids and titles

        for ride in rides:
            for detail in ride:
                if detail == 'id':
                    ride_id = ride[detail]
                elif detail == 'Title':
                    ride_title = ride[detail]

            #add the id and title to dictionary
            All_rides.update({ride_id: ride_title})
        return jsonify(All_rides)


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
            for detail in user:
                if detail=="password":
                   
                    for dit in known_user:
                        if dit =="password":
                            
                            if user[detail]==known_user[dit]:
                                found_password=known_user[dit]

                                return jsonify({"Hello there": found_password})

                           



