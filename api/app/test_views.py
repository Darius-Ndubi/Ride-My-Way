"""Writing tests using pytest"""
from app import app
import pytest
from data import mock_ride,mock_request,mock_user,mock_known_user,mock_edited_ride
import json


"""
    End points to be tested are
        a>view_rides
        b>view_ride
        c>add_ride
        d>ride_request
        e>delete ride
        e>edit article
        f>signup
        g>gignin
"""

def test_view_rides():
    """
        In the list of rides stored
        loop through all the rides and return there
        titles and ids
    """

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
    response = result.post('api/v1/rides', data=json.dumps(mock_ride) ,content_type='application/json')
    json.loads(response.data)
    
    assert response.json == {'1': 'Troy to Sparta',
                             '2': 'Troy to Ithaca',
                             '3': 'The Under world to Athens',
                             '4': 'Colchins to Athens'}
    assert(response.status_code == 200)


def test_ride_request():
    """
        A test on ride request functionality of the Api
    """
    result = app.test_client()
    response = result.post('api/v1/rides/2/join', data=json.dumps(mock_request) ,content_type='application/json')
    json.loads(response.data)

    assert response.json == {'Created request':{'id': 2,
                            'title': 'Troy to Ithaca',
                            'requester': 'Suzuki Kakashi',
                            'ride_price': '800'}}
    assert(response.status_code==200)


def test_delete_ride():
    """
        A test to test user delete ride endpoint
        -->'/api/v1/rides/<int:id>',methods=['DELETE']
    """
    result = app.test_client()
    response = result.delete(
        'api/v1/rides/4', data=json.dumps(mock_ride), content_type='application/json')
    json.loads(response.data)
    
    assert response.json == {u'You deleted':{u'id': 4,
                             u'car_license': u'KCG 001Y',
                             u'title': u'Colchins to Athens',
                             u'ride_date': u'26-06-2018',
                             u'distance': u'100',
                             u'start_time': u'0500',
                             u'arrival_time': u'1000',
                             u'ride_price': u'150'
                             }}

    assert(response.status_code == 200)

def test_edit_ride():
    """
        A test to test user edit_ride endpoint
    """
    result=app.test_client()
    response = result.put(
        'api/v1/rides/edit/4', data=json.dumps(mock_edited_ride), content_type='application/json')
    
    json.loads(response.data)

    assert response.json == {'1': 'Troy to Sparta',
                             '2': 'Troy to Ithaca',
                             '3': 'The Under world to Athens',
                             '4': 'Thebes to Ithaca'}
    assert(response.status_code==200)

    


def test_signup():
    """
        A test to test the users sign up
    """
    result = app.test_client()
    response = result.post('/api/v1/signup', data=json.dumps(mock_user), content_type='application/json')
    
    json.loads(response.data)
    
    assert response.json == {'users':[
        {
            'id': '',
            'email': '',
            'username': '',
            'password': ''
        },
        {
            'id': 1,
            'email': 'ndubidarius@gmail.com',
            'username': 'dario',
            'password': 'masaysay'     
        }
    ]}

    assert(response.status_code==200)
    


def test_signin():
    """
        A test to test user sign in endpoint
    """
    result = app.test_client()
    response = result.post('/api/v1/signin',data=json.dumps(mock_known_user), content_type='application/json')
    input=json.loads(response.data)
    if input.get('password')=='masaysay':
        assert response.json == {'Yeey! welcome back!!': mock_known_user.get('email')}
        assert(response.status_code == 200)
    elif input.get('password') == 'masaysay':
        assert response.json =={'Please signup to join us': mock_known_user.get('email')}
        assert(response.status_code == 200)
