import sqlite3
from public import website
from flask import g


DATABASE = 'db/valve-store.db'


def connect_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = convert_row_to_dictionary
    return db



def init_db():
    with website.app_context():
        db = get_db()
        with website.open_resource('/db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db



@website.before_request
def before_request():
    g.db = connect_db()



@website.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()



def query_db(query, args=(), one=False):
    try:
        cur = get_db().execute(query, args)
        get_db().commit()
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.Error as er:
        print('sqlite error:', er)
        return None


def convert_row_to_dictionary(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

