from flask import Flask,jsonify,request
from app import app
from data import rides
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