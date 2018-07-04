import pytest
import pytest
from app import app 
import json

""" my mock data to test fuctionality of code"""
mock_user={"email":"yagamidelight@gmail.com","username":"deyagami","password":"delight"}


#testing user signup endpoint
def test_signup_exist():
    result=app.test_client()
    response=result.post('/auth/signup', data=json.dumps(mock_user),content_type='application/json')
    assert(response.status_code==200)