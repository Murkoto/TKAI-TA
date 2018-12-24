from flask import Flask, Response, jsonify, request
from models import db, Users
import requests
import socket

app = Flask(__name__)
POSTGRES = {
    'user': 'postgres',
    'pw': '123',
    'db': 'tkai',
    'host': 'PostgreSQL',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

host_name = socket.gethostname()
print(host_name)
host_ip = socket.gethostbyname(host_name)
print(host_ip)

@app.route("/")
def main():
    return 'Service is working'

@app.route("/users")
def user_list():
    userlist = db.session.query(Users)
    jsonRec = []
    for user in userlist:
        address = get_user_address(user.id)
        data = user.to_json()
        data['address'] = address
        jsonRec.append(data)
    return jsonify(jsonRec)

def get_user_address(userid):
    try:
        r = requests.get('http://address'+ ':5200/address/'+str(userid))
        if r.status_code == requests.codes.ok:
            print(r.text)
            return r.text
        else:
            return "Address service is not available"
    except requests.ConnectionError as e:
        print # -*- coding: utf-8 -*-
        return "Address service is not available"

@app.route("/users/add")
def add_user():
    newname = request.args.get('name', type=str)
    newphone = request.args.get('phone', default=None, type=str)
    address = request.args.get('address', default=None, type=str)

    if not newname or not address:
        return{
            'status': 'error',
            'msg': 'Name and Address parameter is needed'
        }
    newRec = Users(name=newname, phone=newphone)
    db.session.add(newRec)
    db.session.commit()

    try:
        r = requests.post('http://address'+ ':5200/address/add', data={'userid' : newRec.id, 'address' : address})
        if r.status_code == requests.codes.ok:
            if r.json()['status'] == 'ok':
                return jsonify({'status': 'ok', 'msg': 'Successfully added'})
            else:
                db.session.delete(newRec)
                db.session.commit()
                return jsonify({'status': 'error', 'msg': r.json()['msg']})
        else:
            db.session.delete(newRec)
            db.session.commit()
            return jsonify({'status': 'error', 'msg': r.json()['msg']})
    except requests.ConnectionError as e:
        db.session.delete(newRec)
        db.session.commit()
        print e # -*- coding: utf-8 -*-
        return jsonify({'status': 'error', 'msg': "Address service is not available"})

@app.route('/users/delete/<user_id>')
def delete_user(user_id):
    userid = user_id
    userRec = db.session.query(Users).filter_by(id=userid).first()
    if not userRec:
        return jsonify({'status': 'ok', 'msg': "Data doesn't exist"})
    db.session.delete(userRec)
    db.session.commit()
    return jsonify({'status': 'ok', 'msg': 'Successfully deleted'})

@app.route('/users/update/<user_id>')
def update_user(user_id):
    userid = user_id
    newname = request.args.get('name', type=str, default=None)
    newphone = request.args.get('phone', default=None, type=str)
    address = request.args.get('address', default=None, type=str)
    if address:
        try:
            r = requests.post('http://address'+ ':5200/address/update', data={'userid' : userid, 'address' : address})
            if r.status_code != requests.codes.ok or r.json()['status'] != 'ok':
                return jsonify({'status': 'error', 'msg': r.json()['msg']})
        except requests.ConnectionError as e:
            print e # -*- coding: utf-8 -*-
            return jsonify({'status': 'error', 'msg': "Address service is not available"})

    userRec = db.session.query(Users).filter_by(id=userid).first()
    if newname:
        userRec.name = newname
    if newphone:
        userRec.phone = newphone
    try:
        db.session.commit()
        return jsonify({'status': 'ok', 'msg': 'Sucessfully updated'})
    except Exception as e:
        print e  # -*- coding: utf-8 -*-
        return jsonify({'status': 'error', 'msg': e.detail})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
