from flask import Flask, Response, jsonify, request
from models import db, Users
import json
import sqlite3 as sql

app = Flask(__name__)
# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'password',
#     'db': 'tkai',
#     'host': 'localhost',
#     'port': '5432',
# }
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# db.init_app(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route("/")
def main():
    return 'Service is working'

@app.route("/add")
def add():
    user = request.args.get('nama')
    with sql.connect("database.db") as con:
            cur = con.cursor()
            name = user
            cur.execute("INSERT INTO users VALUES (NULL, ?)", [user])
            
            con.commit()
            msg = "Record successfully added"
    return 'ditambahkan' + user

@app.route("/drop")
def drop():
    with sql.connect("database.db") as con:
            cur = con.cursor()
            name = 'Kicut'
            cur.execute("DROP table users")
            
            con.commit()

@app.route("/users")
def user_list():
    conn = sql.connect('database.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("select * from users")
    rows = cursor.fetchall()

    print(rows)
    
    return jsonify(rows)
    # list = db.session.query(Users)
    # jsonRec = [z.to_json() for z in list]
    # print(jsonRec)
    # return jsonify(jsonRec)
if __name__ == '__main__':
    app.run(port=5000, debug=True)
