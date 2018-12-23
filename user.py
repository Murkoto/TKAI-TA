from flask import Flask, Response, jsonify
from models import db, Users
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
    r = requests.get('http://'+host_ip + ':5200/address/'+str(userid))
    if r.status_code == requests.codes.ok:
        print(r.text)
        return r.text
    else:
        return "Address service is not available"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
