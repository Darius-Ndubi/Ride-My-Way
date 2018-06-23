"""Writing tests using pytest"""
from app import app
import pytest


"""
    End points to be tested are
        a>view_rides
        b>view_ride
        c>add_ride
        d>ride_request
        e>delete ride
        e>edit article
        f>delete article
        g>ride_response
"""

def test_view_rides():
    """In the list of rides stored
    loop through all the rides and return there
    titles and ids"""
    #-----work--tomorrow---#
    result=app.test_client()
    response=result.get('/api/v1/rides')
    assert(response.status_code==200)

def test_view_ride():

    """
        A test on view_ride endpoint
    """
    result=app.test_client()
    response=result.get('/api/v1/rides/1')
    assert(response.status_code==200)


def test_add_ride():
    """
        A test on create ride end point to verify if it Posts data
    """
    result = app.test_client()
    response = result.post('api/v1/rides')
    assert(response.status_code == 201)


def test_ride_request():
    """
        A test on ride request functionality of the Api
    """
    result = app.test_client()
    response = result.post('api/v1/rides/<int:id>/<string:request>')

    if response == True:
        assert(response.status_code == 201)
    else:
        assert(response.status_code == 404)


def test_delete_ride():
    """
        A test to test user delete ride endpoint
        -->'/api/v1/rides/<int:id>',methods=['DELETE']
    """
    result = app.test_client()
    response = result.delete('api/v1/rides/1')
    assert(response.status_code == 200)

def test_edit_ride():
    """
        A test to test user edit_ride endpoint
    """
    result=app.test_client()
    response=result.put('api/v1/rides/edit/1')
    assert(response.status_code==202)


def test_signup():
    """
        A test to test the users sign up
    """
    result = app.test_client()
    response = result.post('/api/v1/sigup')
    if response == True:
        assert(response.status_code == 201)
    else:
        assert(response.status_code == 404)
