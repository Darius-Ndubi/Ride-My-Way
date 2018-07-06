import pytest
import psycopg2
from app import app
import json

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
    #connect.close()

def drop_tables():
    """DROP TABLE new_user"""
    """DROP TABLE ride"""
    """DROP TABLE requestss"""
    curs.close()
    connect.commit()


createall_tables()
drop_tables()

mock_sign={"email":"yagfafmidelight@gmail.com","password":"delight"}
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
A fuction to find users signed in

"""
def registered():
    curs = connect.cursor()
    curs.execute("SELECT * FROM new_user")
    all=curs.fetchall()
    connect.commit()
    #close the connection
    curs.close()
    return len(all)

def header_token():
    result=app.test_client()
    result.post('/api/v1/auth/signup', data=json.dumps(mock_reg),content_type='application/json')
    response=result.post('/api/v1/auth/login', data=json.dumps(mock_sign),content_type='application/json')
    return response

header_token()

"""
    A test to test users sign  up
"""
def test_signup():
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg),content_type='application/json')
    assert(response.status_code==201)


"""
    A test to test users sign in
"""
def test_signin():
    result=app.test_client()
    response=result.post('/api/v1/auth/login', data=json.dumps(mock_sign),header={"Authorization Header":response},content_type='application/json')
    assert(response.status_code==200)


"""
    A test to test if rides are being added to the database
"""
def test_Add_ride():
    result=app.test_client()
    response=result.post('/api/v1/rides',data=json.dumps(mock_ride),content_type='application/json')
    assert(response.status_code==200)

def test_signup():
    result=app.test_client()
    old_num=registered()
    response=result.post('/auth/signup', data=json.dumps(mock_reg),content_type='application/json')
    new_num=registered()
    assert(old_num+1>new_num),201
"""
    A test on get all rides from db
"""
def test_Get_rides():
    result=app.test_client()
    response=result.get('/api/v1/rides')
    assert(response.status_code==200)

"""
A test on geting a specific ride
"""
def test_Get_ride():
    result=app.test_client()
    response=result.get('/api/v1/rides/1')
    assert(response.status_code==200)
"""
    A test on regetting ride requests
"""
def test_Ride_requests():
    result=app.test_client()
    response=result.get('/api/v1/rides/1/requests')
    assert(response.status_code==200)



drop_tables()



