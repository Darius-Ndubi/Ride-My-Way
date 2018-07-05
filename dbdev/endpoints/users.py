from flask_restplus import Api,Namespace,Resource,fields,reqparse
from app.models import DbManager
from flask import jsonify

class User_fields(object):
    parser = reqparse.RequestParser()

    def get_user_dits(self):

        self.parser.add_argument('username', required=True,
                                    help="Username cannot be blank!")
        self.parser.add_argument('password', required=True,
                                    help="Password cannot be blank!")
        self.parser.add_argument('email', required=True,
                                    help="Email cannot be blank!")

        self.args = self.parser.parse_args()

        return self.args

    def get_user_login(self):

        self.parser.add_argument('email', required=True,
                            help="email cannot be blank!")
        self.parser.add_argument('password', required=True,
                            help="password cannot be blank!")
        
        self.args = self.parser.parse_args()

        return self.args

api = Namespace("users",  description="User endpoints")



R=User_fields()


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
            
        self.new_user=DbManager(email=self.args['email'],username=self.args['username'],password=self.args['password'])
        
        #check if the usr exists
        self.exist=self.new_user.checkUser()
        #if user is found give info why they cant be registerd
        if self.exist:
            return({"Email Error":"Email is already linked to another user, pick another one"}),406
        #if not found allow them to register with us
        else:
            self.new_user.signupUser()
            return({"Successfull":"Proceed to login"})


#@api.route('/auth/signin')
class Signin(Resource):
    def post (self):
        args = R.get_user_login()

        #validating that  non of the enterd fields is empty
        if args['email'] == "":
            return jsonify({"Error": "Email field cannot be empty"})
        elif args['password'] == "":
            return jsonify({"Error": "Password fields cannot be empty"})

        elif '@' not in args['email']:
            return jsonify({"Error": "Email as enterd is not valid"})
        elif '.com' not in args['email']:
            return jsonify({"Error": "Email as enterd is not valid"})

        return (DbManager.login(args['email'],args['password']))
            
        


api.add_resource(Signup, '/auth/signup')
api.add_resource(Signin, '/auth/signin')
