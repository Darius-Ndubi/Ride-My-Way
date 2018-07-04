from flask import Flask

"""Create an instace of flask"""
app=Flask(__name__)

"""Add a secret key for the app"""
app.secret_key = '\xaa\x98\xfb\xf7\xcb\xce\xd3\xdf\x96'

from app import views,data 
