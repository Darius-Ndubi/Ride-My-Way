from flask import Flask,request,jsonify
import json
from flask_restplus import Api,Resource,fields,reqparse
from models import DbManager
from flask_jwt_extended import JWTManager,create_access_token
from werkzeug.security import check_password_hash
#create an instance of flask
app=Flask(__name__)
api=Api(app)
jwt = JWTManager(app)

"""Add a secret key for the app"""
app.secret_key = '\xaa\x98\xfb\xf7\xcb\xce\xd3\xdf\x96'
app.config['JWT_SECRET_KEY'] = '\xe7\x06K\x86>\xe5\x98/\x11\x06\xfbJA-\x86'

class Manage_rides(object):
    parser = reqparse.RequestParser()

    def __init__(self):
        pass

    def get_user_login(self):

        self.parser.add_argument('email', required=True,
                            help="email cannot be blank!")
        self.parser.add_argument('password', required=True,
                            help="password cannot be blank!")
        
        self.args = self.parser.parse_args()

        return self.args



R=Manage_rides()

@api.route('/auth/signin')
class Signin(Resource):
    def post (self):
        self.args = R.get_user_login()

        #validating that  non of the enterd fields is empty
        if self.args['email'] == "":
            return jsonify({"Error": "Email field cannot be empty"})
        elif self.args['password'] == "":
            return jsonify({"Error": "Password fields cannot be empty"})

        elif '@' not in self.args['email']:
            return jsonify({"Error": "Email as enterd is not valid"})
        elif '.com' not in self.args['email']:
            return jsonify({"Error": "Email as enterd is not valid"})
        
        ##check users existance in db
        self.loginuser=DbManager()

        self.exist=self.loginuser.signinusercheck(self.args['email'],self.args['email'])
            
        if self.exist:
            #print (self.exist)
            #compare the has with the one entered
            if check_password_hash(self.exist[0],self.args['password']):
                #if thre is a match give user an access token
                access_token = create_access_token(self.args['email'])
                return({self.args.email: {"Use this token to create a ride":access_token}})
            #if the hashes dont match
            else:
               return ({"Error":"Invalid password"})
        else:
            return({"Error":"User does not exist please register"})


        
if __name__=='__main__':
    app.run(debug=True)