from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from user import app, db
import sqlite3 as sql

def migrate():
    conn = sql.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (' +
                    'id INTEGER PRIMARY KEY,' +
                    'name varchar NOT NULL)')

if __name__ == '__main__':
    # manager.run()
    migrate()
