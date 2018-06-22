"""Writing tests using pytest"""
from app import app
import pytest


"""
    End points to be tested are
        a>view_rides
        b>view_ride
        c>add_ride
        d>signup
        e>signin
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

