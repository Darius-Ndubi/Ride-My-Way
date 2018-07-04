import pytest
from app import app
import json

mock_sign={"email":"yagamidelight@gmail.com","password":"delight"}

def test_signin():
    
    result=app.test_client()
    response=result.post('/auth/signin', data=json.dumps(mock_sign),content_type='application/json')
    assert(response.status_code==200)




