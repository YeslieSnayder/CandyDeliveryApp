from flask import Flask
from application.model.model import *

HOST = '0.0.0.0'
PORT = 8080

app = Flask(__name__)
model = Model()
