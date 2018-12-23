from flask import Flask, Response, jsonify
from models import db, Address
import request
import json
import requests
import socket

app = Flask(__name__)
POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'tkai',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

@app.route("/")
def main():
    return 'Service is working'

@app.route("/address/<user_id>", methods = ['GET'])
def address(user_id):
    userid = user_id
    address = db.session.query(Address).filter_by(user_id=userid).first()
    return address.address

if __name__ == '__main__':
    app.run(port=5200, debug=True)
