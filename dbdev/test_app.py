import pytest
from app import app
import json

mock_sign={"email":"yagamidelight@gmail.com","password":"delight"}
mock_ride={
    "car_lisense": "KAC 345T",
    "title": "Troy to Sparta",
    "ride_date": "06-06-2018",
    "distance": 45,
    "no_seats": 7,
    "start_time": "0700",
    "arrival_time": "1700",
    "ride_price": 1500,
    "creator":"Yagami Light"
    }


"""
    A test to test users sign in
"""
def test_signin():
    
    result=app.test_client()
    response=result.post('/auth/signin', data=json.dumps(mock_sign),content_type='application/json')
    assert(response.status_code==200)


"""
    A test to test if rides are being added to the database
"""
def test_Add_ride():
    result=app.test_client()
    response=result.post('/rides',data=json.dumps(mock_ride),content_type='application/json')
    assert(response.status_code==200)

"""
    A test on get all rides from db
"""
def test_Get_rides():
    result=app.test_client()
    response=result.get('/rides')
    assert(response.status_code==200)

"""
A test on geting a specific ride
"""
def test_Get_ride():
    result=app.test_client()
    response=result.get('/rides/1')
    assert(response.status_code==200)




