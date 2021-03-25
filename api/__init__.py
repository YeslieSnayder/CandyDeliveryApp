from flask import Flask
from model.model import Model

HOST = '0.0.0.0'
PORT = 8080

app = Flask(__name__)
model = Model()
