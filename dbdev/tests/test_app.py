import pytest
import psycopg2
from endpoints import endpoints

connect = psycopg2.connect("dbname='testride' host='localhost' user='dario' password='riot'")
curs = connect.cursor()

def createall_tables():
    commands=(
        """
        CREATE TABLE IF NOT EXISTS new_user(
            id SERIAL PRIMARY KEY NOT NULL,
            email VARCHAR NOT NULL,
            username VARCHAR(10) NOT NULL,
            password VARCHAR NOT NULL
            )
        """,
        """
        CREATE TABLE IF NOT EXISTS ride(
            r_id SERIAL PRIMARY KEY NOT NULL,
            car_license VARCHAR(10) NOT NULL,
            title VARCHAR(20) NOT NULL,
            ride_date VARCHAR(10) NOT NULL,
            distance INT NOT NULL,
            num_seats INT NOT NULL,
            start_time VARCHAR(10) NOT NULL,
            arrival_time VARCHAR(10) NOT NULL,
            ride_price INT NOT NULL,
            creator VARCHAR(20) NOT NULL
            )
        """,
        """
        CREATE TABLE IF NOT EXISTS requestss(
            req_id SERIAL PRIMARY KEY NOT NULL,
            ride_id INT NOT NULL REFERENCES ride(r_id),
            car_license VARCHAR(10) NOT NULL,
            requester_name VARCHAR(20) NOT NULL,
            ride_date VARCHAR(10) NOT NULL,
            title VARCHAR(20) NOT NULL,
            num_seats INT NOT NULL,
            ride_price INT NOT NULL,
            creator VARCHAR(20) NOT NULL,
            action VARCHAR(10)
            )
        """
    )

    for db_table in commands:
        curs.execute(db_table)
    
    curs.close()
    connect.commit()
    connect.close()


createall_tables()

mock_sign={"email":"yagamidelight@gmail.com","password":"delight"}
mock_reg={"email":"yagamidelight@gmail.com","username":"delight","password":"delight"}
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
    A test to test users sign  up
"""
def test_signup():
    result=users.test_client()
    response=result.post('/auth/signup', data=json.dumps(mock_reg),content_type='application/json')
    assert(response.status_code==200)

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
"""
    A test on regetting ride requests
"""
def rest_Ride_requests():
    result=app.test_client()
    response=result.get('/rides/1/requests')
    assert(response.status_code==200)

"""
    A test on regetting ride requests
"""

def rest_Ride_requests():
    result=app.test_client()
    response=result.post('/rides/1/requests')






