from flask import Flask,jsonify,request
from app import app
from data import rides,requested
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
