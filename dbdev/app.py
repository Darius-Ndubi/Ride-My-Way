from flask import Flask,request,jsonify
import json
from flask_restplus import Api,Resource,fields,reqparse
from models import DbManager
from werkzeug.security import generate_password_hash

#create an instance of flask
app=Flask(__name__)
api=Api(app)


"""Add a secret key for the app"""
app.secret_key = '\xaa\x98\xfb\xf7\xcb\xce\xd3\xdf\x96'


class Manage_rides(object):
    parser = reqparse.RequestParser()

    def __init__(self):
        pass

    def get_user_dits(self):

        self.parser.add_argument('username', required=True,
                                 help="Username cannot be blank!")
        self.parser.add_argument('password', required=True,
                                 help="Password cannot be blank!")
        self.parser.add_argument('email', required=True,
                                 help="Email cannot be blank!")

        self.args = self.parser.parse_args()

        return self.args



R=Manage_rides()

@api.route('/auth/signup')
class Signup(Resource):
    def post (self):
        self.args=R.get_user_dits()

        #validating that  non of the enterd fields is empty
        if self.args['email'] == "":
            return jsonify({"Error": "Email field cannot be empty"})
        elif self.args['username'] == "":
            return jsonify({"Error": "Username field cannot be empty"})
        elif self.args['password'] == "":
            return jsonify({"Error": "Password fields cannot be empty"})
        #check if the email has @ and .com
        elif '@' and '.com' not in self.args['email']:
            return jsonify({"Error": "Email as enterd is not valid"})

        #hashing passwd
        self.passwd=self.args['password']
        #hashing the password
        self.passwd_hash=generate_password_hash(self.passwd)
        
        #print (self.passwd_hash)
        self.new_user=DbManager(email=self.args['email'],username=self.args['username'],password=self.args['password'])
        #self.new_user.signupuser(email=self.new_user.email,username=self.new_user.username,password=self.new_user.password)
        
        self.new_user.signupUser()

        return {"Success":"login"}


@api.route('/auth/signin')
class Signin(Resource):
    pass


if __name__=='__main__':
    app.run(debug=True)
