from flask import Flask,jsonify,request
from app import app
from data import rides



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
    
