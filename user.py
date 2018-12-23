from flask import Flask, Response, jsonify
from models import db, Users
import json

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

@app.route("/")
def main():
    return 'Service is working'

@app.route("/users")
def user_list():
    list = db.session.query(Users)
    jsonRec = [z.to_json() for z in list]
    print(jsonRec)
    return jsonify(jsonRec)
if __name__ == '__main__':
    app.run(port=5000, debug=True)
