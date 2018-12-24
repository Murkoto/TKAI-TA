from flask import Flask, Response, jsonify, request
from models import db, Address
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

@app.route("/address/add", methods=['POST'])
def add_address():
    userid = request.form.get('userid')
    newaddress = request.form.get('address')

    if not newaddress:
        return {'status': 'ok'}
    try:
        newRec = Address(user_id=userid, address=newaddress)
        db.session.add(newRec)
        db.session.commit()
        return jsonify({'status': 'ok', 'msg': 'Succesfully added'})
    except Exception as e:
        print e
        return jsonify({'status': 'error', 'msg': e.detail})

@app.route("/address/update", methods=['POST'])
def update_address():
    userid = request.form.get('userid')
    newaddress = request.form.get('address')
    userRec = db.session.query(Address).filter_by(user_id=userid).first()
    userRec.address = newaddress
    try:
        db.session.commit()
        return jsonify({'status': 'ok'})
    except Exception as e:
        print e  # -*- coding: utf-8 -*-
        return jsonify({'status': 'error', 'msg': e.detail})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5200, debug=True)
